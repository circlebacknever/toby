---
name: toby-artifact-style
description: Apply Toby's artifact design system to HTML or React artifacts, SVG or HTML widgets, slide decks, diagrams, charts, dashboards, learning aids, reference cards, mockups, and artifact copy. Use when a produced visual artifact should follow Toby's colors, type, density, evidence-first layout, component patterns, and copy constraints.
---

# Toby Artifact Style

Every artifact you produce under this system either looks like it was made for this exact content, or it looks like AI output. Two outcomes. Pick the first one.

Toby Artifact Style is a constraint set. Tokens, copy constraints, and visual rules are tight. Structural choices stay wide: dense reference card, spacious single claim, ink-heavy authority piece, paper-first reading surface, animated process, static evidence panel, three-slide lesson, or twenty-slide reference deck. Make those choices per artifact.

The failure mode for any design system is convergence — every artifact starting to look like every other artifact. When you feel yourself reaching for the same layout you built last time, stop and pick a different one. The constraints don't mandate sameness. They mandate quality. Within them, vary everything.

## Three principles

**Paper carries work.** `--toby-paper` (`#fdfaf1`) is the default surface. The reader labors on paper — reading, comparing, parsing. Paper is the working mode.

**Dark means judgment.** `--toby-ink` (`#1a1c1f`) for decision surfaces, evidence panels, summaries, section dividers. When something uses ink, the artifact has stopped to make a point. Reserve it for moments that earn the weight. An artifact that uses ink everywhere has made nothing authoritative.

**Red is consequence.** `--toby-accent` (`#c44e3f`) for risk, breach, finality, threshold violation. Never a brand accent. Never plain emphasis. Its scarcity is what makes it land.

## Six visual moves that make Toby Artifact Style coherent

If a panel uses none of these, ask whether it earns its place.

1. **Tinted state families.** When a panel expresses a state (info / stable / watch / consequence / unknown), give it the three-step palette: pale background, mid-saturation border, dark saturated text. The whole panel reads as one mood. See "Callout philosophy" below — this is the foundational pattern.
2. **Categorical section accents.** When a page has multiple sections, give each its own color from the chart palette. The accent shows up as the section number, the bottom-rule strip under the heading, and small cell-id pills.
3. **Mono values, sans labels.** Every number, ID, timestamp, or coordinate is JetBrains Mono with tabular numerals. Every label and description is Inter. The two typefaces alternating is part of the visual signature.
4. **Hairline rules and small radii.** 1px hairlines do almost all the dividing. Cards stay at 12px radius; only outer containing frames get 18px.
5. **Density over whitespace.** Slides and dashboards run dense. Multiple KV pairs, stat grids, sparkline-in-table cells, evidence rows. The reader is treated as a serious professional reviewing evidence; they don't need a hero illustration.
6. **Three-tone progression for narrative blocks.** When a panel walks through reasoning, tint the rows: setup (info teal) → working (watch amber) → conclusion (stable green). The Worked Example component does this; other reasoning panels can borrow the pattern.

## Teaching content can become a deck

For substantial lessons, walkthroughs, lectures, or reference modules, prefer a Toby Artifact Style HTML deck artifact (paginated, prev/next, React `.jsx`) when the user asks for a produced artifact or the material is too dense for chat. For quick explanations, answer in chat and apply artifact copy rules only where artifact copy is being written.

What goes where:
- **Deck (artifact):** glossary, mechanism explanations, tables, diagrams, derivations, examples, summary.
- **Chat:** a short framing line, the comprehension check question, and any branch options.

Slide count grows with the material, but keep the deck to the smallest count that preserves the concept. If the material genuinely wants 18 slides, build 18.

See `references/decks.md` for deck patterns.

## Load reference files based on task

- Writing headings, paragraphs, labels, button text, or any substantive copy → `references/copy.md`
- Building a chart, plot, or data visualization → `references/charts.md`
- Producing a slide deck (HTML or pptx) → `references/decks.md`
- Building any component (callout, badge, stat grid, worked example, decision row, sparkline table, code block, dialog) → `references/components.md`
- Needing placeholder data or demo copy for a slide or artifact → `references/sample-content.md`
- Putting a content-scale or decorative geometric mark on a slide or panel → `references/geometry.md`

