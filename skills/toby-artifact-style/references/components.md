# Toby Artifact components

Load this file when you build any component for a Toby Artifact Style artifact. The components include callouts, alerts, badges, status pills, stat grids, worked examples, decision rows, sparklines in tables, code blocks, dialogs, treeviews, and equation blocks.

## Signature patterns

When a request matches one of these patterns, USE it. These patterns give a Toby Artifact Style artifact its recognizable look.

- **Callout / Alert / Toast** — This state-tinted panel uses the soft / tint / text family. It has a bold title above a body at opacity 0.88.
- **StatusPill** — This pill is fully tinted by hue and shows live system state with a dot and a label.
- **Badge** — This compact mono chip holds a count or a token. Its variants are ink (default), info, stable, watch, and cons.
- **StatGrid (KPI grid)** — The grid has 3 or 4 columns with hairline dividers. Each cell's 2px top accent strip takes the next color in the chart palette.
- **Worked Example** — This example has three rows in order: PREMISE (info-tinted), DERIVATION (watch-tinted), and RESULT (stable-tinted).
- **Decision Row** — The row holds a title, meta text, and Approve / Hold / Reject buttons in matching semantic colors.
- **Sparkline-in-table** — embed an 80–120px trace SVG in a table cell. Add adjacent columns for Last and Δ%.
- **Code block** — This DARK-theme block has an ink-2 background, mono text, a line gutter, a copy button, and syntax classes (kw / num / str / com).
- **Treeview** — Each level has a hairline rule down its left side. The selected row uses paper-2 with a 3px info inset.
- **Annotation pin** — The pin is a numbered circle, a leader line, and a framed label, all in `--toby-info`.
- **Equation block** — The block shows a centered mono formula with a 2px info-colored top accent.
- **Dialog · alert variant** — adds a 4px red top strip and a red title. It is only for irreversible actions.

---

## Full component vocabulary

Beyond the signatures above, Toby Artifact ships ~60 components total.

### Layout & structure
- **Topbar** — This 56px-tall header has a breadcrumb, an optional id stamp, and right-aligned actions.
- **Sidebar** — The sidebar is a grouped vertical nav. The selected row uses `--toby-paper-2` with a 3px `--toby-info` left inset, and never paper-3.
- **Panel** — This content card has an eyebrow, a title, and actions. Its variants are `default` (lifted), `flush` (paper-toned), and `authority` (ink-toned).
- **Tabs** — The active tab has an info-soft tint and a 3px `--toby-info` underline.
- **Accordion** (covers Collapsible) — Only one section opens at a time by default, but passing `multi` lets multiple sections open.
- **Toolbar** — The toolbar is an inline strip of mini-controls. `.toolbar__btn--on` fills with ink + `--text-on-dark`.
- **Pagination** — It uses 32px mono cells with tabular numerals. Ellipses stay when the range overflows.
- **Breadcrumb** — slash-separated trail. Its last item is the current page and has no link styling.

### Form controls
- **Button** — Its variants are `default` (paper), `primary` (ink), `ghost` (transparent), and `consequence` (accent). `--sm` sets a 28px height.
- **Input** — An input is 36px tall, with an info-teal focus ring at a 2px offset.
- **Textarea** — A Textarea is a multi-line Input. Its optional `maxLength` shows a mono character count at the bottom right.
- **Number field** — The field has mono digits with tabular numerals and stacked +/− buttons on the right. The native browser spinners are hidden.
- **OTP field** — The field has N mono slots (default 6) with an optional `groupAt` separator. Backspace moves to the previous slot.
- **Checkbox** + **CheckboxGroup** — The group has a `row` modifier for inline layout.
- **Radio** + **RadioGroup** — They are built the same way as Checkbox.
- **Switch** — Switch is an alias of **Toggle**, so both names refer to one primitive.
- **Toggle** — The toggle is a 36×20 track with a thumb. When on, the track is ink and the thumb is paper.
- **Slider** — It shows a mono value with tabular numerals to the right of the label.
- **ToggleGroup** — A ToggleGroup is a segmented control. `.tgrp__btn--on` fills with ink + white. Buttons use `white-space: nowrap`.
- **Combobox** (covers **Select** and **Autocomplete**) — It is searchable by default, but `searchable={false}` gives a plain Select.
- **Calendar** — Today gets a 2px `--toby-info` border, bold weight, and info text. The selected day fills with ink. Marked dates show a small red dot.
- **DatePicker** — It is a Calendar inside a popover. Its trigger shows the selected date in ISO format in mono.
- **Field / Label / Fieldset** — These are wrappers for form structure.

