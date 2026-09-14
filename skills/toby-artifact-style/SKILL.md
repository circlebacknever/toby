---
name: toby-artifact-style
description: Apply Toby's artifact design system whenever a visual artifact is being produced — an HTML or React page or widget, an SVG or HTML widget, a diagram, image, graphic, chart, dashboard, slide deck, mockup, printable reference card, or the copy inside one. Trigger when the user asks for a visual, including a visual to teach or explain something — draw it, show it, make a diagram, build a chart, sketch a graphic. Do not trigger for a plain text answer or explanation in chat where no visual was asked for; that prose belongs to toby-explain or toby-learning.
---

# Toby Artifact Style

Make every artifact under this system look like it was made for this exact content, in every session.

Toby Artifact Style fixes the tokens, copy constraints, and visual rules, and it leaves structural choices open. Choose the structure for each artifact. A structure can be a dense reference card, a spacious single claim, an ink-heavy authority piece, or a paper-first page for reading. It can also be an animated process, a static evidence panel, a three-slide lesson, or a twenty-slide reference deck.

If you are about to reuse the layout you built last time, stop and pick a different one. Reused layouts lead to convergence, where every artifact looks like every other artifact. The fixed tokens, copy rules, and visual rules keep quality consistent. Within those rules, vary every other part of the structure.

## Three principles

**Work goes on paper.** `--toby-paper` (`#fdfaf1`) is the default surface. Use paper for panels where the reader reads, compares, and parses content.

**Dark means judgment.** Use `--toby-ink` (`#1a1c1f`) for decision panels, evidence panels, summaries, and section dividers. An ink panel tells the reader that the artifact states a judgment at that point. Reserve ink for those points, because an artifact that uses ink everywhere marks no panel as a judgment.

**Red marks consequence.** Use `--toby-accent` (`#c44e3f`) for risk, breach, finality, and threshold violation. Never use red as a brand accent or for plain emphasis. Keep it rare, because readers stop noticing a red that shows up often.

## Six visual moves that make Toby Artifact Style coherent

If a panel uses none of these patterns, ask whether the artifact needs that panel.

1. **Tinted state families.** When a panel expresses a state (info / stable / watch / consequence / unknown), give it the three-step palette: pale background, mid-saturation border, dark saturated text. The three colors make the whole panel read as one color family. See "Callout philosophy" below. This tinted state family is the foundational pattern.
2. **Categorical section accents.** When a page has multiple sections, give each its own color from the chart palette. The accent shows up as the section number, the bottom-rule strip under the heading, and small cell-id pills.
3. **Mono values, sans labels.** Set every number, ID, timestamp, or coordinate in JetBrains Mono with tabular numerals, and set every label and description in Inter. The alternation between the two typefaces is part of the system's recognizable look.
4. **Hairline rules and small radii.** Use 1px hairlines for almost every divider. Cards stay at 12px radius, and only outer containing frames get 18px.
5. **Density over whitespace.** Build slides and dashboards dense, with multiple KV pairs, stat grids, sparkline-in-table cells, and evidence rows. Treat the reader as a serious professional reviewing evidence, because dense panels make the artifact look authoritative.
6. **Three-tone progression for narrative blocks.** When a panel shows a chain of reasoning, tint its rows in order: setup (info teal) → working (watch amber) → conclusion (stable green). The Worked Example component uses this progression, and other reasoning panels can use it too.

## Teaching decks — only when asked

Build a Toby Artifact Style HTML deck (paginated, prev/next, React `.jsx`) only when the user has asked for a produced artifact, deck, or slides. A lesson, walkthrough, or explanation in conversation stays in chat, because toby-explain and toby-learning own those answers and write them in prose. Once a deck has been asked for, apply artifact copy rules to its copy.

Split the content between the deck and chat as follows.
- **Deck (artifact):** put the glossary, mechanism explanations, tables, diagrams, derivations, examples, and summary in the deck.
- **Chat:** put a short framing line, the comprehension check question, and any branch options in chat.

Let the slide count grow with the material, and keep the deck to the smallest count that still teaches the whole concept. If the material needs 18 slides, build 18.

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
2. **Composition mode.** Pick one mode from the list below, and make it different from the mode you used last time.
3. **Ink allocation.** Decide before you start which panels or slides use ink and which use paper, so that no panel ends up in ink by accident.
4. **Logo primitive.** Name the shape. It should hint at the structure of the subject.
5. **For decks:** before writing any slide, identify which slides need interactivity. Choose the interaction type to fit the concept. See `references/decks.md`.

## Composition modes

Pick one mode per artifact, and vary the mode across sessions. The mode determines the layout logic, the density, and how ink and paper are distributed.

**Dense reference.** A dense reference is a grid of cards with high information density, several columns, and multiple KV pairs per section. Each panel has enough content for 30–45 seconds of reading. Use it for protocol references, parameter tables, specification sheets, and side-by-side comparisons. Ink panels appear as evidence callouts inside a paper field.

