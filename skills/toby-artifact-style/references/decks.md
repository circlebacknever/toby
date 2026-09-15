# Toby Artifact decks

Load this file when you produce a slide deck. Build it as HTML for an inline artifact, which is the default for teaching, or as pptx for a downloadable file.

## Format selection

| Format | Use when |
|---|---|
| HTML deck (React `.jsx` artifact) | Teaching artifacts, reference modules, anything paired with personalized-teaching skill. This is the default format. |
| pptx | the user explicitly asks for a `.pptx` file, asks to download a deck, or asks for a deck for offline use. |

If unsure, build the HTML deck.

---

## Before you build this deck

Answer these questions before writing any slide.

1. **What is the deck doing?** Is it teaching a mechanism, summarizing evidence, building a reference, or stepping through a process? The answer determines density and opening structure.
2. **Composition mode.** Pick one from SKILL.md, different from the one used last time.
3. **Ink allocation.** Decide which slides use ink before you start. Section dividers, summaries, glossaries, formula slides, and decision slides are the slides that can use ink. Most slides are paper. Decks where most slides are ink are valid when the content makes more claims than it explains, but choose that mode on purpose.
4. **Opening pattern.** Pick from the options below. Not every deck starts with title → glossary.
5. **Interactivity plan.** Go through the planned slides one at a time, and for each one, ask whether a parameter governs the concept. If yes, pick an interaction type from the catalog below. Sliders are one option among many.

---

## Deck structure — title and end slides

Every Toby Artifact deck opens with a **title slide** and closes with an **end slide**. Both are sparse on purpose, because they come before and after the dense reference content. Between them come the cover/index, then the content, then the references.

```
01  Title           (paper, sparse, mark + giant topic)
02  Cover & index   (paper, dense TOC grid)
03–13  Content      (paper or ink, dense reference)
14  Fin             (ink, sparse, one closing claim)
```

---

## Shared slide content rules

These rules apply to both HTML and pptx output.

### One main claim per slide

Write the slide title as a plain, descriptive sentence that states the claim, and use the body to show the work. If two claims belong on a slide, split them.

- Pass: "Cache layer cut p95 from 312 ms to 184 ms."
- Fail: "Performance results."

### Two slide tones

Each slide uses one of the two tones below, chosen slide by slide.

**Paper (default)** — `#fdfaf1` background. Use paper for reading content such as tables, diagrams, definitions, worked steps, lists, and walkthroughs.

**Ink** — `#1a1c1f` background. Use ink to give authority to section dividers, glossaries, formula slides, summaries, and decision points. Body text on ink uses `#fdfaf1` for primary text and `#a8a39a` for muted text.

### Information density

Decks use the reference-deck system, so they are written like a manual.

A dense slide has multiple cards, several key-value pairs, and tables. It should have enough content for 30–45 seconds of reading.

Not every slide needs to be dense. A slide presenting a single derivation or worked example can have more white space. Match density to how hard the content is to follow.

### Slide id (footer)

The slide id is right-aligned in muted mono text, in this format:

```
XX / NN · R-XX.X · LABEL
```

- `XX / NN` — current slide of total (1-indexed, zero-padded to 2 digits).
- `R-XX.X` — reference deck identifier, for example `R-04.2`.
- `LABEL` — short uppercase section name (`TITLE`, `INDEX`, `GLOSSARY`, `KEPLER`, `WORKED`, `APPLY`, `FIN`).

On ink slides, color the footer text with `--text-on-dark-muted` (`#a8a39a`).

---

## Opening patterns

Vary the opening structure across decks, and pick one of the patterns below for each deck.

**Title slide → cover/index (default for reference decks).** A sparse title slide with the toby mark and the topic in giant type comes first, followed by a dense TOC grid. It works for multi-section reference decks.

**Title → glossary.** A title slide with the logo primitive comes first, then a glossary slide that defines the terms before the mechanism. It works for concept-heavy topics where a reader cannot understand the content while its terms are undefined.

