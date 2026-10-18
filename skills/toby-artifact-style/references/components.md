# Toby Artifact components

Load this file when you build any component for a Toby Artifact Style artifact: callouts, alerts, badges, status pills, stat grids, worked examples, decision rows, sparklines in tables, code blocks, dialogs, treeviews, and equation blocks.

## Signature patterns

Build each component to the pattern below, and reuse an existing component when one already covers the case:

- **Callout / Alert / Toast:** uses the `-soft`, `-tint`, and `-text` colors of its status, with a bold title above a body at opacity 0.88.
- **StatusPill:** uses one set of status colors for its background, border, and text, showing live system status with a dot and a label.
- **Badge:** a compact mono chip that displays a count or short code (`ink`, `info`, `stable`, `watch`, or `cons`).
- **StatGrid (KPI grid):** a 3- or 4-column grid with hairline dividers, where each cell's 2px top accent strip takes the next color in the chart palette.
- **Worked Example:** three rows in order (`PREMISE` in `info-soft`, `DERIVATION` in `watch-soft`, and `RESULT` in `stable-soft`).
- **Decision Row:** a row with a title, meta text, and Approve / Hold / Reject buttons in matching semantic colors.
- **Sparkline-in-table:** an 80–120px trace SVG in a table cell, with adjacent columns for `Last` and `Δ%`.
- **Code block:** a dark-theme block with an `ink-2` background, mono text, a line gutter, a copy button, and syntax classes (`kw`, `num`, `str`, `com`).
- **Treeview:** a vertical hierarchy with a hairline rule down each level's left side and a `--toby-paper-2` background plus 3px `--toby-info` left strip on the selected row.
- **Annotation pin:** a numbered circle, leader line, and framed label in `--toby-info`.
- **Equation block:** a centered mono formula with a 2px info-colored top accent.
- **Dialog alert variant:** adds a 4px red top strip and a red title for irreversible actions.

---

## Full component vocabulary

Build these components to the specs below when a page needs them.

### Layout & structure
- **Topbar:** a 56px-tall header with a breadcrumb, an optional id stamp, and right-aligned actions.
- **Sidebar:** a grouped vertical nav where the selected row uses `--toby-paper-2` with a 3px `--toby-info` left inset (never `paper-3`).
- **Panel:** a content card with an eyebrow, a title, and actions (`default` on `--toby-paper-3`, `flush` on paper, and `authority` on ink).
- **Tabs:** the active tab uses an `info-soft` tint and a 3px `--toby-info` underline.
- **Accordion** (covers Collapsible): opens one section at a time by default, or multiple sections when `multi` is set.
- **Toolbar:** an inline strip of mini-controls where `.toolbar__btn--on` uses an ink background and `--text-on-dark` text.
- **Pagination:** 32px mono cells with tabular numerals, keeping ellipses between page numbers when many pages exist.

### Form controls
- **Button:** variants are `default` (paper), `primary` (ink), `ghost` (transparent), and `consequence` (accent), with `--sm` setting a 28px height.
- **Input:** 36px tall, with an info-teal focus ring at a 2px offset.
- **Textarea:** a multi-line Input whose optional `maxLength` shows a mono character count at the bottom right.
- **Number field:** mono digits with tabular numerals, stacked `+/−` buttons on the right, and hidden native browser spinners.
- **OTP field:** `N` mono slots (default 6) with an optional `groupAt` separator, where Backspace moves to the previous slot.
- **Checkbox** + **CheckboxGroup:** supports a `row` modifier for inline layout.
- **Toggle** (covers Switch): a 36×20 track with a thumb that uses an ink track and paper thumb when on.
- **Slider:** shows a mono value with tabular numerals to the right of the label.
- **ToggleGroup:** a segmented control where `.tgrp__btn--on` uses an ink background and white text with `white-space: nowrap`.
- **Combobox** (covers **Select** and **Autocomplete**): searchable by default, or a plain Select when `searchable={false}`.
- **Calendar:** today gets a 2px `--toby-info` border and bold info text, the selected day fills with ink, and marked dates show a small `--toby-info` dot.
- **DatePicker:** a Calendar inside a popover whose trigger shows the selected ISO date in mono.

