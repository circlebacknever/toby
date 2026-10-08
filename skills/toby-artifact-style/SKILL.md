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

This skill sets the color tokens, the copy rules, and the visual rules that every artifact follows. Pick the structure for each artifact from the composition modes below.

## Words used in this skill

- **Paper** is the cream background color `--toby-paper`. A paper panel is a panel with that background.
- **Ink** is the near-black color `--toby-ink`. An ink panel is a panel with an ink background.
- **Red** is the color `--toby-accent`.
- **Hairline** is a 1px line used as a border or a divider.
- **Eyebrow** is a small UPPERCASE label above a heading or a value, set at 11px with 0.12em letter-spacing.
- **Mono** is the monospace font, JetBrains Mono.
- **KV pair** is a label and its value shown side by side, such as `RETRY RATE` and `18%`.
- **Pill** is a small label with fully rounded ends.
- **Sparkline** is a small line chart with no axes that fits inside a table cell or next to a value.
- **Status colors** are the five color sets for info, stable, watch, consequence, and unknown. Each set has a `-soft` background color, a `-tint` border color, and a `-text` text color. The tokens are under State families below.
- **Section accent** is the chart palette color given to one section of a page.

## Color roles

**Paper.** `--toby-paper` (`#fdfaf1`) is the default background. Use paper for any panel where the reader reads text, compares values, or works through details.

**Ink.** Use `--toby-ink` (`#1a1c1f`) for decision panels, evidence panels, summaries, and section dividers. An ink panel tells the reader that this panel gives a conclusion or a decision. Use ink only for those panels, because when an artifact uses ink everywhere, the reader cannot tell which panel gives a conclusion.

**Red.** Use `--toby-accent` (`#c44e3f`) for a risk, a broken limit, a value past its threshold, or an action that cannot be undone. Never use red as a brand color or for plain emphasis. Keep red rare, because readers stop noticing a red that appears often.

## Visual patterns

1. **Status panels.** A panel that shows a status (info, stable, watch, consequence, or unknown) uses the status colors for that status. Its background is the `-soft` color, its border is the `-tint` color, and its text is the `-text` color. The panel also has a 4px strip on its left edge in the main color of that status, such as `--toby-watch`.
2. **Section accents.** When a page has more than one section, give each section its own color from the chart palette. Use that color for the section number, for a strip under the section heading, and for the small pills that show cell ids.
3. **Hairlines and small corner radii.** Use hairlines for almost every divider. Cards keep a 12px corner radius, and only the outer frame that contains them gets 18px.
4. **Density.** Unless the artifact uses the spacious argument mode, fill slides and dashboards densely. Use KV pairs, stat grids, tables with sparklines in their cells, and rows that each state one measurement.
5. **Three colors for a chain of reasoning.** When a panel shows a chain of reasoning, give its rows the `-soft` status colors in a fixed order. The rows with the starting facts use info teal, the working rows use watch amber, and the conclusion uses stable green. The Worked Example component uses this order. Other reasoning panels can use it too.

## Load reference files based on task

- Writing paragraphs, a hero, feature cards, or a CTA, or rewriting a sentence that fails a copy test → `references/copy.md`
- Building a chart, plot, or data visualization → `references/charts.md`
- Producing a slide deck (HTML or pptx) → `references/decks.md`
- Building any component (callout, badge, stat grid, worked example, decision row, sparkline table, code block, dialog) → `references/components.md`
- Writing CSS for an HTML or React page, including controls, overlays, motion timing, interaction states, icons, or a code block → `references/ui-tokens.md`
- Needing placeholder data or demo copy for a slide or artifact → `references/sample-content.md`
- Adding a geometric drawing to a slide or panel, either as a large labeled figure or as faint decoration → `references/geometry.md`
- Drawing an SVG diagram or a pptx slide, or placing HTML elements by coordinates → `references/layout.md`

## Before you build

Run this checklist before writing any code or markup.

1. **Job.** Decide what the artifact is for. An artifact can teach a mechanism, summarize evidence, serve as a reference, walk through a process, or support a decision. The answer decides the background color and how much content each panel holds.
2. **Composition mode.** Pick one mode from the list below.
3. **Ink panels.** Decide which panels or slides use ink, or decide that none do, before you start.
4. **Logo shape.** Pick a simple line drawing whose form matches the structure of the subject.
5. **Layout.** For a diagram or slide, write the node and arrow lists from `references/layout.md` before any coordinates.
6. **For decks:** before writing any slide, identify which slides need interactivity. Choose the interaction type to fit the concept. See `references/decks.md`.

## Composition modes

Pick one mode per artifact. The mode sets the layout, the density, and where ink goes.