### Overlays & menus (consolidated)
- **Dialog** (covers **Modal** and **AlertDialog**) — It shows a centred panel over a backdrop. `kind="alert"` adds a 4px red top hairline and a red title.
- **Sheet** (covers **Drawer** and **Bottomsheet**) — `side="right" | "left" | "bottom"`. The bottom variant has a drag grip.
- **Popover** — This click-anchored panel has 16px padding. It closes on a click outside it.
- **Tooltip** — This dark ink panel appears only on hover. It has a caret and is always placed above the trigger.
- **PreviewCard** — This hover card holds more than a tooltip but less than a popover.
- **Menu** — This popover menu primitive has group labels, hint shortcuts (`⌘C`, `↵`), separators, and a `danger` variant.
- **ContextMenu** — It is a wrapper around Menu for right-click.
- **Menubar** — It is a horizontal strip with File / Edit / View. The `--open` state uses paper-2 and a 2px info underline.
- **NavigationMenu** — It is like Menubar, but it has rich panels. Each panel gets a 2px info top border.
- **Command palette** — It is a full-screen search with grouped items and a keyboard footer.
- **Toast** — Toasts stack at the bottom right and dismiss themselves after ~4s. Each toast has a semantic left border and a soft tinted background.

### Display & feedback
- **Avatar** — It shows initials only, with no faces and no abstract art. The sizes are sm (22), md (28), and lg (40). The `--ink` variant has a dark fill.
- **Badge** — see Signature.
- **Kbd** — It shows a mono keyboard glyph with a 2px bottom border, so it looks pressable.
- **Spinner** — It is a 1.5px ring with a 720ms linear spin and no glow. The sizes are md (16) and lg (22).
- **Skeleton** — It is a shimmer placeholder. Its kinds are `line` (12px), `title` (18px), and `block` (64px).
- **Progress** — It is a 4px linear bar whose semantic kinds match the state hues. An `indeterminate` kind is also available.
- **Meter** — It is a progress bar with a min/max axis and an optional consequence-red threshold mark.
- **Separator** — It is `horizontal` (1px hairline) or `vertical` (1px column). The `strong` modifier uses `--border-strong`.
- **Empty state** — It has a dashed hairline border, an info-teal geometric icon, a title, a body, and an optional action.

### Data display
- **Metric** — It has a label, a big numeric value, a unit suffix, an optional rail (progress strip), and an optional target line.
- **KV** — It is a two-column definition list. The term appears on the left as an uppercase mono-tracked eyebrow. The value appears on the right in mono with tabular numerals.
- **EvidenceTable** — It is `.tbl`, with the `.num` class for right-aligned mono columns. The header uses a `--border-strong` divider.
- **Sparkline** — It is an inline trace SVG (80–120px wide). Use it as a table cell, a KV value, or a stat-card adornment.

---

## Consolidation rules

Each problem has one primitive, which can have several names. Do not invent a separate component when an existing primitive already covers the case.

| Names that map to one primitive | Primitive | Differentiator |
|---|---|---|
| Modal, AlertDialog, Dialog | `Dialog` | `kind="default" \| "alert"` |
| Drawer, Bottomsheet, Sheet | `Sheet` | `side="right" \| "left" \| "bottom"` |
| Select, Autocomplete, Combobox | `Combobox` | `searchable={true \| false}` |
| Switch, Toggle | `Toggle` | (alias) |
| Collapsible, Accordion | `Accordion` | `multi={true \| false}` |
| Form-checkbox-list, Checkbox group | `CheckboxGroup` | wraps `Checkbox` |
| Form-radio-list, Radio group | `RadioGroup` | wraps `Radio` |
| ContextMenu, Menu, Menubar | `Menu` primitive | each wrapper uses a different trigger |

---

## Paste-ready starter HTML

Every value below references tokens defined in SKILL.md. Change the copy, but never change the structural classes.

### Callout / Alert / Toast — state-tinted panel

```html
<div class="alert alert--watch">
  <div>
    <div class="alert__title">Watch · retry pressure</div>
    <div class="alert__body">Retry volume is 18% above baseline. The two-sample rule has not tripped yet.</div>
  </div>
  <button class="alert__close" aria-label="Dismiss">×</button>
</div>
```

