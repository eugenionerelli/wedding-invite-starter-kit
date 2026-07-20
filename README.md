# Wedding Invite — Starter Kit

A one-page wedding invite site, in a "black tie" style: cover with a
monogram, your story, a countdown, the day's schedule with Google Maps
buttons, a photo gallery, and an RSVP form.

**Free hosting, forever.** No database, no backend, no build step. Just
files you can open and edit, made to run on GitHub Pages or Cloudflare
Pages.

**Live demo of this exact kit:** you're looking at the placeholder
content (Emma & James) — see [Quick start](#quick-start) below to make it
yours.

---

## 📝 The main thing: editing your site visually

This kit includes a **local visual editor** — click on things, type,
drag, done. No account, no cloud service, nothing to sign up for: it
runs entirely on your own computer and edits your real files directly.

**→ [HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md) — the complete,
tested guide.** Selecting things, editing text, changing colors and
fonts, swapping photos, checking mobile, saving — all of it, with every
interaction verified against this exact toolset before being written
down, not assumed.

Everything else in this README (accounts, publishing, going live) is
the supporting setup around that one guide.

---

## What's in here

```
.
├── HOW-TO-USE-THE-EDITOR.md → the complete visual-editing guide — start here
├── index.html        → all the content (names, text, times, venues, photos)
├── css/style.css      → colors, fonts, spacing (the design)
├── css/edited.css      → written by the local editor — don't edit by hand
├── js/main.js         → countdown, animations, RSVP form
├── assets/img/        → (empty) put your own photos here
├── editor/            → local visual editor (GrapesJS) — no account needed
│   └── README.md        → technical reference: how it works, real limitations
└── scripts/
    └── publish.sh       → commit + push, with a confirmation step
```

---

## Prerequisites

### Accounts (free, 10 minutes)

- **GitHub** → [github.com/signup](https://github.com/signup). Required —
  this is where your copy of the site lives and where free hosting comes
  from. Note the username you choose, it ends up in your site's address.
- **Cloudflare** *(optional)* → [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up) —
  only if you pick Cloudflare Pages over GitHub Pages in
  [Going live](#going-live).
- **Claude or ChatGPT** *(optional)* — only if you want an AI assistant's
  help, see [Using an AI assistant](#using-an-ai-assistant-optional).

### Tools on your computer

Only needed for the *Quick start* steps below (cloning, previewing, and
the local editor). If that sounds unfamiliar: it's normal, everyone
starts there, and each check below takes under a minute.

The **Terminal** is the app where you type these commands. On a Mac:
press `Cmd + Space`, type "Terminal", press Enter. It looks intimidating
but you're mostly copying and pasting — nothing is permanent or
dangerous in what follows.

- **Git** — moves your code to GitHub. Check with `git --version`; if
  it's missing, a Mac will offer to install it (accept), or get it from
  [git-scm.com](https://git-scm.com/downloads). Then, once, introduce
  yourself: `git config --global user.name "Your Name"` and
  `git config --global user.email "you@email.com"`.
- **Python 3** — runs the local preview server and the visual editor.
  Check with `python3 --version`. **Already installed on every Mac.** On
  Windows, get it from [python.org/downloads](https://python.org/downloads)
  — during setup, tick **"Add python.exe to PATH"**, easy to miss and the
  most common cause of a "command not found" error afterward.
- **Node.js** *(only for the local visual editor)* — check with
  `node --version`; `v20` or higher is fine. If missing, download the
  **LTS** version from [nodejs.org](https://nodejs.org) and install it —
  a normal installer, like any other app.

If any command above says "command not found" after installing, close
and reopen the Terminal (it doesn't always notice new software right
away).

---

## Quick start

1. **Get your own copy.** Signed into your GitHub account, on this repo's
   page click the green **"Use this template"** button (not "Fork" —
   that keeps you linked to the original; a template gives you a clean,
   independent copy). Name it whatever you like.

2. **Clone it to your computer:**

   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

3. **Look at it right away**, before changing anything:

   ```bash
   python3 -m http.server 8000
   ```

   Open <http://localhost:8000> — that's the starting point.

4. **Edit it.** Two ways, pick whichever suits you (details below):
   - **Visually**, in the local editor (recommended — needs Node.js from
     [Prerequisites](#prerequisites) above, nothing else)
   - **By hand**, in `index.html` / `css/style.css` — every file has
     `CUSTOMIZE` comments marking what to change

5. **Publish it** — see [Going live](#going-live).

That's the whole loop. Everything past this point is detail and options.

---

## Editing visually — the local editor

```bash
cd editor
npm install    # first time only
cd ..
python3 editor/server.py
```

Open **<http://127.0.0.1:8767/editor/>**. It's the free, open-source
library [GrapesJS](https://github.com/GrapesJS/grapesjs), loading your
actual files, running entirely on your own computer.

**→ Full guide: [HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md)** —
how to select things, edit text, change colors and fonts, swap photos,
check mobile, and what the save button actually does (short version:
writes local files, never publishes — that stays a separate, deliberate
step below).

---

## Editing by hand

Every file that has content to customize is marked with a `CUSTOMIZE`
comment: names, date, your story, the schedule, RSVP deadline. Search
for that word in your editor and you'll find every spot.

### The Google Maps buttons

The part guests actually use. In `index.html`, each venue has a line like
this — the link is the part between `href="` and the next `"`:

```html
<a class="btn-location" href="https://www.google.com/maps/search/?api=1&query=Kew+Gardens+London" target="_blank" rel="noopener">Show location</a>
```

Replace everything between those two quotes with your own link. Two ways
to get one:

1. **Easiest** — search the venue on
   [maps.google.com](https://maps.google.com) → **Share** → **Copy
   link**, paste it in place of the URL above.
2. **By hand** — this format always works and never expires:
   `https://www.google.com/maps/search/?api=1&query=VENUE+NAME+CITY`
   (spaces become `+`).

### Photos

The six gallery photos are Unsplash placeholders (free license). To use
your own: put the files in `assets/img/` and change the `src` in
`index.html`, e.g. `src="assets/img/engagement.jpg"`. Export them around
1600px wide and under 500KB each so the page stays fast (on a Mac:
Preview → Tools → Adjust Size).

### The RSVP form

The site is static, so by default the form opens the guest's email app
with the RSVP pre-written (the address is `COUPLE_EMAIL` in
`js/main.js`). It works everywhere, but asks one extra step of the guest.

Free alternatives that collect responses automatically:

- **[Formspree](https://formspree.io)** (50 submissions/month free):
  create a form, you get a URL like `https://formspree.io/f/abcd1234`;
  add `action="that URL"` and `method="POST"` to the `<form id="rsvp-form">`
  tag in `index.html`. Then in `js/main.js`, delete everything between the
  comments `/* MAILTO BLOCK — START */` and `/* MAILTO BLOCK — END */`
  (search for those two lines — they mark exactly what to remove, nothing
  else in the file needs to change). Responses land in your inbox.
- **Google Form / [Tally](https://tally.so)**: build the form there and
  either link to it with a button, or embed it with an `<iframe>`. No
  code, responses land in a spreadsheet.

### Colors and fonts

At the top of `css/style.css` (in `:root`) are the palette and fonts.
Fonts are free from [Google Fonts](https://fonts.google.com) — to
change them, pick new ones there, swap the `<link>` in `index.html`, and
update the names in `style.css`.

### Privacy

- `index.html` has `<meta name="robots" content="noindex">`: it won't
  show up on Google. Remove that line if you want the opposite.
- The site is still **public to anyone with the link** — keep that in
  mind for what you write (skip home addresses, phone numbers).

---

## Going live

### Option A — Cloudflare Pages (simplest, nicest URL)

No commands needed.

1. [dash.cloudflare.com](https://dash.cloudflare.com) (free account) →
   **Workers & Pages**
2. **Create** → **Pages** tab → **Upload assets**
3. Project name: whatever you want in the address (e.g. `emmaandjames`)
4. **Drag in the whole project folder**
5. Done — live at `https://emmaandjames.pages.dev`

To update: re-drag the folder from the same page. Or connect it to your
GitHub repo instead (**Connect to Git**) so every push deploys
automatically — same idea as Option B below, just on Cloudflare.

### Option B — GitHub Pages

If you used "Use this template" your repo already exists on GitHub, so:

1. On the repo page: **Settings → Pages → Build and deployment** →
   Source: *Deploy from a branch* → Branch `main`, folder `/ (root)` →
   **Save**.
2. After about a minute, it's live at
   `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`.

From then on:

```bash
./scripts/publish.sh "Updated the schedule"
```

commits, pushes, and the site redeploys on its own in about a minute.
The script shows you what changed and asks before doing anything.

> **The fix that saves an evening.** If the site ever loads with **no
> styling at all**, create an empty file called `.nojekyll` in the
> project's root folder and publish again — GitHub silently drops any
> folder starting with `_`, which some tools generate.
> `touch .nojekyll`

---

## Before you send it to guests

- [ ] Opened it **on a phone**, not just a laptop
- [ ] Every Maps button goes to the right place
- [ ] The RSVP form **actually reaches you** — send yourself a test one
- [ ] Names, dates, and times checked twice (a wrong date is the classic slip)
- [ ] Sent the link to someone outside the wedding, to see if it makes
      sense with zero context
- [ ] No home address or private phone number anywhere on the page
- [ ] `noindex` is still in place, unless you want it findable on Google

---

## A domain of your own (optional)

`emmaandjames.com` costs roughly $10–15/year from a registrar like
[Cloudflare](https://domains.cloudflare.com), and connects free to
either hosting option above (on Cloudflare Pages: project → *Custom
domains*; on GitHub Pages: repo Settings → Pages → *Custom domain*).

---

## Using an AI assistant (optional)

Everything above works with zero AI involvement — every step is plain
files and copy-paste commands. If you'd rather describe changes in
words and have something else make them, either works well with this
project because it's just files and standard tools, nothing proprietary:

| | Cost (verified July 2026 — check current pricing) | Includes |
|---|---|---|
| **Claude Pro** | ~$20/month | Claude Code |
| **ChatGPT Plus** | ~$20/month | Codex |

One month is enough to finish a site like this — cancel after.
Sources: [claude.com/pricing](https://claude.com/pricing) ·
[developers.openai.com/codex/pricing](https://developers.openai.com/codex/pricing).
**Higher tiers ($100–200/month) are not needed** for a project this size.

---

## An alternative: Webstudio

[Webstudio](https://webstudio.is) is a different kind of tool worth
knowing about: a richer drag-and-drop canvas with its own hosting-free
export, and — unusually — an official way for an AI coding assistant to
operate it directly (`webstudio connect claude` / `webstudio connect
codex`). The tradeoff versus the local editor in this kit: **Webstudio
can't import an existing site** — you rebuild it from a blank canvas
inside their tool, rather than editing these files directly. It also
needs a free account (the free "Hobby" tier is genuinely enough — no
paid plan required, verified against their pricing page).

Not set up in this starter kit, since the local editor above already
covers "edit visually, no account" without the rebuild-from-scratch
step. If you want to try it anyway, the mechanics are the same
regardless of whose site you start from — search Webstudio's own docs
for `webstudio connect` and `webstudio mcp`.

---

## If you get stuck

| Problem | Usual cause |
|---|---|
| "command not found" for `git`/`python3`/`node` | It's not installed, or (Windows) wasn't added to PATH — see [Prerequisites](#prerequisites), then close and reopen the Terminal |
| Site with no styling after publishing | Missing `.nojekyll` — see above |
| "Permission denied" pushing to GitHub | Wrong username, or GitHub needs a **personal access token** instead of your password since 2021 — create one at [github.com/settings/tokens](https://github.com/settings/tokens) → *Generate new token (classic)* → tick `repo` → paste it in place of your password when asked |
| Local editor shows a blank canvas | Check the terminal running `server.py` for an error; make sure `npm install` finished inside `editor/` |
| A save "succeeded" but something stopped working | Read the warning in the editor's status bar — it names exactly which id/class went missing |
| Countdown stuck at "–" | `WEDDING_DATE` in `js/main.js` is malformed, or in the past |
| Blank page | The main file must be named exactly `index.html` |

If none of that explains it, and you're using an AI assistant: paste
**the exact error message** — that's where they're most useful.

---

## Credits

Design and tooling originally built for a different couple's wedding
site, then turned into this generic, reusable kit. Fonts are free from
Google Fonts (Cormorant Garamond, Julius Sans One, Karla, Pinyon
Script). Placeholder photos are free-license from Unsplash — replace
them with your own before sending this to anyone.

Congratulations. 🥂