**Dense reference.** A dense reference is a grid of cards with high information density, several columns, and multiple KV pairs per section. Each panel has enough content for 30–45 seconds of reading. Use it for protocol references, parameter tables, specification sheets, and side-by-side comparisons. Use ink panels only to highlight a measurement or a finding on a page that is mostly paper.

**Spacious argument.** A spacious argument puts one concept in each section, with generous white space around every panel or slide. The reader moves through it slowly. Use it when the artifact covers one deep concept, such as a derivation, a worked example, or an analysis. Ink appears only at summary or decision points.

**Ink-anchored.** Most of the artifact is paper, and its ink panels serve as section dividers, quoted measurements, and decisions. Use this mode for reference decks with several sections.

**Ink-forward.** Most panels are ink. The artifact mostly states conclusions and explains less. Use this mode for summary dashboards, executive snapshots, decision panels, and final-state reference cards. Use a paper panel only as a break for relief or sharp contrast, such as a table to read closely or a diagram that needs white space.

**Diagram-led.** A chart, diagram, or animation takes up most of each panel, and text serves as annotation and labels. Use it when the concept is spatial or relational, as in network topologies, signal flows, state machines, and data distributions. Use cards and KV pairs only to support the diagram.

## Variation

When this session already produced an artifact, give the new one a different composition mode, different ink panels, and a different logo shape. A new deck also uses a different opening pattern and a different interaction type from `references/decks.md`.

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
- **Casing:** Write section labels as eyebrows, in UPPERCASE with 0.12em letter-spacing. Write headings and body text in sentence case. Never use Title Case. Write tokens in all-lowercase (`$toby-paper`).

## Motion

- Use only these motions: an opacity fade, a 4–8px positional slide for menus and toasts, and a hairline ring on focus. An accordion can also rotate its chevron 90° when it opens.
- Do not use spring bounces, scale-up entrances, parallax, particle effects, or animation that only decorates. An animation that the reader can step through or pause counts as content, so it is allowed.

## Imagery + backgrounds

- Paper is the background. Artifacts use no imagery by default.
- Avoid generic lifestyle photos, decorative stock art, repeating patterns, textures, and gradients. Use real or generated imagery when the task requires the reader to see what the product, place, object, state, gameplay, or person looks like.
- Do not use emoji or unicode dingbats. The allowed unicode characters are `→` for handoffs, `·` as a metadata separator, and `±` for uncertainty.

## Logos

Each artifact gets its own logo, built from three parts:

- A simple geometric drawing made of hairlines.
- One short lowercase word for the topic, in Inter at weight 600.
- A single red dot as the only color.

**Choose the drawing for the structure of the subject.** Use a crosshair or grid for a network topology, nested squares for a recursive algorithm, and an orbit arc for an antenna or wave. Use branching lines or a Y-fork for a decision process, and a horizontal rail with a tick for a time series. Use a bell curve outline for a probability distribution, and stacked horizontal bars for a queue or pipeline. Use a partial orbit arc for a rotation or cycle, because readers take a closed circle as decoration. Use a 3×3 grid of squares for matrix or table data.

Do not use an orbit for every subject, a triangle only because it is geometric, or a square only because it is simple. If you cannot explain why the shape fits the subject, pick a different shape.

## Purpose check

Remove a panel or slide that does none of these jobs:

- teach a concept
- state a measurement
- define a term
- list a constraint
- show one step of a worked example
- ask a question for the reader to answer before reading on

## Output types

- **HTML or React:** apply the tokens above, and load Inter and JetBrains Mono from Google Fonts with system fallbacks. Set the page to `--toby-paper` and cards to `--toby-paper-3` with a 1px `--border-hairline` ring.
- **SVG or HTML widget from the visualize tool:** call `visualize:read_me` first. Then replace the CSS variables that `read_me` returns with these tokens. Keep the background transparent. When the widget needs a paper background, fill a top-level `<rect>` or a wrapper element with `--toby-paper`.
- **pptx or HTML deck:** follow `references/decks.md`. The pptx skill handles the file.

## Copy rules

Run four tests on every sentence of artifact copy, and rewrite or cut each sentence that fails one. `references/copy.md` has a passing and a failing example for each.

1. **Cite.** The claim states its source, measurement, or mechanism.
2. **Negation.** Write the opposite of the claim. The sentence passes only when someone could write that opposite and mean it.
3. **Substitution.** Replace the subject with an unrelated noun. The sentence passes only when the result is nonsense.
4. **Reader-skim.** The sentence passes only when a reader who knows the material would lose something if the sentence were cut.

Give every number a unit. Put each caveat and each assumption next to the claim it qualifies, never in a footnote.
