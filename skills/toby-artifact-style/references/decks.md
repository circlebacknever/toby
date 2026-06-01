# Toby Artifact decks

Load this file when producing a slide deck — HTML for an inline inline artifact (default for teaching), or pptx for a downloadable file.

## Format selection

| Format | Use when |
|---|---|
| HTML deck (React `.jsx` artifact) | Teaching artifacts, reference modules, anything paired with personalized-teaching skill. Default. |
| pptx | the user explicitly asks for a `.pptx` file, asks to download a deck, or asks for a deck for offline use. |

If unsure, build the HTML deck.

---

## Before you build this deck

Run these before writing any slide.

1. **What is the deck doing?** Teaching a mechanism, summarizing evidence, building a reference, walking a process? The answer determines density and opening structure.
2. **Composition mode.** Pick one from SKILL.md. Not the one used last time.
3. **Ink allocation.** Decide which slides use ink before you start. Section dividers, summaries, glossaries, formula slides, decision slides earn ink. Most slides are paper. Ink-forward decks (majority dark) are valid when the deck asserts more than explains — decide deliberately.
4. **Opening pattern.** Pick from the options below. Not every deck starts with title → glossary.
5. **Interactivity plan.** Walk the slides conceptually. For each one, ask whether a parameter governs the concept. If yes, pick an interaction type from the catalog below — not always a slider.

---

## Deck structure — title and end bookends

Every Toby Artifact deck opens with a **title slide** and closes with an **end slide**. Both are sparse, intentionally — they bracket the dense reference content. Between them: cover/index, then content, then references.

```
01  Title           (paper, sparse, mark + giant topic)
02  Cover & index   (paper, dense TOC grid)
03–13  Content      (paper or ink, dense reference)
14  Fin             (ink, sparse, one closing claim)
```

---

## Shared slide content rules

Apply to both HTML and pptx output.

### One main claim per slide

The slide title is the claim. The body shows the work. If two claims belong on a slide, split them.

- Pass: "Cache layer cut p95 from 312 ms to 184 ms."
- Fail: "Performance results."

### Two slide tones

Every slide is one tone. Decide per slide.

**Paper (default)** — `#fdfaf1` background. For reading: tables, diagrams, definitions, worked steps, lists, walkthroughs.

**Ink** — `#1a1c1f` background. For authority: section dividers, glossaries, formula slides, summaries, decision points. Body text on ink: `#fdfaf1` primary, `#a8a39a` muted.

### Information density

Reference-deck system. Reading-manual feel.

Dense slides: multiple cards per slide, several key-value pairs, tables. A slide should reward 30–45 seconds of attention.

Not every slide needs to be dense. A slide presenting a single derivation or worked example can breathe. Match density to the cognitive load of the content.

### Slide id (footer)

Right-aligned. Mono. Muted. Format:

```
XX / NN · R-XX.X · LABEL
```

- `XX / NN` — current slide of total (1-indexed, zero-padded to 2 digits).
- `R-XX.X` — reference deck identifier (e.g. `R-04.2`).
- `LABEL` — short uppercase section name (`TITLE`, `INDEX`, `GLOSSARY`, `KEPLER`, `WORKED`, `APPLY`, `FIN`).

On ink slides, color the footer text with `--text-on-dark-muted` (`#a8a39a`).

---

## Opening patterns

Vary the opening structure across decks. Pick one.

**Title slide → cover/index (default for reference decks).** Sparse title with the toby mark + giant topic, followed by a dense TOC grid. Works for multi-section reference decks.

**Title → glossary.** Title slide with logo primitive, then a glossary slide defining the key terms before the mechanism. Works for concept-heavy topics where undefined terms would block comprehension.

**Title → problem statement.** Title slide, then an ink slide stating the problem or question the deck answers. Works for analysis, diagnosis, or decision-support decks.

**Title → worked example first.** Title slide, then immediately a concrete worked example or case. The mechanism explanation comes after. Works when intuition precedes formalism.

**Title → big fact.** Title slide, then a single high-contrast slide stating the central numerical fact, measurement, or result. Works for evidence-led decks where the conclusion is the anchor.

**No title slide.** Start directly with the first claim. Use a section eyebrow and the logo primitive in the footer rather than a dedicated opening slide. Works for short reference cards (≤ 6 slides) or when the deck is one section of a longer session.

---

## Title slide pattern — sparse, paper-toned

The opening identity slide. Big topic, the toby wordmark + mark, a quiet decorative orbit lattice. No TOC here — the cover/index slide handles that.

