# Toby Artifact geometry

Load this file when you put a geometric mark on a slide, panel, or page. The mark can appear at content scale, where the mark IS the figure, or at decorative scale, where it forms a textured backdrop.

## Two scales

- **Content scale (120–220 px).** The mark shows part of the content, so pair it with a small UPPERCASE label that names it. The label is mandatory, because unlabeled geometry counts as decoration, which is not allowed at this scale.
- **Decorative scale (40–80 px).** The mark adds texture, so set its opacity to ≤ 0.25 and give it no label.

If you find yourself sizing a mark between these two ranges, pick one of the two extremes.

## Geometry beside a claim

Place each mark next to the claim it clarifies. A slide with a geometric mark and no claim has no purpose, because the mark only annotates the claim.

## Stroke and color

- Draw marks with a 1px monochromatic stroke in `currentColor` or `--text-primary`.
- Use no fills unless the marker is a solid dot, such as an anchor, a body at a focus, or a periapsis marker.
- A single red dot (`--toby-accent`) is allowed when the dot marks the consequence anchor, such as periapsis, a threshold breach, or a decision point. Otherwise, draw the mark in ink only.

---

## The 20 named marks

Each mark has one purpose. Use a mark at content scale with its named label, or at decorative scale as a faint backdrop.

| Mark | Purpose |
|---|---|
| `orbit-marker` | Single anchored ellipse with a body at one focus. Identifies the subject of an orbit claim. |
| `evidence-field` | Scatter of dots within a bounded region. Marks where samples were taken. |
| `threshold-rail` | Horizontal band defined by a min and a max. Shows watch / consequence boundaries beside a value. |
| `coordinate-stamp` | Tagged anchor at a precise (x, y). The label is in a small framed chip beside the crosshair. |
| `locator-reticle` | Crosshair with bracket marks around a target. Draws the eye hard, so use sparingly. |
| `signal-rings` | Concentric arcs decaying outward. Implies attenuation, decay, broadcast. |
| `uncertainty-fan` | Cone widening with distance. Trajectory uncertainty after a perturbation. |
| `uncertainty-halo` | Ring of decreasing density around a point. Position uncertainty without committing to a direction. |
| `axis-bracket` | Span markers tagged with a value band. Bracket below an axis names the interval as a thing. |
| `route-trace` | Dashed path between two anchored points. Marks the trajectory between the two anchored points. |
| `radial-range` | Two concentric circles defining inner and outer radius. Pair with a label for the band. |
| `phase-bands` | Horizontal stripes of equal width. Seasonal, diurnal, or threshold-banded phases. |
| `timeline-ticks` | Linear tick marks with `T+00`, `T+18`, `T+42` labels. Default temporal axis decoration. |
| `scale-bar` | Tagged span from 0 to a labelled magnitude. Use whenever a diagram is to-scale. |
| `coordinate-fan` | Angular sectors radiating from a point. Angular ranges or sector coverage. |
| `model-envelope` | Smooth band around a trace. The 1σ / 2σ envelope of a fit. |
| `calibration-grid` | Subtle background grid for diagram alignment. Behind dense plots only. |
| `matrix-grid` | Square ruled grid. Backdrop where rows / columns mean something. |
| `orbital-lattice` | Concentric circles + radial spokes. Behind orbital diagrams to indicate the gravitational frame. |
| `triangulation-mesh` | Triangle lattice. Behind ground-station coverage diagrams. |

---

## Pairing marks with subject structure

Pick the mark for the structure of the subject. These defaults cover common subjects.

- For a network or graph subject, use `matrix-grid` or `triangulation-mesh` as the backdrop and `coordinate-stamp` for nodes.
- For a measurement-over-time subject, use `timeline-ticks` as the axis, `model-envelope` for the fit, and `threshold-rail` for the alert band.
- For a trajectory or path subject, use `route-trace` for the path, `uncertainty-fan` for the forecast, and `coordinate-stamp` for waypoints.
- For an orbital subject, use `orbit-marker` at content scale and `orbital-lattice` as a decorative backdrop.
- For a signal or transmission subject, use `signal-rings` for the emitter and `coordinate-fan` for sector coverage.

Refuse these lazy defaults: `orbit-marker` for every artifact regardless of subject, `locator-reticle` as a decoration when no target needs locating, `calibration-grid` everywhere because it looks technical.

If you cannot name why the mark fits the subject's structure, pick a different mark.

---

## Label format

Give each content-scale mark a small UPPERCASE mono label at 11px, with +0.12em letter-spacing, in `--text-muted`. Place the label beneath or beside the mark, never inside it.

Examples include `ORBIT MARKER`, `UNCERTAINTY FAN`, and `COORDINATE STAMP · 34.05° N, 118.24° W`.

---

## Decorative-scale rules

- Keep the mark at 80px or less in any dimension.
- Set the opacity to ≤ 0.25.
- Use `--text-on-dark-muted` on ink surfaces and `--text-muted` on paper.
- Give the mark no label.
- Put at most one decorative mark on a panel, because two marks in one panel look like clutter.
