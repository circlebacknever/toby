---
name: toby-artifact-style
description: >-
  Applies Toby's visual design system to a visual and to the copy inside it. The
  visual can be a diagram, chart, dashboard, slide deck, HTML or React page,
  SVG, mockup, or reference card. Use it when the user asks to draw, show,
  chart, diagram, or build a visual, including a visual that explains something.
  Skip it for a text answer in chat, which toby-explain covers, and for a game,
  which only /toby-game starts.
---

# Toby Artifact Style

This skill fixes the tokens, copy rules, and visual rules. Pick the structure for each artifact from the composition modes below.

## Color roles

**Paper is the surface for working content.** `--toby-paper` (`#fdfaf1`) is the default surface. Use paper for panels where the reader reads, compares, and parses content.

**Dark panels show judgments.** Use `--toby-ink` (`#1a1c1f`) for decision panels, evidence panels, summaries, and section dividers. An ink panel shows the reader that the artifact states a judgment at that point. Reserve ink for those points, because when an artifact uses ink everywhere, the reader cannot tell which panel states a judgment.

**Red is for consequences.** Use `--toby-accent` (`#c44e3f`) for risk, breach, finality, and threshold violation. Never use red as a brand accent or for plain emphasis. Keep it rare, because readers stop noticing a red that appears often.

## Visual patterns

1. **Tinted state families.** A panel that shows a state (info, stable, watch, consequence, unknown) uses that hue's `-soft` background, `-tint` border, and `-text` text, with a 4px left strip in the base hue. The tokens are under State families below.
2. **Categorical section accents.** When a page has multiple sections, give each its own color from the chart palette. The accent appears as the section number, the bottom-rule strip under the heading, and small cell-id pills.
3. **Hairline rules and small radii.** Use 1px hairlines for almost every divider. Cards stay at 12px radius, and only outer containing frames get 18px.
4. **Density.** Outside spacious-argument mode, fill slides and dashboards with KV pairs, stat grids, sparkline-in-table cells, and evidence rows.
5. **Three-tone progression for narrative blocks.** When a panel shows a chain of reasoning, tint its rows in order: setup (info teal) → working (watch amber) → conclusion (stable green). The Worked Example component uses this progression, and other reasoning panels can use it too.

## Load reference files based on task

- Writing paragraphs, a hero, feature cards, or a CTA, or rewriting a sentence that fails a copy test → `references/copy.md`
- Building a chart, plot, or data visualization → `references/charts.md`
- Producing a slide deck (HTML or pptx) → `references/decks.md`
- Building any component (callout, badge, stat grid, worked example, decision row, sparkline table, code block, dialog) → `references/components.md`
- Writing CSS for an HTML or React page, including controls, overlays, motion timing, interaction states, icons, or a code block → `references/ui-tokens.md`
- Needing placeholder data or demo copy for a slide or artifact → `references/sample-content.md`
- Putting a content-scale or decorative geometric mark on a slide or panel → `references/geometry.md`
- Drawing an SVG diagram or a pptx slide, or placing HTML elements by coordinates → `references/layout.md`

## Before you build

Run this checklist before writing any code or markup.

1. **Job.** What is this artifact doing? It might teach a mechanism, summarize evidence, provide a reference, walk through a process, or support a decision. The answer determines surface and density.
2. **Composition mode.** Pick one mode from the list below.
3. **Ink allocation.** Decide which panels or slides use ink, or that none do, before you start.
4. **Logo primitive.** Pick a shape that suggests the structure of the subject.
5. **Layout.** For a diagram or slide, write the node and arrow lists from `references/layout.md` before any coordinates.
6. **For decks:** before writing any slide, identify which slides need interactivity. Choose the interaction type to fit the concept. See `references/decks.md`.

## Composition modes

Pick one mode per artifact. The mode sets the layout, the density, and where ink goes.

**Dense reference.** A dense reference is a grid of cards with high information density, several columns, and multiple KV pairs per section. Each panel has enough content for 30–45 seconds of reading. Use it for protocol references, parameter tables, specification sheets, and side-by-side comparisons. Ink panels appear as evidence callouts inside a paper field.

**Spacious argument.** A spacious argument puts one concept in each section, with generous white space around every panel or slide. The reader moves through it slowly. Use it when the artifact covers one deep concept, such as a derivation, a worked example, or an analysis. Ink appears only at summary or decision points.

**Ink-anchored.** A mostly paper artifact whose ink panels mark section dividers, quoted measurements, and decisions. Use it for reference decks with several sections.

**Ink-forward.** Most surfaces are ink, and paper appears only for relief or sharp contrast. The artifact mostly states conclusions and explains less. Use it for summary dashboards, executive snapshots, decision panels, and final-state reference cards. Use a paper panel only as an interruption, such as a table that needs reading or a diagram that needs white space.

**Diagram-led.** A chart, diagram, or animation takes up most of each panel, and text serves as annotation and labels. Use it when the concept is spatial or relational, as in network topologies, signal flows, state machines, and data distributions. Cards and KVs are secondary.

## Variation

When this session already produced an artifact, give the new one a different composition mode, ink allocation, and logo primitive. A deck also takes a different opening pattern and interaction type from `references/decks.md`.

## Color tokens