```html
<section data-screen-label="01 Title">
  <!-- Toby Artifact mark + wordmark, top-left -->
  <div style="position: absolute; top: 64px; left: 80px; display: flex; align-items: center; gap: 16px;">
    <svg width="44" height="44" viewBox="0 0 64 64" fill="none">
      <circle cx="32" cy="32" r="28" stroke="var(--toby-ink)" stroke-width="1.4"/>
      <ellipse cx="32" cy="32" rx="28" ry="10" stroke="var(--toby-ink)" stroke-width="1.2" transform="rotate(-22 32 32)"/>
      <circle cx="56" cy="20" r="4" fill="var(--toby-accent)"/>
      <circle cx="32" cy="32" r="1.6" fill="var(--toby-ink)"/>
    </svg>
    <span style="font-family: var(--font-sans); font-size: 24px; font-weight: 600; letter-spacing: -0.012em;">toby</span>
  </div>

  <!-- Decorative orbit lattice, large + quiet, far right -->
  <div style="position: absolute; right: -120px; top: 50%; transform: translateY(-50%); opacity: 0.16;">
    <!-- nested ellipses + a small center dot -->
  </div>

  <!-- Title block, anchored left -->
  <div style="position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: center; padding: 0 80px;">
    <div class="ds-eyebrow" style="margin-bottom: 36px;">REFERENCE DECK · R-04.2</div>
    <h1 style="font-size: 128px; font-weight: 600; letter-spacing: -0.024em; line-height: 0.95; margin: 0; max-width: 1200px;">
      Orbital<br>mechanics.
    </h1>
    <p style="font-size: 22px; color: var(--text-secondary); max-width: 720px; margin: 48px 0 0; line-height: 1.55;">
      A working reference for orbits in classical Newtonian gravity. Thirteen reading slides; values carry units; caveats sit beside the figures they qualify.
    </p>
  </div>

  <!-- Bottom mono stripe — three captions -->
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

Recipe:
- **Toby Artifact mark + wordmark** in the top-left. Mark is a hairline circle, two tilted ellipses, a single red dot, a small centre dot. Wordmark is lowercase `toby` in Inter 600.
- **Big topic** in 96–128px Inter 600, tight negative letter-spacing. Period at the end. Anchored left.
- **Quiet decorative shape** on the right, opacity ≤ 0.16. Pick from `references/geometry.md`.
- **Bottom mono stripe** with 2–3 captioned facts (contents, convention, owner). Small uppercase eyebrows + mono values.

---

## Cover / index slide pattern

Dense table-of-contents. 4-column grid of cards, each card naming a section.

- Eyebrow + h1 + short paragraph at the top describing the deck's scope.
- A `--bw-emph` (3px) coloured rule beneath the intro to separate it from the TOC.
- 4×3 grid of cards (or 3×4 — pick to fit slide count). Each card: section number (mono, muted), section title, tagline (meta).
- Highlight new or signature slides by recolouring their section number to the relevant accent.
- A KV block at the bottom for scope / units / convention / out-of-scope.
- A geometry mark in the corner at decorative-scale.

---

## Content slide patterns

These all sit between the cover and the end slide. Compose freely — bring the component vocabulary onto slides.

| Slide type | Pattern |
|---|---|
| **Glossary / definition** | Ink-toned. 3-column dense grid of definition blocks. Eyebrow per column naming the term cluster. |
| **Three-card / three-laws** | 3 cards side-by-side, each with eyebrow + section heading + diagram (SVG) + body + formula block. |
| **Comparison table** | Full-width table with mono cells; group cells with subhead rows or coloured family stripes. |
| **Formula slide** | Ink-toned. Two formula cards side-by-side, plus a worked-examples table beneath. |
| **Worked example** | Use the **Worked Example** component (three rows, info/watch/stable tinted). Pair with a dark **Code Block** in a side column. Cross-check table below. |
| **Annotated diagram** | A card with `position: relative`, an SVG illustration inside, **Annotation Pins** numbered 1..n overlaid, and a side legend mapping numbers to terms. |
| **KPI / stat snapshot** | Ink-toned. 4-column **Stat Grid** with cycling accent stripes. Pair with rejected-alternative **Alerts** in a side column. |
| **Decision** | Ink-toned. Stat Grid up top. Authority decision card (dark, red top hairline, pill in the corner). Rejected alternatives stack as state-tinted Alerts. |
| **Section / quote / summary** | Ink-toned. Sparse. A single claim centered, with a small eyebrow. Optional KV block beneath. |
| **References** | Ink-toned. Reading list table with each entry: cite block, type, one-line description. Plus an "up next" rail at the side. |

See `references/components.md` for the components referenced above.

---

## End slide pattern — sparse, ink-toned

The closing bookend. Centred single claim — the most fundamental fact the deck taught. Ink background, faint geometric backdrop, the toby wordmark in the corner. No content cards.

Recipe:
- **Ink-toned.** Background `#1a1c1f`.
- **Toby Artifact mark + wordmark** in the top-left, using `--text-on-dark` for the strokes (red dot stays accent red).
- **One centred claim** in 64–80px Inter 500. The most fundamental fact the deck just taught — the sentence that, if remembered alone, still does work. Period at the end.
- **Small eyebrow** above the claim in `--toby-accent` (one of the few places consequence red is allowed without indicating risk — it marks the deck closing).
- **One-paragraph context** beneath in 16–17px, color `--text-on-dark-muted`. Cites the source / historical anchor for the claim.
- **Faint geometric backdrop** behind the claim at opacity ≤ 0.12.
- **Bottom mono stripe** with two captions: source line on the left, "begin again at § 02" pointer on the right.
- **No content cards.** No KPIs, no tables, no callouts. The closing slide is one sentence and a frame.