## Before you build

Run this checklist before writing any code or markup.

1. **Job.** What is this artifact doing — teaching a mechanism, summarizing evidence, providing a reference, walking a process, supporting a decision? The answer determines surface and density.
2. **Composition mode.** Pick one from below. Not the one you used last time.
3. **Ink allocation.** Decide before you start which panels or slides use ink and which use paper. Don't let it happen by accident.
4. **Logo primitive.** Name the shape. It should hint at the structure of the subject, not just the subject's name.
5. **For decks:** identify which slides earn interactivity before writing any slide. The concept governs the interaction type — see `references/decks.md`.

## Composition modes

Pick one per artifact. Vary across sessions. The mode is a structural commitment, not a color choice — it governs layout logic, density, and how ink and paper are distributed.

**Dense reference.** Grid of cards, high information density, multiple KV pairs per section, several columns. Rewards 30–45 seconds of attention per panel. Use for protocol references, parameter tables, specification sheets, side-by-side comparisons. Ink panels appear as evidence callouts inside a paper field.

**Spacious argument.** One concept per section. Generous white space. Each panel or slide earns its own breathing room. Reading pace is deliberate. Use when the concept is singular and deep — a derivation, a worked example, an analysis. Ink appears only at summary or decision points.

**Ink-anchored.** Paper is the default surface, but ink panels punctuate the flow — section dividers, quoted measurements, key decisions. The artifact reads as paper-first but the ink anchors give it authority at specific moments. Works well for reference decks with multiple sections.

**Ink-forward.** Majority ink surfaces, paper used only for relief or sharp contrast. The artifact asserts more than it explains. Use for summary dashboards, executive snapshots, decision panels, final-state reference cards. Paper panels should feel like interruptions — a table that needs to be read, a diagram that needs white space.

**Diagram-led.** The visual — chart, diagram, animation — dominates each panel. Text is annotation and label. Use when the concept is fundamentally spatial or relational: network topologies, signal flows, state machines, data distributions. Cards and KVs are secondary.

## Variation mandate

Hard rules against convergence.

- **Never use the same overall composition twice in a session.** If the last artifact was dense reference, this one is spacious argument or diagram-led.
- **Vary ink allocation.** Some artifacts are mostly paper with one or two ink evidence panels. Some are ink-forward with paper used for contrast. Some have no ink at all. All three are valid. Rotate.
- **Vary information density.** A lesson on a single formula can live on three spacious slides. A reference card on a protocol stack should be dense enough to reward sustained attention. Don't flatten everything to the same density.
- **The logo primitive must be chosen for the subject's structure.** See logos section. The same orbit shape on every artifact is a failure.
- **In decks, vary the opening.** See `references/decks.md`.
- **In decks, vary the interaction type.** See `references/decks.md`.

## Color tokens

```css
/* Surfaces */
--toby-paper:        #fdfaf1;  /* primary — bright off-white, slight warmth */
--toby-paper-2:      #ede8d6;  /* recessed */
--toby-paper-3:      #fffefa;  /* lifted card, near-white */

/* Authority + consequence */
--toby-ink:          #1a1c1f;  /* dark panels for decisions, evidence */
--toby-ink-2:        #2a2d33;  /* lifted dark surface */
--toby-accent:       #c44e3f;  /* consequence red — risk, breach, finality only */

/* Semantic state */
--toby-info:         #2e6a78;  /* teal */
--toby-stable:       #4d7a30;  /* leaf green */
--toby-watch:        #b07020;  /* amber */
--toby-unknown:      #88827a;  /* warm grey */

/* Chart palette — positional order for series and categorical accents */
--toby-blue-steel:   #2f6e8a;
--toby-muted-violet: #7a4e85;
--toby-field-olive:  #7d7e3a;
--toby-ochre:        #8a5a1c;
--toby-sage-steel:   #607a5f;
--toby-slate-blue:   #344b6e;

/* Text + border */
--text-primary:       #1a1c1f;
--text-secondary:     #3a3d42;
--text-muted:         #5a5750;
--text-on-dark:       #fdfaf1;
--text-on-dark-muted: #a8a39a;
--border-hairline:    #c8c3b2;
--border-strong:      #7d7967;

/* Interaction shades — derived from ink and accent */
--surface-card:       #fffefa;  /* alias of paper-3 for card backgrounds */
--surface-pressed:    #d9d3bf;
--ink-hover:          #4a4e57;
--ink-pressed:        #000000;
--accent-hover:       #a04030;
--accent-pressed:     #7e3023;

/* Code block — lifted syntax colors for dark bg */
--code-kw:            #8ec8d8;  /* keywords — info teal, lifted */
--code-num:           #e8a48e;  /* numbers — warm coral */
--code-str:           #a8c98a;  /* strings — green, lifted */
--code-com:           #7c7568;  /* comments — muted, italic */
```

