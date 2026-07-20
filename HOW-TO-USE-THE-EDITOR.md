# How to use the visual editor

The complete guide to editing your site by dragging, clicking, and typing —
no code required. This covers **everything** the editor can do: text,
colors, fonts, spacing, photos, layout, and how to check your work on
mobile before you publish.

Every interaction described here was tested for real — not assumed —
against this exact toolset (`grapesjs@0.22.16`), on a MacBook Pro (M4,
16GB RAM, macOS 26.5). If your machine is a similar or newer Apple Silicon
Mac, this will run at least as smoothly.

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

---

## If something feels stuck

| Symptom | What's usually going on |
|---|---|
| Clicking in the canvas does nothing | Click precisely on the visible text/image, not the padding around it — or use the Layers panel instead |
| The Style panel is empty | Nothing is selected yet — click something first |
| A photo won't upload | Check the terminal running `server.py` for an error; confirm the file is actually an image (jpg/png/gif/webp/svg) |
| A change looks right but disappeared after Save | Check the status line for a yellow warning — it names exactly what's missing |
| The whole canvas looks unstyled | Hard-refresh the editor tab (`Cmd+Shift+R`) — occasionally the browser caches an old version of a file |
