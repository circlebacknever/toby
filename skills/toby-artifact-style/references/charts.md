# Toby Artifact charts

Load this file when you build a chart, plot, or data visualization for a Toby Artifact Style artifact.

## Tooling

- Production charts in artifacts: Observable Plot, Vega-Lite, or D3.
- Quick inline charts: Recharts, Chart.js, or hand-rolled SVG.
- Apply the axis, label, and caveat rules from this file with any library.

## What every plot requires

- **Title as a claim.** "p95 latency exceeds 200 ms after 14:00 UTC" passes. "Latency over time" fails.
- **X-axis label with unit.** `time (UTC)`, `requests (n)`, `weight (kg)`.
- **Y-axis label with unit.** `latency (ms)`, `pressure (kPa)`, `accuracy (proportion)`.
- **Numeric ticks or direct annotations.** Use tabular numerals (`tnum`).
- **Legend** when the chart has ≥ 2 encodings. Skip the legend for a single series.
- **Source / model note.** Place it below the chart at meta size (12 px) in `--text-muted`. "Source: prod traces, 2026-04-12 to 2026-05-10."
- **Caveat next to the figure**, never in a footnote. "Sampled at 1 Hz. Spikes < 1 s may be lost."

## Chart palette — positional order

Assign colors by series index.

| Series index | Token | Hex |
|---|---|---|
| 1 | `--toby-blue-steel` | `#2f6e8a` |
| 2 | `--toby-field-olive` | `#7d7e3a` |
| 3 | `--toby-muted-violet` | `#7a4e85` |
| 4 | `--toby-ochre` | `#8a5a1c` |
| 5 | `--toby-sage-steel` | `#607a5f` |
| 6 | `--toby-slate-blue` | `#344b6e` |

Red (`--toby-accent`, `#c44e3f`) is reserved for material consequence, such as a threshold breach, a failure, or a decision point. Never use red as a default series color.

## Allowed plot forms

Use only the plot forms below.

- line
- bar (vertical or horizontal)
- scatter
- heatmap
- timeline
- uncertainty cone or band
- small multiples (faceting)
- sparkline
- slopegraph
- distribution (histogram, kernel density, box, violin)

## Forbidden

- Pie charts (use bar).
- Donut charts (use bar).
- 3D effects of any kind.
- Gradient fills under lines.
- Shadow drops on bars or markers.
- Decorative chrome (chart frames, ornamental backgrounds).
- Rainbow or viridis-as-categorical (use positional palette).

## Direct labeling

Prefer direct labels at series endpoints (Tufte style).

- Place the series name at the right end of the line, in the line's own color.
- Skip the legend when direct labels exist.
- For bars, place values at the bar tips when space allows.

## Grids and axes

- Draw a hairline grid only when it helps the reader, using a 1px dashed line at ≤ 55% opacity in `--border-hairline` (`#c8c3b2`).
- Skip the grid entirely on small charts (sparklines, tile-sized small multiples).
- Draw axis lines as 1px solid `--border-strong` (`#7d7967`).
- Draw tick marks 4px long in the same color as the axis.
- Set axis labels at 12px in `--text-secondary` (`#3a3d42`), and set axis titles at 13px in `--text-primary` (`#1a1c1f`).

## Annotation

- Draw a threshold line as 1px dashed `--toby-accent` when crossing it means consequence. Otherwise, draw it as 1px dashed `--text-muted`.
- Fill confidence bands at 18% opacity in the series color.
- Set an annotation label in mono if it references a value (`p95 = 312 ms`), and in sans otherwise.
- For diagrams needing numbered callouts, use the **Annotation pin** pattern from `references/components.md`.

## Uncertainty

Always show uncertainty when it exists. Don't report a point estimate without an interval if the interval is known.

- Pair point estimates with intervals: `0.73 ± 0.08` or `[0.65, 0.81]`.
- Use uncertainty cones for forecasts, error bars for measured points, confidence bands for fitted curves.

## Sparklines

A sparkline is an inline trace SVG, 80–120px wide, sized to fit a table cell or KV value. See the `Sparkline in a table` snippet in `references/components.md` for the paste-ready pattern.
