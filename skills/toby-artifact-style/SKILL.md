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

Apply these color tokens, typography rules, composition modes, and copy tests to every visual artifact.

## Terms

- **Paper** (`--toby-paper`, `#fdfaf1`) is the warm cream default background for reading text, comparing values, and inspecting details.
- **Ink** (`--toby-ink`, `#1a1c1f`) is the near-black background reserved for decision panels, evidence summaries, and section dividers.
- **Red** (`--toby-accent`, `#c44e3f`) marks only a risk, a broken limit, a value past its threshold, an irreversible action, and the single dot in the artifact logo.
- **Hairline** is a 1px border or divider (`--border-hairline`), paired with a 12px card radius (18px only on an outer frame).
- **Eyebrow** is an 11px UPPERCASE label with `+0.12em` letter-spacing above a heading or value.
- **KV pair** is a mono eyebrow label paired with a tabular-numeral value, and a **Sparkline** is an axis-free inline trace (`80–120px`) inside a table cell or stat card.
- **Status colors** are the five semantic families (`info`, `stable`, `watch`, `cons`, `unknown`), each with `-soft` (background), `-tint` (border), and `-text` (foreground) tokens.

## Visual patterns

1. **Status panels.** Give a status panel its family's `-soft` background, `-tint` border, `-text` foreground, and a 4px left strip in the family's main color (`--toby-watch`). Never put a decorative left stripe on a non-status card.
2. **Section accents.** When a page has multiple sections, assign each section one color from the chart palette in order for its section number, heading rule, and cell pills.
3. **Density.** Fill reference slides and dashboards densely with KV pairs, stat grids, and sparkline tables unless using the spacious argument mode.
4. **Three-step reasoning tint.** In a Worked Example or reasoning chain, tint starting premises with `info-soft`, derivation steps with `watch-soft`, and the conclusion with `stable-soft`.

## Reference files

Open the reference file that matches the artifact:

- Paragraphs, heroes, feature cards, CTAs, or copy rewrites: `references/copy.md`
- Charts, plots, or data visualizations: `references/charts.md`
- Slide decks (HTML React or `.pptx`): `references/decks.md`
- UI components (callouts, pills, stat grids, worked examples, decision rows, sparkline tables, code blocks, dialogs): `references/components.md`
- CSS controls, overlays, motion timing, focus states, or syntax tokens: `references/ui-tokens.md`
- Placeholder domain data or demo copy: `references/sample-content.md`
- Geometric marks at content or decorative scale: `references/geometry.md`
- SVG diagrams, `.pptx` coordinates, or box/arrow layout checks: `references/layout.md`

## Before you build

Complete these six decisions before writing markup or code:

1. **Job:** decide whether the artifact teaches a mechanism, summarizes evidence, serves as a reference, walks through a process, or supports a decision.
2. **Composition mode:** pick one of the five modes below.
3. **Ink panels:** choose which panels or slides use ink before starting.
4. **Logo mark:** pick a geometric hairline mark that matches the subject's structure.
5. **Layout:** for diagrams or coordinate slides, write the node and arrow lists from `references/layout.md` before choosing coordinates.
6. **Deck interactivity:** for decks, pick the opening pattern and which slides use interactive controls (`references/decks.md`).

## Composition modes

Pick one mode per artifact, and switch the mode, ink placement, and logo mark when building a second artifact in the same session:

- **Dense reference:** multi-column card grids with KV pairs and tables on paper, using ink only to highlight a key measurement or decision.
- **Spacious argument:** one concept per section with generous whitespace for derivations or worked examples, using ink only at summary or decision points.
- **Ink-anchored:** mostly paper panels with ink panels serving as section dividers, quoted measurements, and decisions.
- **Ink-forward:** mostly ink panels stating conclusions for executive snapshots or final-state cards, using a paper panel only for a dense table or diagram.
- **Diagram-led:** a chart, diagram, or simulation fills most of the canvas, with text limited to annotations and compact KV cards.

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

/* Chart palette in positional order */
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

## Typography, motion, and imagery

- **Typography:** use Inter (`400` body, `500` emphasis, `600` headings, never `700`) and JetBrains Mono (`400`, `500`) with `tabular-nums` everywhere. Standard px sizes are `display 34`, `h1 28`, `h2 22`, `section 18`, `body 14`, `body-sm 13`, `meta 12`, `eyebrow 11`, and `mono 13` (deck slide titles scale with `references/decks.md`). Use sentence case for headings and body text, and UPPERCASE with `+0.12em` tracking only on eyebrows.
- **Color and motion:** never use gradients, rainbow scales, glow, colored shadows, spring bounces, scale entrances, or decorative animation. Use only opacity fades, 4–8px menu/toast slides, focus rings, chevron rotation, and user-controlled simulation steps.
- **Imagery and symbols:** default to paper without stock photos or textures. Never use emoji or dingbats. The allowed symbols are `→` (handoff), `·` (separator), and `±` (uncertainty).

## Logos

Build each artifact's logo from three parts: a 1px hairline geometric mark, one lowercase word for the topic in Inter 600, and a single `--toby-accent` red dot.

Match the mark to the subject's structure (`references/geometry.md`): a grid or crosshair for a network, nested squares for recursion, a partial orbit arc for a cycle, a Y-fork for a decision tree, a ticked rail for a time series, a bell curve for a distribution, or stacked bars for a queue. If you can't state why the mark fits the subject, pick another mark.

## Purpose and output types

Remove any panel or slide that doesn't teach a concept, state a measurement, define a term, list a constraint, show a worked step, or ask a check question.

- **HTML or React:** load Inter and JetBrains Mono from Google Fonts with system fallbacks. Set the page to `--toby-paper`, and set cards to `--toby-paper-3` with a 1px `--border-hairline` border.
- **SVG or HTML widget (`visualize` tool):** call `visualize:read_me` first, replace its CSS variables with these tokens, and fill a top-level `<rect>` or wrapper with `--toby-paper` when a background is needed.
- **Decks (`.pptx` or HTML):** follow `references/decks.md`.

## Copy rules

Check every sentence of artifact copy against the four tests in `references/copy.md`:

1. **Cite:** state the source, measurement, or mechanism.
2. **Negation:** the opposite of the claim must be a meaningful statement someone could argue for.
3. **Substitution:** replacing the subject with an unrelated noun must make the sentence nonsense.
4. **Reader-skim:** cut any sentence a knowledgeable reader could skip without losing information.

Give every number a unit, and place every caveat and assumption right next to the claim it qualifies.
