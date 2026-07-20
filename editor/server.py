#!/usr/bin/env python3
"""
Local server for the GrapesJS editor. Standard library only, no
dependency beyond Python 3.

Serves the static files (the real site + the editor's own assets) and
handles POST /save to write the changes made in the canvas.

Usage:
    python3 editor/server.py [port]      (default: 8767)

Doesn't publish anything on its own: it only writes to disk. `git push`
stays a separate, deliberate step — see scripts/publish.sh.
"""

import http.server
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets" / "img"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8767

MAX_UPLOAD_BYTES = 20_000_000  # 20MB — generous for a phone photo, small enough to stay safe
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}

# If any of these disappear from the saved HTML, main.js silently stops
# working: the countdown freezes, the RSVP form stops sending, the
# gallery stops opening. A plain string check is enough for a warning —
# no need for a real HTML parser for this purpose.
REQUIRED_IDS = [
    "cd-days", "cd-hours", "cd-minutes", "cd-seconds",
    "countdown", "lightbox", "rsvp-form", "rsvp-note",
]
REQUIRED_CLASSES = ["reveal", "gallery-grid"]
REQUIRED_FIELDS = ["first-name", "last-name", "attending", "guests", "guest-names", "message"]


# iPhones save photos as HEIC by default. We can't fix that here — HEIC
# doesn't render in most browsers (Chrome, Firefox, Android all lack
# native support), so it would look broken to most wedding guests. Better
# to reject it clearly than to silently relabel it as .jpg and ship a
# photo nobody but iPhone/Safari users can actually see.
REJECTED_EXTENSIONS = {
    ".heic": "iPhone photos are saved as HEIC, which most browsers can't display. "
             "Convert it first: on a Mac, open it in Preview and use File → Export → JPEG.",
    ".heif": "This HEIF photo won't display in most browsers. "
             "Convert it to JPEG first (on a Mac: Preview → File → Export → JPEG).",
}


def safe_filename(name):
    """Strip everything except a plain, ASCII-safe filename — no path
    components, no characters that could escape ASSETS_DIR or confuse a
    shell/URL later. Raises ValueError with a user-facing message for a
    format we deliberately don't accept (see REJECTED_EXTENSIONS)."""
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = Path(name).name  # drops any directory component, defeats ../../
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name).strip("-") or "photo"
    stem, ext = Path(name).stem, Path(name).suffix.lower()

    if ext in REJECTED_EXTENSIONS:
        raise ValueError(REJECTED_EXTENSIONS[ext])
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        ext = ".jpg"
    return stem or "photo", ext