```css
.alert {
  display: flex; gap: 12px; padding: 12px 16px;
  border: 1px solid var(--border-hairline);
  border-left: 4px solid var(--text-muted);
  background: var(--surface-card);
  border-radius: var(--radius-base);
  font-size: 13px; line-height: 1.55;
}
.alert--info   { background: var(--toby-info-soft);   border-color: var(--toby-info-tint);   border-left-color: var(--toby-info);   color: var(--toby-info-text); }
.alert--watch  { background: var(--toby-watch-soft);  border-color: var(--toby-watch-tint);  border-left-color: var(--toby-watch);  color: var(--toby-watch-text); }
.alert--cons   { background: var(--toby-cons-soft);   border-color: var(--toby-cons-tint);   border-left-color: var(--toby-accent); color: var(--toby-cons-text); }
.alert--stable { background: var(--toby-stable-soft); border-color: var(--toby-stable-tint); border-left-color: var(--toby-stable); color: var(--toby-stable-text); }
.alert__title { font-weight: 600; margin-bottom: 4px; color: inherit; }
.alert__body  { color: inherit; opacity: 0.88; }
.alert__close { margin-left: auto; background: none; border: none; cursor: pointer; color: inherit; opacity: 0.6; font-size: 16px; padding: 0 4px; }
```

The same `--*-soft / --*-tint / --*-text` triple sets the colors for status pills, badges, toasts, and worked-example rows. Build new state-tinted patterns the same way.

### Status pill — dot + label

```html
<span class="pill pill--watch">Watch +18%</span>
```

```css
.pill { display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px;
  border-radius: 999px; font-size: 12px; font-weight: 500;
  border: 1px solid; white-space: nowrap; }
.pill::before { content: ''; width: 6px; height: 6px; border-radius: 50%; }
.pill--watch { background: var(--toby-watch-soft); border-color: var(--toby-watch-tint); color: var(--toby-watch-text); }
.pill--watch::before { background: var(--toby-watch); }
/* Repeat for --info / --stable / --cons / --unknown with the matching family. */
```

### Stat grid — KPI cells with cycling accent stripes

```html
<div class="stat-grid stat-grid--4">
  <div class="stat">
    <div class="stat__label">DRIFT (OBSERVED)</div>
    <div><span class="stat__value">0.31</span><span class="stat__unit">°C/orbit</span></div>
    <div class="stat__delta stat__delta--up">▲ +0.03 °C · vs 24h ago</div>
    <div class="stat__source">Sensor S-1 · n=240</div>
  </div>
  <!-- Repeat .stat for each cell. Use 3 or 4 columns in total. -->
</div>
```

```css
.stat-grid { display: grid; border: 1px solid var(--border-hairline);
  border-radius: var(--radius-base); background: var(--surface-card); overflow: hidden; }
.stat-grid--3 { grid-template-columns: repeat(3, 1fr); }
.stat-grid--4 { grid-template-columns: repeat(4, 1fr); }
.stat { padding: 20px; border-right: 1px solid var(--border-hairline);
  display: flex; flex-direction: column; gap: 8px; position: relative; }
.stat::before { content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 2px; background: var(--stat-accent, transparent); }
.stat:nth-child(4n+1) { --stat-accent: var(--toby-info); }
.stat:nth-child(4n+2) { --stat-accent: var(--toby-stable); }
.stat:nth-child(4n+3) { --stat-accent: var(--toby-watch); }
.stat:nth-child(4n+4) { --stat-accent: var(--toby-slate-blue); }
.stat__label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--text-muted); font-weight: 600; }
.stat__value { font-size: 28px; font-weight: 600; font-feature-settings: 'tnum';
  letter-spacing: -0.012em; line-height: 1.1; }
.stat__unit { font-family: var(--font-mono); font-size: 12px;
  color: var(--text-muted); margin-left: 4px; }
.stat__delta { font-family: var(--font-mono); font-size: 12px; }
.stat__delta--up { color: var(--toby-stable); }
.stat__delta--down { color: var(--toby-accent); }
.stat__delta--flat { color: var(--text-muted); }
.stat__source { font-family: var(--font-mono); font-size: 11px;
  color: var(--text-muted); margin-top: 4px; }
```

### Worked Example — three-row tinted progression