### Overlays & menus
- **Dialog** (covers **Modal** and **AlertDialog**): a centered panel over a backdrop, where `kind="alert"` adds a 4px red top hairline and red title.
- **Sheet** (covers **Drawer** and **Bottomsheet**): `side="right" | "left" | "bottom"`, with a drag grip on the bottom variant.
- **Popover:** a click-anchored panel with 16px padding.
- **Tooltip:** a dark ink panel with a caret that appears above the trigger on hover.
- **Menu:** a popover menu with group labels, shortcut hints (`⌘C`, `↵`), separators, and a `danger` variant.
- **Menubar:** a horizontal strip (`File / Edit / View`) whose `--open` state uses `paper-2` and a 2px info underline.
- **NavigationMenu:** a Menubar where each item opens a larger content panel with a 2px info top border.
- **Command palette:** a full-screen search modal with grouped items and a keyboard footer.
- **Toast:** stacks at the bottom right, dismisses after ~4s, and uses a semantic left border and soft tinted background.

### Display & feedback
- **Avatar:** shows initials only (`sm 22`, `md 28`, `lg 40`), with a dark fill on the `--ink` variant.
- **Kbd:** a mono keyboard glyph with a 2px bottom border.
- **Spinner:** a 1.5px ring with a 720ms linear spin and no glow (`md 16`, `lg 22`).
- **Skeleton:** a static placeholder (`line 12px`, `title 18px`, `block 64px`).
- **Progress:** a 4px linear bar matching the state hues, with an optional `indeterminate` kind.
- **Meter:** a progress bar with a min/max axis and an optional consequence-red threshold mark.
- **Separator:** `horizontal` (1px hairline) or `vertical` (1px column), using `--border-strong` for the `strong` modifier.
- **Empty state:** a dashed hairline border, an info-teal geometric icon, a title, a body, and an optional action.

### Data display
- **Metric:** a label, a large numeric value, a unit suffix, an optional progress strip, and an optional target line.
- **KV:** a two-column definition list with a mono eyebrow term on the left and a tabular-numeral mono value on the right.
- **EvidenceTable:** `.tbl` with `.num` for right-aligned mono columns and a `--border-strong` header divider.
- **Sparkline:** an inline trace SVG (`80–120px` wide) used in a table cell, KV value, or stat card.

---

## Paste-ready starter HTML

The colors below use the tokens defined in `SKILL.md`. Change the copy, and keep the structural classes unchanged.

### Callout / Alert / Toast

```html
<div class="alert alert--watch">
  <div>
    <div class="alert__title">Watch · retry pressure</div>
    <div class="alert__body">Retry volume is 18% above baseline. The two-sample rule hasn't tripped yet.</div>
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

The same `--*-soft / --*-tint / --*-text` triple sets the colors for status pills, badges, toasts, and worked-example rows.

### Status pill

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

### Stat grid

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
.stat:nth-child(4n+1) { --stat-accent: var(--toby-blue-steel); }
.stat:nth-child(4n+2) { --stat-accent: var(--toby-muted-violet); }
.stat:nth-child(4n+3) { --stat-accent: var(--toby-field-olive); }
.stat:nth-child(4n+4) { --stat-accent: var(--toby-ochre); }
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

### Worked Example

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
      <div class="worked__caveat">Caveat: this assumes a circular orbit and doesn't include J2 perturbations.</div>
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

### Sparkline in a table

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

### Decision row

```html
<div class="dec">
  <div class="dec__body">
    <div class="dec__title">Approve controlled release of M-01 v4.2?</div>
    <div class="dec__meta">Rollback owner · Mission ops · Sayo  ·  Confidence · High · CI 95%  ·  Cadence · two-sample rule</div>
    <div class="dec__rationale">Rationale · both meters stayed inside the watch band for two samples</div>
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
.dec__rationale { font-size: 13px; margin-top: 8px; }
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

### Code block

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

### Annotation pin

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