## Callout philosophy — soft / tint / text per hue

Every semantic hue has a three-step palette. Use these together whenever a component expresses a state — alerts, toasts, status pills, badges, callouts, worked-example rows, KPI accent stripes. The whole component reads as one coherent color family.

```css
/* soft = pale bg · tint = mid border · text = saturated dark fg */
--toby-info-soft:    #e2e9ea;  --toby-info-tint:    #bfcdce;  --toby-info-text:    #2c3a3a;
--toby-stable-soft:  #e3ecd5;  --toby-stable-tint:  #bcc89e;  --toby-stable-text:  #2d4818;
--toby-watch-soft:   #f1e6d2;  --toby-watch-tint:   #d6c19a;  --toby-watch-text:   #5a431d;
--toby-cons-soft:    #f6e2dc;  --toby-cons-tint:    #e9b7ad;  --toby-cons-text:    #7a2d22;
--toby-unknown-soft: #ebe8e3;  --toby-unknown-tint: #c4bfb6;  --toby-unknown-text: #3f3d39;
```

Pattern for a state-tinted panel: background = `*-soft`, border = `*-tint`, left strip (4px) = un-soft hue, text = `*-text`. See `references/components.md` for paste-ready HTML.

## Color rules

- No gradients. No rainbow scales. No glow. No colored shadows.
- No red as brand accent. Use ink weight, hairline, or position for emphasis.
- Chart palette is positional — use in fixed order, by series index. Also drives section accents on long pages.
- **No left-accent-colored cards** as a general decoration (a known AI-slop tell). Exception: alerts/toasts use a single 4px coloured left strip from the callout family — that's a documented pattern, not the forbidden one.

## Typography

- **Sans:** Inter (400 / 500 / 600). System sans fallback.
- **Mono:** JetBrains Mono (400 / 500). For values, units, IDs, coordinates.
- **Sizes:** display 34 · h1 28 · h2 22 · section 18 · body 14 · body-sm 13 · meta 12 · eyebrow 11 · mono 13. Units: px on web; convert to Pt for pptx.
- **Weights:** 400 body, 500 emphasis, 600 headings. No 700 in product UI.
- **Letter-spacing:** 0 on display, headings, and body; +0.12em on eyebrows only.
- **Numerals:** tabular (`tnum`) everywhere.
- **Casing:** UPPERCASE eyebrows (tracked 0.12em) for section labels. Sentence case for headings and body. Never Title Case. All-lowercase for tokens (`$toby-paper`). Mono for values, IDs, coordinates.

## Spacing — all multiples of 4

Prefer named tokens. Pick the closest, never a one-off.

```css
--space-xs:     4px;   /* gap between tightly-coupled siblings */
--space-sm:     8px;   /* inline gap, badge padding */
--space-md:    12px;   /* tight control padding */
--space-base:  16px;   /* row padding, card body gap */
--space-lg:    20px;   /* cell padding, dialog body gap */
--space-xl:    24px;   /* section padding */
--space-2xl:   32px;   /* dialog padding */
--space-3xl:   40px;   /* empty-state padding */
--space-4xl:   48px;   /* major separation */
--space-5xl:   64px;   /* section gap */
```