**Title → problem statement.** The title slide comes first, then an ink slide that states the problem or question the deck answers. It works for analysis, diagnosis, or decision-support decks.

**Title → worked example first.** The title slide comes first, followed immediately by a concrete worked example or case, and the mechanism explanation comes after. It works when intuition should come before formalism.

**Title → big fact.** The title slide comes first, then a single high-contrast slide that states the central numerical fact, measurement, or result. It works for evidence-led decks organized around their conclusion.

**No title slide.** Start directly with the first claim. Use a section eyebrow and the logo primitive in the footer, and skip the dedicated opening slide. It works for short reference cards (≤ 6 slides) or when the deck is one section of a longer session.

---

## Title slide pattern — sparse, paper-toned

The title slide opens the deck and identifies it. It shows the topic in big type, the toby wordmark and mark, and a faint decorative orbit lattice. It has no TOC, because the TOC goes on the cover/index slide.

```html
<section data-screen-label="01 Title">
  <!-- The Toby Artifact mark and wordmark go in the top-left. -->
  <div style="position: absolute; top: 64px; left: 80px; display: flex; align-items: center; gap: 16px;">
    <svg width="44" height="44" viewBox="0 0 64 64" fill="none">
      <circle cx="32" cy="32" r="28" stroke="var(--toby-ink)" stroke-width="1.4"/>
      <ellipse cx="32" cy="32" rx="28" ry="10" stroke="var(--toby-ink)" stroke-width="1.2" transform="rotate(-22 32 32)"/>
      <circle cx="56" cy="20" r="4" fill="var(--toby-accent)"/>
      <circle cx="32" cy="32" r="1.6" fill="var(--toby-ink)"/>
    </svg>
    <span style="font-family: var(--font-sans); font-size: 24px; font-weight: 600; letter-spacing: -0.012em;">toby</span>
  </div>

  <!-- A large, faint decorative orbit lattice goes on the far right. -->
  <div style="position: absolute; right: -120px; top: 50%; transform: translateY(-50%); opacity: 0.16;">
    <!-- Draw nested ellipses and a small center dot here. -->
  </div>

  <!-- The title block is aligned to the left. -->
  <div style="position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 0 80px;">
    <div class="ds-eyebrow" style="margin-bottom: 36px;">REFERENCE DECK · R-04.2</div>
    <h1 style="font-size: 128px; font-weight: 600; letter-spacing: -0.024em; line-height: 0.95; margin: 0; max-width: 1200px;">
      Orbital<br>mechanics.
    </h1>
    <p style="font-size: 22px; color: var(--text-secondary); max-width: 720px; margin: 48px 0 0; line-height: 1.55;">
      This deck is a working reference for orbits in classical Newtonian gravity. It has thirteen reading slides, with a unit on every value and each caveat beside the figure it qualifies.
    </p>
  </div>

  <!-- The bottom mono stripe has three captions. -->
  <div style="position: absolute; bottom: 80px; left: 80px; right: 80px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 48px;">
    <div>
      <div class="ds-eyebrow ds-eyebrow--quiet">CONTENTS</div>
      <div class="ds-mono" style="font-size: 13px; margin-top: 6px;">14 slides · 18 terms · 8 symbols</div>
    </div>
    <div>
      <div class="ds-eyebrow ds-eyebrow--quiet">CONVENTION</div>
      <div class="ds-mono" style="font-size: 13px; margin-top: 6px;">SI · J2000 · right-handed</div>
    </div>
    <div>
      <div class="ds-eyebrow ds-eyebrow--quiet">OWNER</div>
      <div class="ds-mono" style="font-size: 13px; margin-top: 6px;">Mission ops · Sayo</div>
    </div>
  </div>

  <div class="ds-footer"><span class="ds-footer__id">01 / 14 · R-04.2 · TITLE</span></div>
</section>
```

