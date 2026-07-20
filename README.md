# Wedding Invite — Starter Kit

A one-page wedding invite site, in a "black tie" style: cover with a
monogram, your story, a countdown, the day's schedule with Google Maps
buttons, a photo gallery, and an RSVP form.

**Free hosting, forever.** No database, no backend, no build step. Just
files you can open and edit, made to run on GitHub Pages or Cloudflare
Pages.

**No coding required — and no learning to code either.** An AI assistant
does the technical work; you use a visual editor for the design. Two
guides, in order: **[AI-SETUP.md](AI-SETUP.md)** then
**[HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md)**.

The placeholder content you'll see (Emma & James) is there to be
replaced with yours.

---

## How this works: two steps, in this order

**You are not going to learn web development to do this.** The approach
here is deliberate: an AI assistant does every technical thing, and you
spend your time on the part that actually needs you — deciding what it
should look like.

### 1️⃣ Set up an AI assistant → **[AI-SETUP.md](AI-SETUP.md)**

Claude Code or Codex (~$20/month, one month is enough). It installs
what's missing, sets up the site, publishes it online, and handles
anything technical you hit later. There's a copy-paste first message in
that guide that takes you from zero to a live website.

### 2️⃣ Make it yours → **[HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md)**

A **visual editor that runs on your own computer** — click, type, drag.
Free and open source ([GrapesJS](https://github.com/GrapesJS/grapesjs)),
no account, no subscription, editing your real files directly. This is
where you do the design.

That guide also covers **how far you can push your assistant** — with
concrete examples, because most people ask for far less than they could
get.

> Everything below is reference material. If you've read those two
> guides, you can mostly ignore the rest — or better, point your
> assistant at it when a question comes up.

---

## What's in here

```
.
├── AI-SETUP.md              → step 1: your AI assistant does the technical part
├── HOW-TO-USE-THE-EDITOR.md → step 2: the visual editor, and how far to push AI
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

## Quick start

1. **Get your own copy.** Signed into your GitHub account, on this repo's
   page click the green **"Use this template"** button (not "Fork" —
   that keeps you linked to the original; a template gives you a clean,
   independent copy). Name it whatever you like.

2. **Set up your AI assistant** → **[AI-SETUP.md](AI-SETUP.md)**, then
   hand it the copy-paste first message in that guide. It downloads the
   project, installs anything missing, publishes the site, and gives you
   the web address.

3. **Open the visual editor and make it yours** →
   **[HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md)**.

4. **Say "publish it"** whenever you want the live site updated.

That's the whole loop.

---

## Reference: what this actually needs

**You can skip this section.** Your assistant checks and installs all of
it in step 2 — it's here so you know what's on your machine, and for the
occasional moment when something says "command not found."

- **A GitHub account** → [github.com/signup](https://github.com/signup).
  Free. This is where your site lives and where the free hosting comes
  from; your username ends up in the web address.
- **Git** — moves your files to GitHub. `git --version` to check; a Mac
  offers to install it, or [git-scm.com](https://git-scm.com/downloads).
- **Python 3** — runs the local preview and the visual editor.
  `python3 --version` to check. **Already on every Mac.** On Windows,
  from [python.org/downloads](https://python.org/downloads) — tick
  **"Add python.exe to PATH"** during setup, which is easy to miss and
  the usual cause of "command not found" afterwards.
- **Node.js** — needed by the visual editor and by the assistants
  themselves. `node --version`; v20 or higher. Otherwise the **LTS**
  installer from [nodejs.org](https://nodejs.org).

> After installing anything, **close and reopen the Terminal** — it
> doesn't always notice new software right away.

### Running things by hand, if you'd rather

```bash
python3 -m http.server 8000     # preview the site → localhost:8000

cd editor && npm install && cd ..   # once
python3 editor/server.py            # the visual editor → 127.0.0.1:8767/editor/
```

---

## Reference: how the pieces work

**Also skippable.** This is the "what's under the hood" section — useful
if you're curious, and useful to point your assistant at
(*"the README explains the RSVP options, have a look"*). Every file has
`CUSTOMIZE` comments marking the spots that are meant to be changed.

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

> **Or just say "publish it."** Your assistant does all of this — it's
> exactly the kind of fiddly, one-time setup worth handing over. What
> follows is here so you know what's happening, and for the day you want
> to do it yourself.

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

## Why this particular toolchain

In case you're wondering whether there's something better out there —
these were the alternatives, and why they didn't make the cut:

- **[GrapesJS](https://github.com/GrapesJS/grapesjs)** *(what this kit
  uses)* — open source, free forever, runs on your own machine, and
  crucially **edits an existing site** rather than making you rebuild it.
  Nobody else's servers hold your work.
- **Webstudio** — a genuinely nicer canvas, and free to use. But it
  **can't import an existing site**: you'd rebuild this design from a
  blank page inside their tool, then export it back out. Worth a look if
  you ever start something from scratch; not worth it here.
- **Framer / Webflow** — polished, and popular for good reason, but
  built around their own paid hosting. Getting a site *out* of them and
  onto free hosting ranges from awkward to impossible.

The deciding factor was ownership: this kit is plain HTML and CSS, so
your assistant can change absolutely anything in it, and no company can
change the terms on a website you've already sent to two hundred people.

---

## If you get stuck

| Problem | Usual cause |
|---|---|
| "command not found" for `git`/`python3`/`node` | It's not installed, or (Windows) wasn't added to PATH — see [what this actually needs](#reference-what-this-actually-needs), then close and reopen the Terminal |
| Site with no styling after publishing | Missing `.nojekyll` — see above |
| "Permission denied" pushing to GitHub | Wrong username, or GitHub needs a **personal access token** instead of your password since 2021 — create one at [github.com/settings/tokens](https://github.com/settings/tokens) → *Generate new token (classic)* → tick `repo` → paste it in place of your password when asked |
| Local editor shows a blank canvas | Check the terminal running `server.py` for an error; make sure `npm install` finished inside `editor/` |
| A save "succeeded" but something stopped working | Read the warning in the editor's status bar — it names exactly which id/class went missing |
| Countdown stuck at "–" | `WEDDING_DATE` in `js/main.js` is malformed, or in the past |
| Blank page | The main file must be named exactly `index.html` |

**Honestly, the fastest fix for any of these:** paste the exact error
message to your assistant and let it sort it out. That's precisely the
kind of thing it's good at, and precisely the kind of thing not worth
your evening.

---

## Credits

Design and tooling originally built for a different couple's wedding
site, then turned into this generic, reusable kit. Fonts are free from
Google Fonts (Cormorant Garamond, Julius Sans One, Karla, Pinyon
Script). Placeholder photos are free-license from Unsplash — replace
them with your own before sending this to anyone.

Congratulations. 🥂