```html
<div class="worked">
  <div class="worked__row worked__row--premise">
    <div class="worked__step">PREMISE</div>
    <div class="worked__body">The period of a circular orbit follows Kepler's third law: T² ∝ a³, with μ = 3.986 × 10¹⁴ m³/s².</div>
  </div>
  <div class="worked__row worked__row--derivation">
    <div class="worked__step">DERIVATION</div>
    <div>
      <div class="worked__body">Substitute a = R_⊕ + h with R_⊕ = 6371 km and h = 420 km.</div>
      <div class="worked__math">T = 2π √(a³ / μ)</div>
    </div>
  </div>
  <div class="worked__row worked__row--result">
    <div class="worked__step">RESULT</div>
    <div>
      <div class="worked__body">The orbital period is approximately 92.8 minutes.</div>
      <div class="worked__math">T ≈ 5568 s ≈ 92.8 min</div>
      <div class="worked__caveat">Caveat: this assumes a circular orbit. It does not include J2 perturbations.</div>
    </div>
  </div>
</div>
```

```css
.worked { border: 1px solid var(--border-hairline); border-radius: var(--radius-base);
  background: var(--surface-card); overflow: hidden; }
.worked__row { display: grid; grid-template-columns: 120px 1fr; gap: 16px;
  padding: 16px 20px; border-bottom: 1px solid var(--border-hairline);
  align-items: baseline; }
.worked__row:last-child { border-bottom: none; }
.worked__row--premise    { background: var(--toby-info-soft);   border-bottom-color: var(--toby-info-tint); }
.worked__row--derivation { background: var(--toby-watch-soft);  border-bottom-color: var(--toby-watch-tint); }
.worked__row--result     { background: var(--toby-stable-soft); border-bottom-color: var(--toby-stable-tint); }
.worked__row--premise    .worked__step { color: var(--toby-info-text); }
.worked__row--derivation .worked__step { color: var(--toby-watch-text); }
.worked__row--result     .worked__step { color: var(--toby-stable-text); }
.worked__step { font-family: var(--font-mono); font-size: 11px;
  text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600; }
.worked__body { font-size: 13px; line-height: 1.55; color: inherit; }
.worked__math { font-family: var(--font-mono); font-size: 14px;
  padding: 8px 0; color: inherit; }
.worked__caveat { font-size: 12px; opacity: 0.78; margin-top: 8px;
  padding-left: 12px; border-left: 2px solid currentColor; }
```

### Sparkline in a table — four columns, two left + two right

```html
<table class="tbl">
  <thead>
    <tr>
      <th>Signal</th>
      <th>12-sample trace</th>
      <th class="num">Last</th>
      <th class="num">Δ%</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Drift posterior</td>
      <td>
        <svg width="120" height="22" viewBox="0 0 120 22">
          <rect x="2" y="7" width="116" height="9" fill="var(--toby-paper-2)" opacity="0.7"/>
          <path d="M 2 4 L 23 8 L 44 12 L 65 12 L 86 15 L 118 19"
                fill="none" stroke="var(--toby-accent)" stroke-width="1.25"/>
          <circle cx="118" cy="19" r="2" fill="var(--toby-accent)"/>
        </svg>
      </td>
      <td class="num">0.54</td>
      <td class="num delta--down">−5.3%</td>
    </tr>
  </tbody>
</table>
```

```css
.tbl { width: 100%; border-collapse: collapse; font-size: 13px; }
.tbl th { text-align: left; font-weight: 600; color: var(--text-muted);
  padding: 12px 16px; border-bottom: 1px solid var(--border-strong);
  text-transform: uppercase; font-size: 11px; letter-spacing: 0.08em; white-space: nowrap; }
.tbl td { padding: 14px 16px; border-bottom: 1px solid var(--border-hairline); vertical-align: middle; }
.tbl tr:last-child td { border-bottom: none; }
.tbl .num, .tbl th.num { text-align: right; font-family: var(--font-mono); font-feature-settings: 'tnum'; }
.delta--up   { color: var(--toby-stable); }
.delta--down { color: var(--toby-accent); }
.delta--flat { color: var(--text-muted); }
```

### Decision row — Approve / Hold / Reject

```html
<div class="dec">
  <div class="dec__body">
    <div class="dec__title">Approve controlled release of M-01 v4.2?</div>
    <div class="dec__meta">Owner · Mission ops · Sayo  ·  Confidence · High · CI 95%  ·  Cadence · two-sample rule</div>
  </div>
  <div class="dec__actions">
    <button class="dec__btn dec__btn--approve dec__btn--on">Approve</button>
    <button class="dec__btn dec__btn--hold">Hold</button>
    <button class="dec__btn dec__btn--reject">Reject</button>
  </div>
</div>
```