Build the title slide from these parts:
- **Toby Artifact mark + wordmark:** place them in the top-left. The mark consists of a hairline circle, two tilted ellipses, a single red dot, and a small centre dot. The wordmark is lowercase `toby` in Inter 600.
- **Big topic:** set it in 96–128px Inter 600 with tight negative letter-spacing, end it with a period, and align it left.
- **Faint decorative shape:** place it on the right at opacity ≤ 0.16, and pick it from `references/geometry.md`.
- **Bottom mono stripe:** show 2–3 captioned facts (contents, convention, owner) with small uppercase eyebrows and mono values.

---

## Cover / index slide pattern

The cover/index slide is a dense table of contents, laid out as a 4-column grid of cards that each name a section.

- Put an eyebrow, an h1, and a short paragraph describing the deck's scope at the top.
- Draw a `--bw-emph` (3px) coloured rule beneath the intro to separate the intro from the TOC.
- Lay out a 4×3 grid of cards, or a 3×4 grid if that fits the slide count better. Each card shows a section number (mono, muted), a section title, and one plain sentence (meta) saying what the section covers.
- Highlight new or signature slides by recolouring their section number to the relevant accent.
- Add a KV block at the bottom for scope, units, convention, and out-of-scope items.
- Place a geometry mark at decorative scale in the corner.

---

## Content slide patterns

These slide types all go between the cover and the end slide. Compose them freely, and use the components on slides.

| Slide type | Pattern |
|---|---|
| **Glossary / definition** | Use an ink tone and a dense 3-column grid of definition blocks. Each column has an eyebrow that labels the term cluster. |
| **Three-card / three-laws** | Place 3 cards side by side, and give each one an eyebrow, a section heading, an SVG diagram, a body, and a formula block. |
| **Comparison table** | Use a full-width table with mono cells. Group the cells with subhead rows or coloured family stripes. |
| **Formula slide** | Use an ink tone, with two formula cards side by side and a worked-examples table beneath them. |
| **Worked example** | Use the **Worked Example** component (three rows, info/watch/stable tinted). Pair it with a dark **Code Block** in a side column, and put a cross-check table below. |
| **Annotated diagram** | Use a card with `position: relative` and an SVG illustration inside. Overlay **Annotation Pins** numbered 1..n, and add a side legend that maps numbers to terms. |
| **KPI / stat snapshot** | Use an ink tone and a 4-column **Stat Grid** with cycling accent stripes. Pair it with rejected-alternative **Alerts** in a side column. |
| **Decision** | Use an ink tone with a Stat Grid at the top. Add an authority decision card that is dark, with a red top hairline and a pill in the corner. Show rejected alternatives as a stack of state-tinted Alerts. |
| **Section / quote / summary** | Use a sparse ink-toned slide with a single centered claim and a small eyebrow. A KV block beneath the claim is optional. |
| **References** | Use an ink tone and a reading list table where each entry has a cite block, a type, and a one-line description. Add an "up next" rail at the side. |

See `references/components.md` for the components referenced above.

---

## End slide pattern — sparse, ink-toned

The end slide closes the deck. It shows a single centred claim that states the most fundamental fact the deck taught. It has an ink background, a faint geometric backdrop, and the toby wordmark in the corner, with no content cards.

Build the end slide from these parts:
- **Ink-toned:** the background is `#1a1c1f`.
- **Toby Artifact mark + wordmark:** place them in the top-left, with `--text-on-dark` for the strokes and the red dot kept accent red.
- **One centred claim:** set it in 64–80px Inter 500 and end it with a period. A reader who remembers only the claim still has something useful.
- **Small eyebrow:** place it above the claim in `--toby-accent`. The end slide is one of the few places where consequence red appears without indicating risk, because the red marks the deck's close.
- **One-paragraph context:** place it beneath the claim at 16–17px in `--text-on-dark-muted`, and cite the source or historical origin of the claim.
- **Faint geometric backdrop:** place it behind the claim at opacity ≤ 0.12.
- **Bottom mono stripe:** show two captions, with the source line on the left and a "begin again at § 02" pointer on the right.
- **No content cards:** leave out KPIs, tables, and callouts, so the closing slide has only one sentence and a frame.