## Control heights, icon sizes, radius, border widths

```css
/* Control heights — pair with --space-* paddings */
--ctrl-h-xs:   20px;   /* badge, very compact pill */
--ctrl-h-sm:   28px;   /* btn--sm, toolbar btn, pagination cell */
--ctrl-h-md:   36px;   /* default btn, input, combobox */
--ctrl-h-lg:   44px;   /* touch target, OTP slot */
--ctrl-h-xl:   56px;   /* topbar */

/* Icons */
--icon-xs: 12px;  --icon-sm: 14px;  --icon-md: 16px;  --icon-lg: 20px;  --icon-xl: 24px;

/* Radius — small radii keep the system serious */
--radius-xs:    4px;   /* kbd, day cells */
--radius-sm:    8px;   /* compact controls, chips */
--radius-md:   10px;   /* buttons */
--radius-base: 12px;   /* inputs, cards, panels */
--radius-lg:   18px;   /* outer slide panel, dialog */
--radius-full: 999px;  /* pills, status dots */

/* Border widths */
--bw-hairline: 1px;    /* default rule */
--bw-accent:   2px;    /* focus ring, in-page accent */
--bw-emph:     3px;    /* section accent strip, active-tab underline, sidebar inset */
--bw-strip:    4px;    /* alert left edge, dialog--alert top */
```

## Elevation, z-index, animation

```css
/* Elevation — pick the lowest layer that solves the problem */
--elev-hairline: 0 0 0 1px var(--border-hairline);
--elev-card:     0 1px 0 var(--border-hairline);
--elev-low:      0 1px 2px rgba(28,31,35,0.06);
--elev-mid:      0 2px 8px -2px rgba(28,31,35,0.10), 0 0 0 1px var(--border-hairline);
--elev-pop:      0 6px 24px -8px rgba(28,31,35,0.18), 0 0 0 1px var(--border-hairline);
--elev-high:     0 12px 32px -10px rgba(28,31,35,0.24), 0 0 0 1px var(--border-hairline);

/* Forbidden: inner shadows, glow, multi-layer ambient/key shadows, colored shadows. */

/* Z-index — strictly layered; never invent a value between these */
--z-base: 0;  --z-rail: 10;  --z-dropdown: 50;  --z-nav-panel: 60;
--z-popover: 70;  --z-tooltip: 80;  --z-sheet: 90;  --z-modal: 100;  --z-toast: 200;

/* Animation */
--ease-out:          cubic-bezier(0.2, 0, 0, 1);
--motion-fast:       100ms;  /* hover, focus, press */
--motion-quick:      120ms;  /* state changes */
--motion-disclosure: 180ms;  /* panel reveal */
--motion-overlay:    220ms;  /* sheet & dialog entrance */
```

- Allowed motion: opacity fade, 4–8px positional slide for menus/toasts, hairline ring on focus, 90° chevron rotation on accordion open.
- Forbidden: spring bounces, scale-up entrances, parallax, particle effects, animated illustrations.

## Interaction states

- **Hover (paper):** bg steps to `--toby-paper-2`. Foreground unchanged.
- **Hover (dark):** bg lifts to `--ink-hover` (`#4a4e57`). Text unchanged.
- **Active / press:** bg steps DARKER (`--surface-pressed` / `--ink-pressed` / `--accent-pressed`), border stays. No scale shrink. The control does NOT move.
- **Focus:** 2px outside ring in `--toby-info` (teal), 2px offset. **Never red.**
- **Selected / current in lists/trees/menus:** `--toby-paper-2` background + a 3px `--toby-info` inset on the left. Paper-3 against paper-3 is INVISIBLE — never use it as a selection state.

Hover and base must differ by ≥ 3:1 contrast (WCAG 1.4.11).

## Imagery + backgrounds