Example claim line: `Bound orbits are ellipses. The rest is detail.`

---

## Title slide logo primitive

Each deck gets a per-artifact logo: a hairline geometric primitive + one short lowercase Inter-600 word naming the topic + a single red dot as the only color.

**Pick the shape for the structure of the subject, not just its name.** Examples:
- Network topology, graph, mesh → crosshair or grid lattice
- Recursive or nested structure → concentric squares or nested brackets
- Wave, signal, antenna, oscillation → arc or sinusoidal rail
- Decision tree, branching process → Y-fork or tree branches
- Time series, pipeline, queue → horizontal rail with tick marks
- Probability, distribution, uncertainty → bell outline or spread cone
- Rotation, orbit, cycle → partial orbit arc (not a full circle — too generic)
- Matrix, table, grid data → small grid of squares, 3×3

Lazy defaults to refuse: orbit for everything, plain triangle, plain square. If you cannot name why the shape fits the subject's structure, pick a different shape.

See `references/geometry.md` for the 20 named geometric marks and their purposes.

---

## Interactivity catalog

The concept governs the interaction type. Identify what the learner needs to falsify or explore, then pick the mechanism. Sliders are one option among many.

**When to make a slide interactive:** the concept has a parameter that governs a visual outcome, a trade-off between two effects, or a process the learner should be able to step through. If moving a control would let the learner falsify an intuition — build it. Decorative motion fails the test.

### Interaction types

**Slider (continuous parameter).** A scalar value governs a visual or numerical outcome. Use when the relationship between input and output is the lesson: gain vs noise figure, sample size vs confidence interval, learning rate vs convergence. Skip when the parameter is categorical or when the interesting thing isn't the gradient — use a toggle or step-through.

**Step-through / stepper.** A button advances a process one step at a time. Use for algorithms (sort traversal, packet routing, hash collision resolution), protocols (handshake sequence, state machine transitions), or any process where the sequence is the lesson. Each step updates the diagram and adds an annotation. Don't animate automatically — let the learner control the pace.

**Toggle / mode switch.** A binary or small-N switch changes the view. Use when the concept has two distinct states or representations that benefit from direct comparison: time domain vs frequency domain, serial vs parallel execution, raw data vs normalized data. The learner sees the difference by switching.

**Direct manipulation.** The learner drags, rotates, or repositions an element in a diagram. Use for spatial or geometric concepts: moving a threshold line to see false-positive/negative tradeoff, rotating a beam to show angle vs gain, repositioning a node to show path length change. Requires more implementation but produces the strongest intuition for spatial concepts.

**Input → computed output.** The learner types a value; the slide computes and displays a result. Use for formulas where plugging in numbers is the lesson: Friis equation, Shannon capacity, Nyquist rate. Show the formula, the inputs, and the computed output updating live. Validate input range; show a boundary error rather than breaking.

**Clickable taxonomy.** Clicking a term or node expands its definition or sub-structure inline. Use for hierarchical reference material: protocol layers, taxonomy trees, component breakdowns. The learner explores at their own depth rather than being walked through every branch.

**Comparative panels.** Two side-by-side panels update from a shared control. Use when the lesson is a trade-off or comparison that must be perceived simultaneously: two algorithms on the same data, two antenna configurations in the same environment.

**Simulation with run/pause.** The learner presses Run to advance a simulation in real time, and Pause to inspect state. Use for queue dynamics, signal propagation, population models, or any system with emergent behavior over time. Include a Reset. Keep the simulation loop under ~60 fps; honor `prefers-reduced-motion` with a static snapshot mode.

---

## HTML deck pattern (React artifact)

The default format.

### Structure