**Spacious argument.** A spacious argument puts one concept in each section, with generous white space around every panel or slide. The reader moves through it slowly. Use it when the artifact covers one deep concept, such as a derivation, a worked example, or an analysis. Ink appears only at summary or decision points.

**Ink-anchored.** Paper is the default surface, and ink panels break up the paper at section dividers, quoted measurements, and named decisions. The artifact is mostly paper, and the ink panels mark the points where it states a judgment. It works well for reference decks with multiple sections.

**Ink-forward.** Most surfaces are ink, and paper appears only for relief or sharp contrast. The artifact asserts more than it explains. Use it for summary dashboards, executive snapshots, decision panels, and final-state reference cards. Use a paper panel only as an interruption, such as a table that needs reading or a diagram that needs white space.

**Diagram-led.** A chart, diagram, or animation takes up most of each panel, and text serves as annotation and labels. Use it when the concept is spatial or relational, as in network topologies, signal flows, state machines, and data distributions. Cards and KVs are secondary.

## Variation mandate

Follow these rules so that artifacts do not converge on one look.

- **Never use the same overall composition twice in a session.** If the last artifact was dense reference, this one is spacious argument or diagram-led.
- **Vary ink allocation.** An artifact can be mostly paper with one or two ink evidence panels, ink-forward with paper used for contrast, or free of ink. Rotate among these three allocations across artifacts.
- **Vary information density.** A lesson on a single formula can take three spacious slides. A reference card on a protocol stack should be dense enough for sustained study. Do not give every artifact the same density.
- **Choose the logo primitive for the subject's structure.** See the logos section below. Using the same orbit shape on every artifact breaks this rule.
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

Every semantic hue has a three-step palette. Use the three steps together whenever a component expresses a state, as in alerts, toasts, status pills, badges, callouts, worked-example rows, and KPI accent stripes. The whole component then reads as one color family.

```css
/* soft = pale bg · tint = mid border · text = saturated dark fg */
--toby-info-soft:    #e2e9ea;  --toby-info-tint:    #bfcdce;  --toby-info-text:    #2c3a3a;
--toby-stable-soft:  #e3ecd5;  --toby-stable-tint:  #bcc89e;  --toby-stable-text:  #2d4818;
--toby-watch-soft:   #f1e6d2;  --toby-watch-tint:   #d6c19a;  --toby-watch-text:   #5a431d;
--toby-cons-soft:    #f6e2dc;  --toby-cons-tint:    #e9b7ad;  --toby-cons-text:    #7a2d22;
--toby-unknown-soft: #ebe8e3;  --toby-unknown-tint: #c4bfb6;  --toby-unknown-text: #3f3d39;
```

A state-tinted panel uses `*-soft` for the background, `*-tint` for the border, the un-soft hue for the 4px left strip, and `*-text` for the text. See `references/components.md` for paste-ready HTML.

## Color rules

- Do not use gradients, rainbow scales, glow, or colored shadows.
- Do not use red as a brand accent. Use ink weight, a hairline, or position for emphasis.
- The chart palette is positional, so use its colors in fixed order by series index. The same palette sets the section accents on long pages.
- **Do not give cards a colored left accent** as general decoration, because readers recognize that accent as a sign of AI-generated design. Alerts and toasts are the exception, because their single 4px coloured left strip from the callout family is the documented pattern.

## Typography

- **Sans:** Use Inter at weights 400, 500, and 600, with the system sans font as the fallback.
- **Mono:** Use JetBrains Mono at weights 400 and 500 for values, units, IDs, and coordinates.
- **Sizes:** display 34 · h1 28 · h2 22 · section 18 · body 14 · body-sm 13 · meta 12 · eyebrow 11 · mono 13. The sizes are in px on the web, so convert them to Pt for pptx.
- **Weights:** Use 400 for body, 500 for emphasis, and 600 for headings. Do not use 700 in product UI.
- **Letter-spacing:** Use 0 on display text, headings, and body, and use +0.12em on eyebrows only.
- **Numerals:** Use tabular numerals (`tnum`) everywhere.
- **Casing:** Use UPPERCASE eyebrows (tracked 0.12em) for section labels and sentence case for headings and body. Never use Title Case. Write tokens in all-lowercase (`$toby-paper`), and set values, IDs, and coordinates in mono.

## Spacing — all multiples of 4

Prefer named tokens. When no token matches exactly, pick the closest one, and never use a one-off value.

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

- Use only these motions: an opacity fade, a 4–8px positional slide for menus and toasts, and a hairline ring on focus. An accordion can also rotate its chevron 90° when it opens.
- Do not use spring bounces, scale-up entrances, parallax, particle effects, or animated illustrations.

## Interaction states