Example claim line: `Bound orbits are ellipses, and everything else about them is detail.`

---

## Title slide logo primitive

Each deck gets a per-artifact logo, which combines a hairline geometric primitive with one short lowercase Inter-600 word for the topic. A single red dot is the logo's only color.

**Pick the shape for the structure of the subject.** Examples:
- Network topology, graph, mesh → crosshair or grid lattice
- Recursive or nested structure → concentric squares or nested brackets
- Wave, signal, antenna, oscillation → arc or sinusoidal rail
- Decision tree, branching process → Y-fork or tree branches
- Time series, pipeline, queue → horizontal rail with tick marks
- Probability, distribution, uncertainty → bell outline or spread cone
- Rotation, orbit, cycle → partial orbit arc, because a closed circle reads as generic decoration.
- Matrix, table, grid data → small grid of squares, 3×3

Refuse these lazy defaults: an orbit for everything, a plain triangle, and a plain square. If you cannot explain why the shape fits the subject's structure, pick a different shape.

See `references/geometry.md` for the 20 named geometric marks and their purposes.

---

## Interactivity catalog

Choose the interaction type to fit the concept. Identify what the learner needs to falsify or explore, then pick the mechanism. 

**Make a slide interactive** when its concept has a trade-off between two effects or a parameter that governs a visual outcome. Interactivity also fits a process that the learner should be able to step through. If moving a control would let the learner falsify an intuition, build the control. Decorative motion does not meet this condition, so leave it out.

### Interaction types

**Slider (continuous parameter).** A scalar value governs a visual or numerical outcome. Use it when the relationship between input and output is the lesson: gain vs noise figure, sample size vs confidence interval, learning rate vs convergence. If the parameter is categorical, or if the gradient is not what matters, use a toggle or step-through.

**Step-through / stepper.** A button advances a process one step at a time. Use for algorithms (sort traversal, packet routing, hash collision resolution), protocols (handshake sequence, state machine transitions), or any process where the sequence is the lesson. Each step updates the diagram and adds an annotation. Do not animate the steps automatically, because the learner controls the pace.

**Toggle / mode switch.** A binary or small-N switch changes the view. Use when the concept has two distinct states or representations that benefit from direct comparison: time domain vs frequency domain, serial vs parallel execution, raw data vs normalized data. The learner sees the difference by switching.

**Direct manipulation.** The learner drags, rotates, or repositions an element in a diagram. Use for spatial or geometric concepts: moving a threshold line to see false-positive/negative tradeoff, rotating a beam to show angle vs gain, repositioning a node to show path length change. It takes more work to build, but it gives the learner the strongest intuition for spatial concepts.

**Input → computed output.** The learner types a value, and the slide computes and displays a result. Use for formulas where plugging in numbers is the lesson: Friis equation, Shannon capacity, Nyquist rate. Show the formula, the inputs, and the computed output updating live. Validate input range, and show a boundary error when the value falls outside it.

**Clickable taxonomy.** Clicking a term or node expands its definition or sub-structure inline. Use for hierarchical reference material: protocol layers, taxonomy trees, component breakdowns. The learner chooses how deep to explore.

**Comparative panels.** Two side-by-side panels update from a shared control. Use when the lesson is a trade-off or comparison that must be perceived simultaneously: two algorithms on the same data, two antenna configurations in the same environment.

**Simulation with run/pause.** The learner presses Run to advance a simulation in real time, and Pause to inspect state. Use for queue dynamics, signal propagation, population models, or any system with emergent behavior over time. Include a Reset. Keep the simulation loop under ~60 fps, and honor `prefers-reduced-motion` with a static snapshot mode.

---