```jsx
import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

const SLIDES = [
  { id: "title", section: "TITLE", render: () => (...) },
  { id: "cover", section: "INDEX", render: () => (...) },
  { id: "concept", section: "MECHANISM", render: () => (...) },
  // one entry per claim
  { id: "fin", section: "FIN", render: () => (...) },
];

export default function Deck() {
  const [i, setI] = useState(0);
  // keyboard nav, prev/next handlers
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
- Slide aspect ratio: 16:9, enforced via CSS `aspect-ratio: 16/9`.
- Slide width fills the artifact viewport.
- Padding inside slide: `clamp(20px, 4vw, 64px)` outer; `1rem` inside cards.
- Font sizes scale with viewport — use `clamp()` for display sizes.

### Typography
Load Inter and JetBrains Mono via `@import` from `cdn.jsdelivr.net`:

```jsx
<style>{`
  @import url('https://cdn.jsdelivr.net/npm/@fontsource-variable/inter@5/index.css');
  @import url('https://cdn.jsdelivr.net/npm/@fontsource-variable/jetbrains-mono@5/index.css');
`}</style>
```

Fallbacks: `-apple-system, sans-serif` for Inter; `ui-monospace, monospace` for JetBrains Mono.

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
  // callout family — info
  infoSoft: "#e2e9ea", infoTint: "#bfcdce", infoText: "#2c3a3a",
  // callout family — stable
  stableSoft: "#e3ecd5", stableTint: "#bcc89e", stableText: "#2d4818",
  // callout family — watch
  watchSoft: "#f1e6d2", watchTint: "#d6c19a", watchText: "#5a431d",
  // callout family — cons
  consSoft: "#f6e2dc", consTint: "#e9b7ad", consText: "#7a2d22",
  // callout family — unknown
  unknownSoft: "#ebe8e3", unknownTint: "#c4bfb6", unknownText: "#3f3d39",
};
```

### Navigation

- Prev/next buttons at the bottom. Lucide `ChevronLeft` / `ChevronRight` at 16–20px, 1.5px stroke.
- Bind `ArrowLeft` and `ArrowRight` keys via `useEffect` + `window.addEventListener`.
- Disable Prev on first slide, Next on last. Don't wrap around.
- Optional: small dot indicator row showing position, max ~20 dots before switching to numeric counter.

### Per-slide structure

Every slide has, in order:

1. **Eyebrow** — UPPERCASE +0.12em, 11px, muted, section name and slide id (e.g. `05 / 17 · NUMEROLOGY`).
2. **Title** — claim-led, sentence case, Inter 600. Sized via `clamp(24px, 3vw, 38px)`.
3. **Body** — paragraphs, tables, cards, diagrams, interactive controls.
4. **(Optional) Caption** — meta or caveat, mono 12px, muted, pinned bottom.

### Card patterns inside slides

See `references/components.md` for full paste-ready HTML. Quick reference:

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
- `T.ink2` background, no border, 24px padding, white-on-dark text.

### Forbidden in HTML decks
- Drop shadows, glow, gradients.
- Animated slide transitions beyond a 100ms opacity fade.
- localStorage / sessionStorage (not supported in inline artifacts).
- Builds that reveal one bullet at a time. Show the whole slide at once.
- Carousels or `display: none` sections during streaming.

---

## pptx deck pattern

Used when the user asks for a `.pptx` file. The pptx skill handles file mechanics (python-pptx). Toby Artifact controls visuals.

### Format
- 16:9, 1920 × 1080 px native.
- Outer padding: 64 px top/bottom, 80 px left/right.
- Inside cards: 18–24 px padding.

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
- Background: `--toby-paper-3` (`#fffefa`).
- 1px hairline ring: `--border-hairline` (`#c8c3b2`).
- 18 px padding.
- Eyebrow label (11 pt, +0.12em, `--text-muted`) on top.
- Value (mono, 14 pt) below.

**Evidence card (ink)**
- Background: `--toby-ink-2` (`#2a2d33`).
- No border.
- 24 px padding.

### Color use in pptx
- Default text: `T.textPrimary` on paper, `T.textOnDark` on ink.
- Section labels and meta: `T.textMuted` on paper, `T.textOnDarkMuted` on ink.
- Semantic tokens for status pills only.
- `T.accent` red for consequence callouts only.

### Section divider (ink) — recipe
- Full ink background (`#1a1c1f`).
- Eyebrow (UPPERCASE +0.12em, 11 pt mono, `T.textOnDarkMuted`) at top-left: `SECTION 03`.
- Section title (Inter 38 pt, 600, `T.textOnDark`) centered horizontally, vertically positioned at ~38% from top.
- Hairline geometric primitive (orbit, square, crosshair) below the title, ≤ 80 px, stroke `T.textOnDarkMuted`. See `references/geometry.md`.
- Slide id at bottom-right.

### Forbidden in pptx
- Stock photos. Lifestyle imagery. Hero photographs.
- Decorative gradients on title slides.
- Animated transitions beyond cut and 100ms fade.
- Builds that reveal one bullet at a time.
- Centered single-bullet "wisdom" slides.
- Drop shadows. Glow. Reflections.
- Title Case headings.
