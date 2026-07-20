# Local editor (GrapesJS) — how it works and its real limits

A visual editor that runs **on your own computer**: no account, no cloud,
no external service to sign up for — it's a local library (npm), not a
cloud product like Webstudio or Framer.

**Looking for how to actually use it — clicking, editing text, changing
colors, swapping photos?** That's
**[HOW-TO-USE-THE-EDITOR.md](../HOW-TO-USE-THE-EDITOR.md)**. This page is
the companion technical reference: what happens under the hood, and the
one real limitation worth knowing about.

## Starting it

```bash
python3 editor/server.py
```

Then open **http://127.0.0.1:8767/editor/**.

It loads the **real** site (not a copy): it reads `../index.html` and
`../css/style.css` fresh, every time you open the page.

## Saving

The "Save to project" button writes to disk:

- `index.html` — replaces the `<body>` content with whatever is in the
  canvas, **keeping** the `<head>` (meta tags, fonts) and the
  `<script src="js/main.js">` tag exactly as they are now.
- `css/edited.css` — a **separate** stylesheet that layers on top of
  `style.css` without ever replacing it (see why, below).

**It doesn't publish anything.** It only writes the local files. Sending
them online stays a deliberate, separate step:
`git add . && git commit -m "..." && git push` (or
`./scripts/publish.sh "message"`).

## A real GrapesJS limitation, verified

While testing the save round-trip, I found that **GrapesJS doesn't
correctly parse properties written in the compact shorthand form
`background: color` and `border: width style color`** — it silently
drops them when importing an existing stylesheet. The expanded forms
(`background-color`, `border-color`, `border-width`, `border-style`)
work fine.

In this starter kit's `style.css`, this affects **7 rules**:

| Selector | Shorthand property |
|---|---|
| `.scroll-hint span` | `background` |
| `.btn-location` | `border` |
| `.divider` | `background` |
| `.chip span` | `border` |
| `.chip input:checked + span` | `background`, `border` |
| `.btn-confirm` | `background`, `border` |
| `.footer` | `border-top` |

**Why nothing looks broken today:** `css/edited.css` layers on top of
`style.css` instead of replacing it — that's exactly why saving writes
a separate file rather than rewriting `style.css` directly. For those 7
rules, `edited.css` simply doesn't say anything about the dropped
properties, and the original declaration in `style.css` stays valid and
visible: borders and backgrounds stay where they are.

**What can happen in practice:** if you open one of these elements in
the Style panel and try to change **its background or border color**,
the change might not survive saving — you'll see it update in the
canvas, but after "Save" and a reload it may revert to the original,
because the export didn't capture the new property.

**If this happens to you:** it's not something you did wrong. Either
edit `css/edited.css` directly and write the rule using
`background-color:`/`border-color:` instead of the shorthand form (that
form always works), or ask an AI assistant (Claude Code, ChatGPT/Codex)
to do it for you — point it at this file and describe what you want.

## Photo uploads — another thing verified, not assumed

Double-clicking a photo in the canvas opens GrapesJS's built-in "Select
Image" dialog. Checked directly in its source
(`grapesjs/dist/index.d.ts`): **without an upload endpoint configured,
GrapesJS embeds uploaded photos as Base64 directly inside `index.html`**
— technically works, but turns a 2MB photo into a page that's several
megabytes of text.

This kit avoids that: `editor/server.py` implements a real
`POST /upload-asset` endpoint (parsing `multipart/form-data` by hand,
deliberately not using Python's `cgi` module — it's deprecated since
3.11 and gone in 3.13), and `editor.js` points GrapesJS's asset manager
at it.

**A second, independent review of this endpoint** (an adversarial
read-through by a separate reviewer, specifically hunting for ways it
could go wrong) found three real issues in the first version, all fixed:

- **iPhone photos (HEIC)** were silently saved with a `.jpg` name while
  keeping their actual HEIC bytes — producing a file that looks fine in
  the upload dialog but shows as broken for the many browsers that can't
  decode HEIC. Now rejected up front with an actual message telling you
  how to convert it (Preview → File → Export → JPEG).
- **A byte-level truncation bug** in the multipart parser: any uploaded
  file whose *own last byte* happened to be `\r` or `\n` — a plain-text
  format like SVG saved by almost any editor, for instance — would get
  silently cut one byte short. Verified fixed with an SVG crafted to
  reproduce exactly this: byte-for-byte identical after the fix.
- **A race condition**: two uploads landing in the same instant that
  both sanitize to the same filename could silently overwrite one
  another, contradicting this file's own "never overwrites" promise.
  Fixed with an atomic create-if-absent write instead of a check-then-write;
  verified by firing two real concurrent uploads at the same name and
  confirming both survive under different filenames.

Verified end to end after the fixes, including the parts that already
worked before: a file actually lands in `assets/img/`, and a
maliciously crafted filename like `../../../etc/passwd` gets reduced to
a plain, safe name before it ever touches the filesystem.

## Automatic safety net

Every save checks that the ids/classes/fields `js/main.js` depends on
are still present (countdown, RSVP, lightbox, gallery). If something is
missing, the status line at the top of the editor flags it in yellow —
a warning, not a block: the save still happens, so you don't lose your
work while you figure out how to fix it.

## If you customize the site's structure yourself

If you add or rename elements that the countdown, RSVP form, or gallery
lightbox depend on, update the three lists at the top of
`editor/server.py` (`REQUIRED_IDS`, `REQUIRED_CLASSES`,
`REQUIRED_FIELDS`) to match — that's what powers the safety-net warning
above.