```css
/* Surfaces */
--toby-paper:        #fdfaf1;
--toby-paper-2:      #ede8d6;  /* recessed */
--toby-paper-3:      #fffefa;  /* lifted card, near-white */

/* Authority + consequence */
--toby-ink:          #1a1c1f;  /* dark panels for decisions, evidence */
--toby-ink-2:        #2a2d33;  /* lifted dark surface */
--toby-accent:       #c44e3f;

/* Semantic state */
--toby-info:         #2e6a78;  /* teal */
--toby-stable:       #4d7a30;  /* leaf green */
--toby-watch:        #b07020;  /* amber */
--toby-unknown:      #88827a;  /* warm grey */

/* The chart palette is in positional order for series and categorical accents. */
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

/* Fonts */
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', ui-monospace, monospace;
```

## State families

```css
/* soft = pale bg · tint = mid border · text = saturated dark fg */
--toby-info-soft:    #e2e9ea;  --toby-info-tint:    #bfcdce;  --toby-info-text:    #2c3a3a;
--toby-stable-soft:  #e3ecd5;  --toby-stable-tint:  #bcc89e;  --toby-stable-text:  #2d4818;
--toby-watch-soft:   #f1e6d2;  --toby-watch-tint:   #d6c19a;  --toby-watch-text:   #5a431d;
--toby-cons-soft:    #f6e2dc;  --toby-cons-tint:    #e9b7ad;  --toby-cons-text:    #7a2d22;
--toby-unknown-soft: #ebe8e3;  --toby-unknown-tint: #c4bfb6;  --toby-unknown-text: #3f3d39;
```

## Color rules

- Do not use gradients, rainbow scales, glow, inner shadows, or colored shadows.
- For emphasis, use ink weight, a hairline, or position.
- Do not give a card a colored left accent as decoration, because readers recognize that accent as a sign of AI-generated design. An alert or toast keeps its 4px state strip.

## Typography

- **Sans:** Use Inter at weights 400, 500, and 600, with the system sans font as the fallback.
- **Mono:** Use JetBrains Mono at weights 400 and 500 for values, units, IDs, timestamps, and coordinates.
- **Sizes:** display 34 · h1 28 · h2 22 · section 18 · body 14 · body-sm 13 · meta 12 · eyebrow 11 · mono 13. The sizes are in px. For pptx, use the point sizes in `references/decks.md`.
- **Weights:** Use 400 for body, 500 for emphasis, and 600 for headings. Do not use 700 in product UI.
- **Letter-spacing:** Use 0 on display text, headings, and body, and use +0.12em on eyebrows only.
- **Numerals:** Use tabular numerals (`tnum`) everywhere.
- **Casing:** Use UPPERCASE eyebrows (tracked 0.12em) for section labels and sentence case for headings and body. Never use Title Case. Write tokens in all-lowercase (`$toby-paper`).

## Motion

- Use only these motions: an opacity fade, a 4–8px positional slide for menus and toasts, and a hairline ring on focus. An accordion can also rotate its chevron 90° when it opens.
- Do not use spring bounces, scale-up entrances, parallax, particle effects, or animation that only decorates. An animated process the reader can step through or pause is content.

## Imagery + backgrounds

- Paper is the background. Artifacts use no imagery by default.
- Avoid generic lifestyle photos, decorative stock art, repeating patterns, textures, and gradients. Use real or generated imagery when the task requires the product, place, object, state, gameplay, or person to be inspectable.
- Do not use emoji or unicode dingbats. The allowed unicode characters are `→` for handoffs, `·` as a metadata separator, and `±` for uncertainty.

## Logos

Each artifact gets its own logo, built from three parts:

- A hairline geometric primitive.
- One short lowercase Inter-600 word for the topic.
- A single red dot as the only color.

**Choose the primitive for the structure of the subject.** Use a crosshair or grid for a network topology, nested squares for a recursive algorithm, and an orbit arc for an antenna or wave. Use branching lines or a Y-fork for a decision process, and a horizontal rail with a tick for a time series. Use a bell curve outline for a probability distribution, and stacked horizontal bars for a queue or pipeline. Use a partial orbit arc for a rotation or cycle, because a closed circle reads as decoration, and a 3×3 grid of squares for matrix or table data.

Refuse these lazy defaults: an orbit for everything, a triangle because it is geometric, and a square because it is simple. If you cannot explain why the shape fits the subject, pick a different shape.

## Purpose check

Remove a panel or slide that does none of these jobs:

- teach a concept
- state a measurement
- define a term
- list a constraint
- walk a worked step
- pose a question that the reader answers before the next sentence

## Output types

- **HTML or React:** apply the tokens above, and load Inter and JetBrains Mono from Google Fonts with system fallbacks. Set the page to `--toby-paper` and cards to `--toby-paper-3` with a 1px `--border-hairline` ring.
- **Visualizer SVG or HTML widget:** call `visualize:read_me` first, then override its CSS variables with these tokens. Keep the background transparent, and put paper on a top-level `<rect>` or a wrapper when the widget needs it.
- **pptx or HTML deck:** follow `references/decks.md`. The pptx skill handles the file.

## Copy rules

Run four tests on every sentence of artifact copy, and rewrite or cut each sentence that fails one. `references/copy.md` has a passing and a failing example for each.

1. **Cite.** The claim states its source, measurement, or mechanism.
2. **Negation.** Someone could write the opposite claim and mean it.
3. **Substitution.** The sentence becomes nonsense when an unrelated noun replaces its subject.
4. **Reader-skim.** A reader who knows the material loses something when the sentence is cut.

Give every number a unit. Put each caveat and each assumption next to the claim it qualifies, never in a footnote.
