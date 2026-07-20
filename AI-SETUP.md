# Step 1 — Get an AI assistant to do the technical part

**This is the first thing to do, before anything else.** Not because the
rest is hard, but because there's no reason for you to spend your
evenings on it.

The plan for this whole project:

```
   ┌──────────────────────────┐         ┌───────────────────────────┐
   │  Your AI assistant       │         │  You, in the editor       │
   │  (Claude Code / Codex)   │         │  (visual, click-and-drag) │
   ├──────────────────────────┤         ├───────────────────────────┤
   │  • installs everything   │         │  • your names, your words │
   │  • sets up the site      │         │  • colors, sizes, spacing │
   │  • publishes it online   │         │  • your photos            │
   │  • adds new sections     │  ◀────▶ │  • looking at it and      │
   │  • fixes what's broken   │         │    deciding what's wrong  │
   │  • anything technical    │         │  • checking it on a phone │
   └──────────────────────────┘         └───────────────────────────┘
         does the work                       makes the decisions
```

You are the art director. The assistant is the entire technical
department. That division is the point — and it's why you don't need to
learn git, or the terminal, or HTML, to end up with a site you're proud
of.

---

## Which one?

Either works. Both cost about the same, both are excellent at this.

| | Cost *(verified July 2026 — check current pricing)* | The tool |
|---|---|---|
| **Claude Pro** | ~$20/month | **Claude Code** |
| **ChatGPT Plus** | ~$20/month | **Codex** |

One month is plenty to finish a wedding site. Cancel afterwards if you
want — the site keeps running, it doesn't depend on the subscription.

**The $100–200/month tiers are not needed here.** Those are for people
writing software all day. Don't let anyone tell you otherwise.

Sources: [claude.com/pricing](https://claude.com/pricing) ·
[developers.openai.com/codex/pricing](https://developers.openai.com/codex/pricing)

---

## Setting up Claude Code

**The least technical route: the desktop app.** Claude Code comes as a
Mac and Windows app, and as a web app at
[claude.ai/code](https://claude.ai/code) — no terminal involved. If the
words "command line" make you tired, start there: install it, sign in
with your Claude account, and point it at your project folder.

**If you're comfortable in the Terminal** (or your assistant tells you
to), the command-line version is one line:

```bash
npm install -g @anthropic-ai/claude-code
```

Then, from inside your project folder:

```bash
claude
```

It'll walk you through signing in the first time.

## Setting up Codex

```bash
npm install -g @openai/codex
```

Then, from inside your project folder:

```bash
codex
```

Same idea: it asks you to sign in with your ChatGPT account on first run.

> **Both of those need Node.js first.** If `npm` isn't recognized,
> install the **LTS** version from [nodejs.org](https://nodejs.org) — a
> normal installer, like any other app — then close and reopen the
> Terminal.
>
> Or: skip it, use the Claude Code desktop app, and let the assistant
> tell you what it needs.

---

## The very first thing to ask it

Once it's running **in your project folder**, this single message gets
you from nothing to a live website:

> I've just copied a wedding invite starter kit into this folder. I'm not
> a developer — please do the technical setup for me.
>
> Read the README.md first so you understand what this project is. Then:
> check I have everything installed that this needs, get the site
> publishing to GitHub Pages, and tell me the web address when it's live.
>
> Explain each step in plain language as you go, and ask me before
> anything that can't be undone.

That's it. That's the setup. It will install what's missing, handle git,
turn on hosting, and hand you a URL.

**Then, and only then**, you open the visual editor and start making it
yours — see **[HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md)**.

---

## How to get good results

These are the habits that make the difference between "the AI messed up
my site" and "I finished it in a weekend."

**1. Point it at file names.**
"In `index.html` and `css/style.css`…" — vague requests get vague
results. Naming the file focuses it immediately.

**2. Describe the outcome, not the method.**
✅ *"Make the whole thing feel warmer — less black-tie, more sunny
garden party."*
❌ *"Change font-family to Playfair and set the background to #FDF6E3."*

You're the art director. Directors describe what they want to see, not
which knobs to turn. The second version also caps the result at whatever
you already knew to ask for.

**3. Tell it to look at the result.**
> "Run the site locally, look at it on a phone-sized screen, and show
> me a screenshot before you change anything else."

These assistants can start the site, open a browser, and actually *see*
the page. An assistant that looks catches things an assistant that only
types will miss.

**4. Say what must not break.**
> "Don't change the countdown, the RSVP form, or the photo gallery —
> just the colors."

This project has moving parts (the countdown timer, the RSVP form, the
photo lightbox) that live in `js/main.js`. Naming them as off-limits is
cheap insurance.

**5. Point it at this project's own documentation.**
> "Read `editor/README.md` before you touch the CSS — it documents
> constraints specific to this project."

Those files were written partly *for* an AI assistant to read. There are
real, documented quirks in here (certain CSS shorthand properties get
dropped by the visual editor; the countdown depends on specific ids).
An assistant that's read those notes won't rediscover them the hard way
on your live site.

**6. Work in small steps, and look after each one.**
One change → look at it → next change. It's tempting to ask for ten
things at once; you'll get a better site asking for one thing ten times,
because you're steering after every step.

**7. Paste errors exactly as they appear.**
Whole message, unedited. This is where these tools genuinely shine —
an error that would cost you an evening of searching is often a
ten-second fix for them.

---

## Trust it to work. Verify the result.

Letting an assistant do the technical work does **not** mean clicking
"yes" without looking. You don't need to read code to verify well —
you need to check the things you're actually qualified to judge, which
happen to be the things that matter most:

- **Look at the site yourself** after each change. You'll spot "that
  doesn't look right" faster than any tool.
- **Check it on your actual phone**, not just a phone-sized window.
- **Ask it to explain what it did**, in plain words: *"explain that
  change as if I don't code."* If the explanation doesn't make sense to
  you, that's worth a follow-up question — not because it's necessarily
  wrong, but because you should understand your own website.
- **Ask to see before publishing**: *"show me first, don't publish yet."*
- **Test the RSVP form yourself**, by actually submitting one. This is
  the single most important thing on the site and the easiest to get
  subtly wrong.

**Your undo button is git**, and it's better than you'd expect. Every
published version is saved. If a change makes things worse, you can
always say:

> "That's worse — undo it and go back to how it was before."

and it can. Nothing here is one-way.

**One hard rule:** never paste passwords, credit card numbers, or
security tokens into a chat, and don't let an assistant put them in a
file. Legitimate setup (like signing into GitHub) happens in your own
browser, not by handing over a password.

---

## What to do when it gets stuck

It happens. Two things that reliably unstick it:

1. **Show it the evidence.** *"The site loads but there's no styling at
   all"* is more useful than *"it's broken."* Even better: *"here's the
   exact error message: [paste]"*.
2. **Let it look for itself.** *"Open the site and check the browser
   console for errors."* It can do that.

And if a whole approach turns out wrong: *"scrap that, let's go back to
the last working version and try something different."* Cheap to do,
and often faster than debugging a bad path.

---

## Where the assistant ends and you begin

Not everything should go to the assistant. Once the site is set up and
live, small visual changes are genuinely **faster to do yourself** in
the editor — you see the result instantly instead of describing it,
waiting, and looking.

That boundary — what's worth doing yourself, what's worth handing over,
and how far you can realistically push — is laid out with concrete
examples in
**[HOW-TO-USE-THE-EDITOR.md](HOW-TO-USE-THE-EDITOR.md#the-division-of-labor)**.

That's the next thing to read.