- Paper is the background. No imagery by default.
- Avoid generic lifestyle photos, decorative stock art, repeating patterns, textures, and gradients. Use real or generated imagery when the task requires the product, place, object, state, gameplay, or person to be inspectable.
- Geometry as decoration is allowed only when it clarifies. Two scales: **primary** at content size with a small uppercase label, or **decorative** small (≤ 80px) and quiet (opacity ≤ 0.25). See `references/geometry.md` for the named marks.

## Iconography

- Use Lucide where available. Inline SVG is acceptable for static artifacts; use the app's icon library for coded frontends when one exists. Icons are 16–20px, 1.5px stroke, square caps, monochromatic `currentColor`.
- Heroicons-outline, Tabler, and Phosphor-regular are acceptable fallback families. Material Icons and Carbon are too dense — forbidden.
- About 12 glyphs system-wide. If you're reaching for a 13th, a text label would do the job.
- Forbidden: emoji, unicode dingbats. Allowed unicode: `→` for handoffs, `·` as metadata separator, `±` for uncertainty.

## Logos / wordmarks

Per-artifact. Never a fixed brand.

Each artifact gets:
- A hairline geometric primitive.
- One short lowercase Inter-600 word naming the topic.
- A single red dot as the only color.

**The primitive must be chosen for the structure of the subject, not just its name.** A network topology → crosshair or grid. A recursive algorithm → nested squares. An antenna or wave → orbit arc. A decision process → branching lines or Y-fork. A time series → horizontal rail with a tick. A probability distribution → bell curve outline. A queue or pipeline → stacked horizontal bars.

Lazy defaults to refuse: orbit for everything, triangle because it's geometric, square because it's simple. If you cannot name why the shape fits the subject, pick a different shape.

## Purpose check

Every sentence, panel, or slide must do one of these. If it does none, remove it.

- teach a concept
- state a measurement
- define a term
- list a constraint
- walk a worked step
- pose a question that gates the next sentence

## Output-type mapping

### HTML / React artifacts
- Apply all tokens above. Background = `--toby-paper`. Cards = `--toby-paper-3` with 1px `--border-hairline` ring.
- Load Inter and JetBrains Mono via CDN. Provide system fallbacks.
- Numerals always tabular: `font-variant-numeric: tabular-nums;`.

### Visualizer SVG diagrams
- Call `visualize:read_me` first, then override its CSS variables with Toby Artifact tokens before generating output.
- Visualizer requires transparent background — set paper color on a top-level `<rect>` if a paper field is wanted.
- Use the Toby Artifact chart palette in positional order for any series.

### Visualizer HTML widgets
- Call `visualize:read_me` first, then override its CSS variables with Toby Artifact tokens.
- Keep background transparent. Apply Toby Artifact paper via a wrapper if needed.

### pptx slide decks
- See `references/decks.md`. The pptx skill handles file mechanics. Toby Artifact controls colors, fonts, sizes, padding, and slide structure.

### HTML decks for teaching
- See `references/decks.md`. React `.jsx` artifact with prev/next pagination and keyboard navigation.

## Copy rules

Every sentence in artifact copy must pass at least one of: **cite**, **negation**, **substitution**, **reader-skim**. Sentences that fail all four are filler. Remove them.

Copy cuts:
- Marketing adjectives (powerful, intuitive, seamless, elegant, game-changing, delightful).
- Throat-clearing openers (in today's fast-paced world, we all know, let's dive in).
- Self-praise of the writing (cleanly, clearly, honestly, in plain English, just the facts).
- Vague magnitude (a lot of, many, huge, massive) — replace with a number, range, or omit.
- Inflated verbs (unlock, transform, supercharge, revolutionize, harness, empower).
- Mission-stating (on a mission to, dedicated to, passionate about).
- First and second person (we, I, our, you) in most reference contexts.
- Emoji. Exclamation points.
- Numbers without units. A bare number is a defect.

**No contrastive framing.** State the positive claim directly.

**Headings carry the claim.** Body explains or qualifies. Caveats sit next to the claim, never in a footnote.

Global Toby voice controls register. This skill controls artifact structure, visual tokens, density, copy tests, and component patterns.

For any substantive copy work, load `references/copy.md`.
