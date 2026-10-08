# Toby Artifact geometry

Load this file when you put a geometric mark on a slide, panel, or page. A mark is used at one of two scales. At content scale, the mark is the figure the reader studies. At decorative scale, the mark is faint background texture.

## Two scales

- **Content scale (120–220 px).** The mark shows part of the content, so pair it with a small UPPERCASE label that names it. The label is mandatory, because unlabeled geometry counts as decoration, which is not allowed at this scale.
- **Decorative scale (40–80 px).** The mark adds texture, so set its opacity to ≤ 0.25 and give it no label.

Do not size a mark between 80 px and 120 px. Pick a size inside one of the two ranges.

## Geometry beside a claim

Place each mark next to the claim it clarifies. Do not put a mark on a slide that has no claim, because a mark only explains the claim beside it.

## Stroke and color

- Draw marks with a 1px monochromatic stroke in `currentColor` or `--text-primary`.
- Draw marks as outlines with no fill. The only exception is a solid dot for one point, such as an anchor, a body at an orbit's focus, or periapsis.
- A single red dot (`--toby-accent`) is allowed when the dot marks where the consequence happens, such as periapsis, a threshold breach, or a decision point. Otherwise, draw the mark in ink only.

---

## The 20 named marks

Each mark has one purpose. Use a mark at content scale with its label, or at decorative scale as a faint backdrop.

| Mark | Purpose |
|---|---|
| `orbit-marker` | Single anchored ellipse with a body at one focus. Shows which body a claim about an orbit refers to. |
| `evidence-field` | Scatter of dots within a bounded region. Marks where samples were taken. |
| `threshold-rail` | Horizontal band defined by a min and a max. Shows watch / consequence boundaries beside a value. |
| `coordinate-stamp` | Tagged anchor at a precise (x, y). The label is in a small framed chip beside the crosshair. |
| `locator-reticle` | Crosshair with bracket marks around a target. Readers look at it first, so use it sparingly. |
| `signal-rings` | Concentric arcs decaying outward. Use it to show attenuation, decay, or broadcast. |
| `uncertainty-fan` | Cone widening with distance. Shows trajectory uncertainty after a perturbation. |
| `uncertainty-halo` | Ring of decreasing density around a point. Shows position uncertainty without choosing a direction. |
| `axis-bracket` | Span markers tagged with a value band. A bracket below an axis marks one range of values on that axis. |
| `route-trace` | Dashed path between two anchored points. Marks the trajectory. |
| `radial-range` | Two concentric circles defining inner and outer radius. Pair with a label for the band. |
| `phase-bands` | Horizontal stripes of equal width. Shows seasonal, diurnal, or threshold-banded phases. |
| `timeline-ticks` | Linear tick marks with `T+00`, `T+18`, `T+42` labels. Use it as the default decoration for a time axis. |
| `scale-bar` | Tagged span from 0 to a labelled magnitude. Use whenever a diagram is to-scale. |
| `coordinate-fan` | Angular sectors radiating from a point. Shows angular ranges or sector coverage. |
| `model-envelope` | Smooth band around a trace. Shows the 1σ / 2σ envelope of a fit. |
| `calibration-grid` | Subtle background grid for diagram alignment. Use it only behind dense plots. |
| `matrix-grid` | Square ruled grid. Use it as a backdrop where rows / columns mean something. |
| `orbital-lattice` | Concentric circles + radial spokes. Place it behind an orbit diagram as a reference frame centered on the main body. |
| `triangulation-mesh` | Triangle lattice. Place it behind ground-station coverage diagrams. |

---

## Pairing marks with subject structure

Pick the mark for the structure of the subject. These defaults cover common subjects.

- For a network or graph subject, use `matrix-grid` or `triangulation-mesh` as the backdrop and `coordinate-stamp` for nodes.
- For a measurement-over-time subject, use `timeline-ticks` as the axis, `model-envelope` for the fit, and `threshold-rail` for the alert band.
- For a trajectory or path subject, use `route-trace` for the path, `uncertainty-fan` for the forecast, and `coordinate-stamp` for waypoints.
- For an orbital subject, use `orbit-marker` at content scale and `orbital-lattice` as a decorative backdrop.
- For a signal or transmission subject, use `signal-rings` for the emitter and `coordinate-fan` for sector coverage.

Do not use `orbit-marker` for every artifact whatever the subject, `locator-reticle` as decoration when no target needs locating, or `calibration-grid` everywhere because it looks technical.

If you cannot explain why the mark fits the subject's structure, pick a different mark.

---

## Label format

Give each content-scale mark a small UPPERCASE mono label at 11px, with +0.12em letter-spacing, in `--text-muted`. Place the label beneath or beside the mark. Do not put the label inside the mark.

Examples include `ORBIT MARKER`, `UNCERTAINTY FAN`, and `COORDINATE STAMP · 34.05° N, 118.24° W`.

---

## Decorative-scale rules

- Use `--text-on-dark-muted` on ink surfaces and `--text-muted` on paper.
- Put at most one decorative mark on a panel, because two marks in one panel look like clutter.