- **Hover (paper):** The background changes to `--toby-paper-2`, and the foreground stays the same.
- **Hover (dark):** The background lightens to `--ink-hover` (`#4a4e57`), and the text stays the same.
- **Active / press:** The background turns DARKER (`--surface-pressed` / `--ink-pressed` / `--accent-pressed`), and the border stays. The control does NOT shrink or move.
- **Focus:** Draw a 2px outside ring in `--toby-info` (teal) at a 2px offset. **Never use red.**
- **Selected / current in lists/trees/menus:** Use a `--toby-paper-2` background with a 3px `--toby-info` inset on the left. Paper-3 against paper-3 is INVISIBLE, so never use paper-3 as a selection state.

Hover and base must differ by ≥ 3:1 contrast (WCAG 1.4.11).

## Imagery + backgrounds

- Paper is the background, and artifacts use no imagery by default.
- Avoid generic lifestyle photos, decorative stock art, repeating patterns, textures, and gradients. Use real or generated imagery when the task requires the product, place, object, state, gameplay, or person to be inspectable.
- Geometry as decoration is allowed only when it clarifies the content. Use it at one of two scales. A **primary** mark appears at content size with a small uppercase label, and a **decorative** mark is small (≤ 80px) and faint (opacity ≤ 0.25). See `references/geometry.md` for the named marks.

## Iconography

- Use Lucide where available. Inline SVG is acceptable for static artifacts. Use the app's icon library for coded frontends when one exists. Draw icons at 16–20px with a 1.5px stroke, square caps, and monochromatic `currentColor`.
- Heroicons-outline, Tabler, and Phosphor-regular are acceptable fallback families. Material Icons and Carbon are too dense, so do not use them.
- Keep the system to about 12 glyphs. If you need a 13th, use a text label.
- Do not use emoji or unicode dingbats. The allowed unicode characters are `→` for handoffs, `·` as a metadata separator, and `±` for uncertainty.

## Logos / wordmarks

Each artifact gets its own logo or wordmark, and no fixed brand applies across artifacts.

Each artifact gets:
- A hairline geometric primitive.
- One short lowercase Inter-600 word naming the topic.
- A single red dot as the only color.

**Choose the primitive for the structure of the subject.** Use a crosshair or grid for a network topology, nested squares for a recursive algorithm, and an orbit arc for an antenna or wave. Use branching lines or a Y-fork for a decision process, and a horizontal rail with a tick for a time series. Use a bell curve outline for a probability distribution, and stacked horizontal bars for a queue or pipeline.

Refuse these lazy defaults: an orbit for everything, a triangle because it is geometric, and a square because it is simple. If you cannot name why the shape fits the subject, pick a different shape.

## Purpose check

Every sentence, panel, or slide must do one of the jobs below. If it does none of them, remove it.

- teach a concept
- state a measurement
- define a term
- list a constraint
- walk a worked step
- pose a question that gates the next sentence

## Output-type mapping

### HTML / React artifacts
- Apply all tokens above. Set the background to `--toby-paper`, and set cards to `--toby-paper-3` with a 1px `--border-hairline` ring.
- Load Inter and JetBrains Mono via CDN. Provide system fallbacks.
- Always set numerals to tabular with `font-variant-numeric: tabular-nums;`.

### Visualizer SVG diagrams
- Call `visualize:read_me` first, then override its CSS variables with Toby Artifact tokens before generating output.
- Visualizer requires a transparent background, so if you want a paper field, set the paper color on a top-level `<rect>`.
- Use the Toby Artifact chart palette in positional order for any series.

### Visualizer HTML widgets
- Call `visualize:read_me` first, then override its CSS variables with Toby Artifact tokens.
- Keep the background transparent, and if the widget needs paper, apply Toby Artifact paper through a wrapper.

### pptx slide decks
- See `references/decks.md`. The pptx skill handles the file mechanics, and Toby Artifact controls colors, fonts, sizes, padding, and slide structure.

### HTML decks for teaching
- See `references/decks.md`. Build a React `.jsx` artifact with prev/next pagination and keyboard navigation.

## Copy rules

Every sentence in artifact copy must pass the **cite**, **negation**, and **substitution** tests, and then stay in after the **reader-skim** cut. `references/copy.md` defines all four.

The banned words are in the operating guide, which is already loaded. This skill adds none.

**Slide and chart titles state the claim in a plain, descriptive sentence.** A section heading is a one- or two-word label or a phrase that says what the section covers. The body explains or qualifies. Put caveats next to the claim, never in a footnote.

**Every number has a unit.** A bare number is a defect.

The clarity rules apply most strictly to labels. An axis title, a legend entry, a KPI caption, and a slide heading each get the three-word cap on noun stacks. Each also gets one name per thing, held identical across every chart in the artifact.

Toby's global voice rules control register. This skill controls artifact structure, visual tokens, density, copy tests, and component patterns.

For any substantive copy work, load `references/copy.md`.
