# How to use the visual editor

This is where **you** work: clicking, typing, dragging, and deciding what
looks right. Your AI assistant handles everything technical — if you
haven't set one up yet, do that first:
**[AI-SETUP.md](AI-SETUP.md)**.

The editor itself is [GrapesJS](https://github.com/GrapesJS/grapesjs) —
free, open source, and running entirely on your own computer. No account,
no subscription, no company hosting your work-in-progress. It opens your
*actual* files, so what you see is genuinely the site, not a preview of
one.

Every interaction described here was tested for real — not assumed —
against this exact toolset (`grapesjs@0.22.16`), on a MacBook Pro (M4,
16GB RAM, macOS 26.5). If your machine is a similar or newer Apple Silicon
Mac, this will run at least as smoothly.

---

## The division of labor

The single most useful thing to understand about this whole project:

> **The editor is for taste. The assistant is for everything else.**

You use the editor because looking at something and thinking *"that's too
big"* is instant, and describing it in words is not. You use the
assistant because setting up hosting, writing a new section, or fixing a
mobile layout bug is work you have no reason to learn.

### Do it yourself, in the editor

Fast, visual, immediate — describing these to an assistant is slower than
just doing them:

- Your names, your story, your dates, venue names
- Text sizes, weights, letter spacing
- Colors of text and most backgrounds
- Spacing and padding — nudging until it breathes right
- Swapping photos in the gallery
- Reordering sections, duplicating a schedule event
- Checking how it all looks on a phone

### Hand it to your assistant

Either the editor genuinely can't, or it'd be tedious:

| What | Why not the editor |
|---|---|
| **Changing the typefaces** | The font dropdown only offers generic system fonts — the four Google Fonts this design uses aren't in it (see [the note below](#changing-colors-fonts-and-spacing--the-style-manager)) |
| **Border/background color on buttons, chips, the divider, the footer** | 7 specific rules in this project use a CSS shorthand the editor drops on import — documented precisely in [`editor/README.md`](editor/README.md) |
| **Anything in `js/main.js`** | The countdown, the RSVP form, the photo lightbox. The editor deliberately doesn't touch this file |
| **Anything in the `<head>`** | Page title, the WhatsApp link preview, fonts loaded |
| **A genuinely new section** | The editor's blocks are generic; an assistant writes one that matches this design's structure and spacing |
| **"It looks wrong only on mobile"** | Needs a media query — an assistant fixes this in a sentence |
| **Publishing, hosting, domains, git** | All of it |

### The rule of thumb

**Try it in the editor first. If it fights you for more than a minute,
stop and ask.** That minute is the whole heuristic — you'll be right
almost every time, and you're never stuck for long either way.

---

## Starting it

```bash
cd editor
npm install    # first time only, ~2 seconds
cd ..
python3 editor/server.py
```

Open **<http://127.0.0.1:8767/editor/>**. It loads your actual `index.html`
and `css/style.css` — not a copy — so anything you see is the real site.

---

## The interface, in one screenshot's worth of words

```
┌─────────────────────────────────────────────────────────────┐
│  Local editor   — status message —          [Save to project]│ ← top bar
├─────────────────────────────────────────────────────────────┤
│ [🖥][▭][📱]      [⛶][👁][⛶][</>][↶][↷][⬇⚠️][🗑⚠️]   [🖌][⚙][▤][➕]│ ← toolbar
│                                     ⚠️ = not what it looks like, see below      │
├───────────────────────────────────────────────────┬─────────┤
│                                                     │  right  │
│                  the canvas —                      │  panel  │
│                  your actual site,                 │ (varies │
│                  live and editable                 │  by     │
│                                                     │  icon)  │
└─────────────────────────────────────────────────────┴─────────┘
```

**Top-left icons** — switch the canvas preview width: Desktop, Tablet
(770px), Mobile (320px — a phone in portrait, which is what most guests
will actually use). Use these to check your layout before publishing.

**Toolbar icons**, left to right — checked against exactly what each one
is wired to do, since two of them are easy to mistake for the opposite
of what they are:

| Icon | Does | |
|---|---|---|
| grid | Toggle component outlines on/off | |
| eye | Preview (hides all editor chrome) | |
| ⛶ | Fullscreen | |
| `</>` | **View code** — see [below](#checking-your-work) | |
| ↶ | Undo | |
| ↷ | Redo | |
| ⬇ (down arrow into tray) | ⚠️ **Import — NOT export.** Opens a code-paste box; whatever you put there **replaces the entire canvas**. Don't click this expecting a download. | |
| 🗑 | ⚠️ **Clears the whole canvas — NOT "delete selected."** Asks for confirmation first, but confirming empties the entire page, not just whatever you have selected. For deleting one element, use the small trash icon in that element's own floating toolbar (below) instead. | |

> Both of those last two look at a glance like they should be safe,
> ordinary actions — "there's probably an export button" and "the trash
> icon deletes what I picked" are reasonable guesses, and both are
> wrong here. If you're not trying to start over from a blank page,
> leave both alone.

**Right-side panel switcher** — four icons that change what the panel
shows:

| Icon | Panel | What it's for |
|---|---|---|
| 🖌 brush | **Style Manager** | Colors, fonts, spacing, size — anything visual |
| ⚙ gear | **Settings** | Element-specific fields: alt text on photos, link addresses |
| ▤ stack | **Layers** | The whole page as a tree — an alternative way to select things |
| ➕ plus | **Blocks** | Drag-in new pieces: a link, a quote, a text section |

---

## Selecting something to edit

**Click on it** in the canvas. A blue outline appears around it, and a
small floating toolbar shows up above it:

```
↑  ⊹  ⧉  🗑
select   move   duplicate   delete
parent
```

The right panel switches to show that element's style.

> **If a click doesn't seem to do anything:** click directly on a letter
> of the text itself, not the empty space around it — text elements are
> only as "wide" as their actual content. If you're trying to select a
> whole section (like the cover, or one event in the schedule) rather
> than a single piece of text inside it, the **Layers panel** (▤ icon)
> is often easier: click "Header" there to select the entire cover
> section at once, without having to find an empty spot to click in the
> canvas.

---

## Editing text

**Double-click** any text to start typing directly in the canvas — the
same as editing a Google Doc. A small formatting toolbar appears above
it (bold, italic, underline, strikethrough, link). Click anywhere else
to stop editing; your change is saved into the page immediately (not to
disk yet — that's the separate "Save to project" step, see below).

**Worked example — changing the names on the cover:**

1. Double-click "EMMA" in the big heading.
2. Select the text (drag across it, or `Cmd+A` while inside it) and type
   your own name.
3. Click elsewhere to stop editing.
4. Repeat for the other name and the date underneath.

---

## Changing colors, fonts, and spacing — the Style Manager

Select anything, then click the 🖌 **brush icon** if the panel isn't
already showing styles. Six sections, each one collapsed by default —
click a section name to open it:

- **General** — how the element sits in the layout (display, float, position)
- **Flex** — direction, wrap, alignment, order — only relevant if the
  element is itself a flex container or a flex child
- **Dimension** — width, height, margin, padding
- **Typography** — font family, size, weight, letter spacing, **color**,
  line height, text alignment
- **Decorations** — background color, border, border radius, box shadow
- **Extra** — opacity, transitions, transforms

To change a color: open **Typography** (for text) or **Decorations**
(for backgrounds/borders), find **Color** / **Background color**, and
click the swatch to pick one, or type a value directly (a hex code like
`#2e2e2b`, or a name like `steelblue`).

> **One real limitation, worth knowing before you touch fonts.** The
> **Font family** dropdown only lists generic system fonts (Arial,
> Georgia, Times New Roman, and a dozen others) — it does **not** include
> the four Google Fonts this design actually uses (Cormorant Garamond,
> Julius Sans One, Karla, Pinyon Script), and it can't be typed into
> freely. In practice: **leave Font family alone** — the existing
> pairing is what gives the site its character, and font size, weight,
> letter spacing, and color all work perfectly through this same panel
> without touching it. If you do want to swap a typeface, that's a job
> for the **code view** below, or for an AI assistant.

**A safety detail worth knowing:** when you change a style, the editor
creates a small, specific rule just for that one element — it does not
rewrite the shared style every heading or button uses. Changing this
one event's time doesn't affect the other two.

---

## Swapping photos

**Double-click any photo** in the gallery (or the cover, if you add one
there). A "Select Image" window opens:

- **Drag a file in, or click to browse** — uploads it and saves a real
  file into `assets/img/` (verified: it does not embed the photo as a
  giant block of text inside your HTML, which is what this editor would
  do by default without the small upload helper already wired up in this
  kit — see `editor/README.md` if you're curious how).
- **Or paste a URL** in the field at top and click **Add image** — for a
  photo already hosted somewhere else.

Click the new thumbnail to apply it. The **Alt** field (in the ⚙
Settings panel, with the photo selected) is its description for screen
readers and for when the image fails to load — update it to match.

---

## Rearranging and adding sections

- **Layers panel** (▤ icon): drag rows up/down to reorder; click the eye
  icon to hide something without deleting it.
- **Blocks panel** (➕ icon): drag a new block (Link, Quote, Text
  section) directly into the canvas where you want it.
- The floating toolbar's **duplicate** icon (⧉) is the fastest way to
  add a fourth schedule event: duplicate the third one, then edit the
  copy.

---

## Checking your work

- **Device icons** (top-left): preview at Tablet and Mobile widths —
  most guests will open the link on a phone, so check there before
  anything else.
- **Preview** (eye icon): hides all editor chrome so you see exactly
  what a guest would.
- **View code** (`</>` icon): shows the live HTML and CSS side by side.
  You don't need to read it to use this tool, but it's the fastest way
  to double-check exactly what a change did — or to hand a specific
  snippet to an AI assistant if you want help with something.
- **Undo / redo** (↶ / ↷ icons, or `Cmd+Z` / `Cmd+Shift+Z`): work as
  expected, for any change made in the canvas.

---

## Saving

**"Save to project"** (top right) writes everything to your actual
files. The status line tells you what happened:

- **Green — "Saved."** Everything's fine.
- **Yellow — a warning listing specific ids/classes.** Something the
  countdown, RSVP form, or gallery lightbox depends on went missing —
  usually from deleting a whole section rather than just its text. The
  save still happens (you won't lose work), but re-check that part of
  the page.
- **Red — an error.** Something went wrong on the server side; the
  message says what.

Saving **never publishes anything** — see the main [README](README.md#going-live)
for that separate, deliberate step.

Once you've saved and you're happy, publishing is one sentence to your
assistant: *"publish it."*

---

## How far to push your assistant

Most people ask for far less than they could get. The limit isn't what
these tools can build — it's what you think to ask for. So here's a
concrete ladder, from "obviously yes" to "you probably didn't realize
this was on the table."

### The things the editor can't do

One sentence each. These are the everyday handoffs:

> "Change the typeface pairing to something warmer and more romantic —
> keep it to two Google Fonts, and show me two options before you pick."

> "The 'Show location' buttons should have a soft gold border instead of
> black. Note that `editor/README.md` explains why the visual editor
> can't do this one."

> "On my phone the schedule times feel cramped against the venue names.
> Fix the spacing on mobile only — don't change the desktop layout."

### New things the site doesn't have yet

A paragraph each, and genuinely useful for a wedding:

> "Add an **'Add to calendar'** button under the ceremony time, so guests
> can save it to their phone in one tap."

> "Add a **travel and accommodation** section after the schedule: two or
> three hotel suggestions with links, and a note about parking. Match the
> existing design exactly."

> "Change the RSVP so responses land in a **spreadsheet** instead of my
> email. Walk me through whatever I need to sign up for — the README
> mentions Formspree and Tally as options."

> "Add a **dietary requirements** field and a **song request** field to
> the RSVP form."

> "Put a **soft password page** in front of the site — nothing serious,
> just a word printed on the paper invitations, so it isn't wide open to
> anyone who finds the link."

> "Some of our guests don't speak English. Add a **language toggle** with
> a translated version of all the text."

### The ambitious end

This is where it stops feeling like a tool and starts feeling like
having a designer on call:

> "I've decided black-tie is wrong for us. **Redesign the whole thing**
> as a warm Mediterranean garden wedding — terracotta, olive, hand-drawn
> feel. Keep every section and all the working parts, change the entire
> visual language. Show me the cover first before doing the rest."

That works because the design lives almost entirely in one stylesheet.
A total aesthetic change is a genuinely reasonable request here, and it
costs you a conversation rather than a rebuild.

Others worth knowing you can ask for:

> "Go through the whole site for **accessibility** — colour contrast,
> alt text, keyboard navigation — and fix what's wrong. Explain what you
> found in plain language."

> "Our photos are slowing the page down. **Optimise them** and make the
> gallery load faster, without visibly reducing quality."

> "Act as a **picky design critic** for a moment. Look at the live site
> on both desktop and mobile and tell me the five things you'd change,
> ranked. Don't change anything yet — just tell me."

That last one is underrated. These assistants are genuinely good at
critique, and it costs you nothing to ask before you commit.

### So where's the actual ceiling?

Not where you'd expect. For a static site like this, an assistant can
realistically build essentially anything you can describe.

The real constraints are:

1. **Your ability to describe what you want.** Vague in, vague out. This
   is why the editor matters — it's often faster to *show* yourself what
   you want by trying it, than to find words for it.
2. **Your ability to tell whether it's right.** Which is why every
   ambitious request should end with *"…and show me."*
3. **Genuinely dynamic features.** Anything needing a real server —
   user accounts, a live seating-chart editor, payments. Possible, but
   it stops being a free static site. For a wedding invite you almost
   certainly don't want to cross that line.

**A practical ceiling worth respecting:** don't chain five ambitious
requests without looking in between. Not because it'll break, but
because if something goes subtly wrong on step two, you want to notice
before it's baked into steps three through five.

---

## If something feels stuck

| Symptom | What's usually going on |
|---|---|
| Clicking in the canvas does nothing | Click precisely on the visible text/image, not the padding around it — or use the Layers panel instead |
| The Style panel is empty | Nothing is selected yet — click something first |
| A photo won't upload | Check the terminal running `server.py` for an error; confirm the file is actually an image (jpg/png/gif/webp/svg) |
| A change looks right but disappeared after Save | Check the status line for a yellow warning — it names exactly what's missing |
| The whole canvas looks unstyled | Hard-refresh the editor tab (`Cmd+Shift+R`) — occasionally the browser caches an old version of a file |