def write_new_file(stem, ext, content):
    """assets/img/photo.jpg, then photo-1.jpg, photo-2.jpg… Uses an atomic
    create-exclusive open so two uploads racing for the same filename at
    the same instant can never overwrite one another — the loser of the
    race gets the next available name instead of silently clobbering the
    winner's bytes."""
    n = 0
    while True:
        candidate = ASSETS_DIR / (f"{stem}{ext}" if n == 0 else f"{stem}-{n}{ext}")
        try:
            fd = os.open(candidate, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            n += 1
            continue
        with os.fdopen(fd, "wb") as f:
            f.write(content)
        return candidate


def parse_multipart(body, boundary):
    """Minimal multipart/form-data parser for exactly what a browser file
    upload sends. Deliberately not using the stdlib `cgi` module: it's
    deprecated since 3.11 and removed in 3.13, and this project's own
    README tells people to install the latest Python.

    Returns a list of {name, filename, content} dicts — filename is None
    for plain (non-file) fields.
    """
    marker = b"--" + boundary.encode("ascii")
    parts = body.split(marker)
    fields = []
    for part in parts:
        # Strip exactly one leading/trailing CRLF (the multipart framing
        # around each part) — never a blanket .strip(), which would also
        # eat any \r or \n bytes the file's own content happens to end
        # with, silently truncating it.
        if part.startswith(b"\r\n"):
            part = part[2:]
        if part.endswith(b"\r\n"):
            part = part[:-2]
        if not part or part == b"--":
            continue
        if b"\r\n\r\n" not in part:
            continue
        header_block, content = part.split(b"\r\n\r\n", 1)
        headers = header_block.decode("utf-8", errors="replace")
        disp = re.search(r'name="([^"]*)"(?:;\s*filename="([^"]*)")?', headers)
        if not disp:
            continue
        fields.append({"name": disp.group(1), "filename": disp.group(2), "content": content})
    return fields


def find_missing(html):
    missing = []
    for id_ in REQUIRED_IDS:
        if f'id="{id_}"' not in html:
            missing.append(f'id="{id_}"')
    for cls in REQUIRED_CLASSES:
        if not re.search(rf'class="[^"]*\b{re.escape(cls)}\b[^"]*"', html):
            missing.append(f'class="{cls}"')
    for field in REQUIRED_FIELDS:
        if f'name="{field}"' not in html:
            missing.append(f'name="{field}"')
    return missing


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format_, *args):
        sys.stderr.write(f"[editor] {self.address_string()} — {format_ % args}\n")

    def do_POST(self):
        if self.path == "/upload-asset":
            self._handle_upload()
            return
        if self.path != "/save":
            self.send_error(404, "Only /save and /upload-asset accept POST")
            return

        length = int(self.headers.get("Content-Length", 0))
        if length == 0 or length > 10_000_000:
            self._json(400, {"error": "request body missing or too large"})
            return

        try:
            data = json.loads(self.rfile.read(length))
            new_html = data["html"]
            new_css = data["css"]
        except (json.JSONDecodeError, KeyError) as e:
            self._json(400, {"error": f"invalid JSON: {e}"})
            return

        try:
            warnings = self._write(new_html, new_css)
        except Exception as e:
            self._json(500, {"error": str(e)})
            return

        self._json(200, {"ok": True, "warnings": warnings})

    def _handle_upload(self):
        """Receives a photo dropped into the editor's image picker and
        writes a real file to assets/img/ — the point of this endpoint is
        to exist at all: without it, GrapesJS's default behavior is to
        embed the photo as Base64 directly inside index.html (verified
        against its own source), which would bloat the page hugely and
        defeat the "keep photos under 500KB" advice in the README."""
        content_type = self.headers.get("Content-Type", "")
        boundary_match = re.search(r'boundary=(?:"([^"]+)"|([^;]+))', content_type)
        length = int(self.headers.get("Content-Length", 0))

        if not boundary_match or length == 0:
            self._json(400, {"error": "expected multipart/form-data with a file"})
            return
        if length > MAX_UPLOAD_BYTES:
            self._json(400, {"error": f"file too large (max {MAX_UPLOAD_BYTES // 1_000_000}MB)"})
            return

        boundary = boundary_match.group(1) or boundary_match.group(2)
        body = self.rfile.read(length)
        fields = parse_multipart(body, boundary)
        uploaded = [f for f in fields if f["filename"]]

        if not uploaded:
            self._json(400, {"error": "no file found in the upload"})
            return

        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        saved = []
        for field in uploaded:
            try:
                stem, ext = safe_filename(field["filename"])
            except ValueError as e:
                self._json(400, {"error": str(e)})
                return
            path = write_new_file(stem, ext, field["content"])
            saved.append({"src": f"assets/img/{path.name}"})

        # Shape GrapesJS's asset manager expects from `autoAdd: true`:
        # { data: [ {src: "..."} , ... ] }
        self._json(200, {"data": saved})

    def _write(self, new_html, new_css):
        index_path = ROOT / "index.html"
        current = index_path.read_text(encoding="utf-8")

        if "<body>" not in current or "</body>" not in current:
            raise ValueError("index.html has no <body>/</body>: unexpected structure, writing nothing")

        head, _, rest = current.partition("<body>")
        _, _, tail = rest.rpartition("</body>")

        # GrapesJS's editor.getHtml() includes its own <body> tag (the
        # root component), so it must be stripped before reinserting
        # ours — otherwise you end up with a <body> nested inside another.
        clean_body = new_html.strip()
        clean_body = re.sub(r"^<body[^>]*>", "", clean_body, count=1, flags=re.I)
        clean_body = re.sub(r"</body>\s*$", "", clean_body, count=1, flags=re.I).strip()

        # The <script> tag stays fixed: the editor manages structure and
        # style, not the interactive behavior hand-written in js/main.js.
        new_content = (
            f"{head}<body>\n"
            f"{clean_body}\n"
            f'  <script src="js/main.js"></script>\n'
            f"</body>{tail}"
        )

        index_path.write_text(new_content, encoding="utf-8")

        # Separate layer, never overwrites style.css: if GrapesJS's
        # export didn't carry over some advanced detail (animations,
        # media queries, texture), the site doesn't lose the original.
        edited_path = ROOT / "css" / "edited.css"
        header_comment = (
            "/* Generated by the local editor (GrapesJS) — don't edit by hand.\n"
            "   Layers on top of style.css: the latter stays the base. */\n\n"
        )
        edited_path.write_text(header_comment + new_css, encoding="utf-8")

        return find_missing(clean_body)

    def _json(self, code, body):
        payload = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Editor at http://127.0.0.1:{PORT}/editor/  (project root: {ROOT})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