## HTML deck pattern (React artifact)



### Structure

```jsx
import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

const SLIDES = [
  { id: "title", section: "TITLE", render: () => (...) },
  { id: "cover", section: "INDEX", render: () => (...) },
  { id: "concept", section: "MECHANISM", render: () => (...) },
  // Add one entry per claim.
  { id: "fin", section: "FIN", render: () => (...) },
];

export default function Deck() {
  const [i, setI] = useState(0);
  // Add keyboard navigation and the prev/next handlers.
  return (
    <div style={{...}}>
      <div className="slide">{SLIDES[i].render()}</div>
      <Footer index={i} total={SLIDES.length} section={SLIDES[i].section} />
      <Nav onPrev={...} onNext={...} />
    </div>
  );
}
```

### Sizing
- Enforce a 16:9 slide aspect ratio with CSS `aspect-ratio: 16/9`.
- Slide width fills the artifact viewport.
- Use `clamp(20px, 4vw, 64px)` for the outer slide padding and `1rem` for padding inside cards.
- Font sizes scale with viewport, so use `clamp()` for display sizes.

### Typography
Load Inter and JetBrains Mono via `@import` from `cdn.jsdelivr.net`:

```jsx
<style>{`
  @import url('https://cdn.jsdelivr.net/npm/@fontsource-variable/inter@5/index.css');
  @import url('https://cdn.jsdelivr.net/npm/@fontsource-variable/jetbrains-mono@5/index.css');
`}</style>
```

Use `-apple-system, sans-serif` as the fallback for Inter and `ui-monospace, monospace` as the fallback for JetBrains Mono.

Always use `font-variant-numeric: tabular-nums;` on numerals.

### Color tokens in JS

```jsx
const T = {
  paper: "#fdfaf1",
  paper2: "#ede8d6",
  paper3: "#fffefa",
  ink: "#1a1c1f",
  ink2: "#2a2d33",
  accent: "#c44e3f",
  info: "#2e6a78",
  stable: "#4d7a30",
  watch: "#b07020",
  unknown: "#88827a",
  textPrimary: "#1a1c1f",
  textSecondary: "#3a3d42",
  textMuted: "#5a5750",
  textOnDark: "#fdfaf1",
  textOnDarkMuted: "#a8a39a",
  hairline: "#c8c3b2",
  borderStrong: "#7d7967",
  // These tokens are the info callout family.
  infoSoft: "#e2e9ea", infoTint: "#bfcdce", infoText: "#2c3a3a",
  // These tokens are the stable callout family.
  stableSoft: "#e3ecd5", stableTint: "#bcc89e", stableText: "#2d4818",
  // These tokens are the watch callout family.
  watchSoft: "#f1e6d2", watchTint: "#d6c19a", watchText: "#5a431d",
  // These tokens are the cons callout family.
  consSoft: "#f6e2dc", consTint: "#e9b7ad", consText: "#7a2d22",
  // These tokens are the unknown callout family.
  unknownSoft: "#ebe8e3", unknownTint: "#c4bfb6", unknownText: "#3f3d39",
};
```

### Navigation

- Put prev/next buttons at the bottom, using Lucide `ChevronLeft` / `ChevronRight` at 16–20px with a 1.5px stroke.
- Bind `ArrowLeft` and `ArrowRight` keys via `useEffect` + `window.addEventListener`.
- Disable Prev on the first slide and Next on the last, and do not wrap around.
- Optionally, show position with a small row of indicator dots, and switch to a numeric counter past ~20 dots.

### Per-slide structure

Every slide has, in order:

1. **Eyebrow** — UPPERCASE +0.12em, 11px, muted, section name and slide id, for example `05 / 17 · NUMEROLOGY`.
2. **Title** — claim-led, sentence case, Inter 600. Size it with `clamp(24px, 3vw, 38px)`.
3. **Body** — paragraphs, tables, cards, diagrams, interactive controls.
4. **(Optional) Caption** — meta or caveat, mono 12px, muted, pinned bottom.

