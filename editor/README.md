# Local editor (GrapesJS) — how it works and its real limits

A visual editor that runs **on your own computer**: no account, no cloud,
no external service to sign up for — it's a local library (npm), not a
cloud product like Webstudio or Framer.

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