```css
.dec { border: 1px solid var(--border-hairline); border-radius: var(--radius-base);
  background: var(--surface-card); padding: 20px;
  display: grid; grid-template-columns: 1fr auto; gap: 20px; align-items: start; }
.dec__title { font-size: 14px; font-weight: 600; }
.dec__meta { font-family: var(--font-mono); font-size: 11px;
  color: var(--text-muted); letter-spacing: 0.04em; line-height: 1.5; }
.dec__actions { display: flex; flex-direction: column; gap: 8px; min-width: 120px; }
.dec__btn { background: var(--surface-card); border: 1px solid var(--border-hairline);
  border-radius: 6px; padding: 8px 16px;
  font-size: 12px; font-weight: 500; cursor: pointer; }
.dec__btn--approve { color: var(--toby-stable); border-color: var(--toby-stable); }
.dec__btn--hold    { color: var(--toby-watch);  border-color: var(--toby-watch); }
.dec__btn--reject  { color: var(--toby-accent); border-color: var(--toby-accent); }
.dec__btn--on.dec__btn--approve { background: var(--toby-stable); color: var(--text-on-dark); }
.dec__btn--on.dec__btn--hold    { background: var(--toby-watch);  color: var(--text-on-dark); }
.dec__btn--on.dec__btn--reject  { background: var(--toby-accent); color: var(--text-on-dark); }
```

Use only the three listed verbs. The chosen verb's button fills with its semantic color. Each decision needs a rationale field and a named rollback owner.

### Code block — dark theme

```html
<pre class="code"><code><span class="code__ln">1</span><span class="code__kw">function</span> retryWithBackoff(<span class="code__num">3</span>) {<br/>  <span class="code__com">// Removing this fixes the bug, but the reason is unknown.</span><br/>  <span class="code__kw">return</span> <span class="code__str">"ok"</span>;<br/>}</code><button class="code__copy">copy</button></pre>
```

```css
.code { background: var(--toby-ink-2); color: var(--text-on-dark);
  font-family: var(--font-mono); font-size: 13px; line-height: 1.55;
  padding: 16px 20px; border-radius: var(--radius-base); position: relative;
  overflow-x: auto; }
.code__ln { color: var(--text-on-dark-muted); margin-right: 16px;
  user-select: none; display: inline-block; width: 20px; text-align: right; }
.code__kw  { color: var(--code-kw); }
.code__num { color: var(--code-num); }
.code__str { color: var(--code-str); }
.code__com { color: var(--code-com); font-style: italic; }
.code__copy { position: absolute; top: 12px; right: 12px; background: transparent;
  border: 1px solid var(--text-on-dark-muted); color: var(--text-on-dark-muted);
  padding: 4px 10px; border-radius: var(--radius-sm); font-size: 11px;
  font-family: var(--font-sans); cursor: pointer; }
```

### Annotation pin — numbered callout on a diagram

```html
<div class="pin" style="top: 40px; left: 120px;">
  <span class="pin__num">1</span>
  <span class="pin__line"></span>
  <span class="pin__label">Periapsis · closest approach</span>
</div>
```

```css
.pin { position: absolute; display: flex; align-items: center; gap: 8px;
  font-family: var(--font-sans); font-size: 12px; color: var(--toby-info-text); }
.pin__num { width: 22px; height: 22px; border-radius: 50%;
  background: var(--toby-info); color: var(--text-on-dark);
  display: inline-flex; align-items: center; justify-content: center;
  font-weight: 600; font-size: 11px; font-family: var(--font-mono); }
.pin__line { width: 24px; height: 1px; background: var(--toby-info); }
.pin__label { background: var(--toby-info-soft);
  border: 1px solid var(--toby-info-tint); padding: 4px 10px;
  border-radius: var(--radius-sm); }
```

---

## Quick rules summary

- Numeric columns are always right-aligned, mono, with tabular numerals.
- State-tinted components always use one color family, with a soft background, a tint border, a text foreground, and a left strip in the family's base color.
- Selected items in lists use paper-2 with a 3px info inset, because paper-3 against paper-3 is invisible.
- Focus rings are 2px info-teal outside rings at a 2px offset. They are never red.
- A press state makes the background darker but does not move the control.