### Card patterns inside slides

The cards below are a quick reference, but the full paste-ready HTML is in `references/components.md`.

**KV card (paper)**
```jsx
<div style={{
  background: T.paper3,
  border: `1px solid ${T.hairline}`,
  borderRadius: 12,
  padding: 18,
}}>
  <div style={{ fontSize: 11, letterSpacing: "0.12em", textTransform: "uppercase", color: T.textMuted }}>label</div>
  <div style={{ fontFamily: "var(--font-mono)", fontSize: 14, marginTop: 6 }}>value</div>
</div>
```

**Evidence card (ink, on paper slide)**
- Use for a quoted measurement, a derived formula, or a stated decision inside a paper slide.
- Give it a `T.ink2` background, no border, 24px padding, and white-on-dark text.

### Forbidden in HTML decks
- Drop shadows, glow, gradients.
- Animated slide transitions beyond a 100ms opacity fade.
- localStorage / sessionStorage (not supported in inline artifacts).
- Builds that reveal one bullet at a time. Show the whole slide at once.
- Carousels or `display: none` sections during streaming.

---

## pptx deck pattern

Use this pattern when the user asks for a `.pptx` file. The pptx skill is for the file mechanics with python-pptx, while Toby Artifact covers the visuals.

### Format
- Use a 16:9 slide at 1920 × 1080 px native size.
- Set the outer padding to 64 px top and bottom and 80 px left and right.
- Use 18–24 px padding inside cards.

### Typography in pptx

| Use | Font | Size (Pt) | Weight |
|---|---|---|---|
| Display | Inter | 38 | 600 |
| H1 / slide title | Inter | 30 | 600 |
| H2 / card title | Inter | 22 | 600 |
| Section label | Inter (eyebrow) | 11 | 500 |
| Body | Inter | 16 | 400 |
| Body small | Inter | 14 | 400 |
| Meta / footer | JetBrains Mono | 11 | 400 |
| Value / ID | JetBrains Mono | 14 | 400 |

If Inter or JetBrains Mono is not installed, fall back to Calibri (sans) and Consolas (mono). Don't use Arial, Times, or Helvetica.

### pptx card patterns

**KV card (paper)**
- Set the background to `--toby-paper-3` (`#fffefa`).
- Draw a 1px hairline ring in `--border-hairline` (`#c8c3b2`).
- Use 18 px padding.
- Put the eyebrow label (11 pt, +0.12em, `--text-muted`) on top.
- Put the value (mono, 14 pt) below the label.

**Evidence card (ink)**
- Set the background to `--toby-ink-2` (`#2a2d33`).
- Use no border and 24 px padding.

### Color use in pptx
- Use `T.textPrimary` for default text on paper and `T.textOnDark` on ink.
- Use `T.textMuted` for section labels and meta on paper and `T.textOnDarkMuted` on ink.
- Use semantic tokens for status pills only.
- Use `T.accent` red for consequence callouts only.

### Section divider (ink) — recipe
- Fill the background with ink (`#1a1c1f`).
- Put the eyebrow (UPPERCASE +0.12em, 11 pt mono, `T.textOnDarkMuted`) at the top-left, for example `SECTION 03`.
- Center the section title (Inter 38 pt, 600, `T.textOnDark`) horizontally, about 38% down from the top.
- Place a hairline geometric primitive (orbit, square, crosshair) below the title at ≤ 80 px, with stroke `T.textOnDarkMuted`. See `references/geometry.md`.
- Put the slide id at the bottom-right.

### Forbidden in pptx
- Stock photos, lifestyle imagery, and hero photographs.
- Decorative gradients on title slides.
- Animated transitions beyond cut and 100ms fade.
- Builds that reveal one bullet at a time.
- Centered single-bullet slides that state a maxim.
- Drop shadows, glow, and reflections.
- Title Case headings.
