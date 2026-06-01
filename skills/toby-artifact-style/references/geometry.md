# Toby Artifact geometry

Load this file when putting a geometric mark on a slide, panel, or page — either at content scale (the mark IS the figure) or at decorative scale (the mark is textural backdrop).

## Two scales, nothing in between

- **Content scale (120–220 px).** The mark is doing work. Pair it with a small UPPERCASE label naming it. The label is mandatory — unlabeled geometry is decoration and out.
- **Decorative scale (40–80 px).** The mark is textural. Opacity ≤ 0.25. No label.

If you find yourself sizing a mark between these two ranges, pick one of the two extremes.

## Geometry never carries a panel alone

Each mark clarifies a claim that lives next to it. A slide with only a geometric mark and no accompanying claim has no purpose. The mark is annotation; the claim is content.

## Stroke and color

- 1px stroke, monochromatic, `currentColor` or `--text-primary`.
- No fills except where a marker is intentionally a solid dot (anchor, body at focus, periapsis marker).
- A single red dot (`--toby-accent`) is allowed when the dot marks the consequence anchor — periapsis, threshold breach, decision point. Otherwise, ink only.

---

## The 20 named marks

Each mark has one purpose. Apply at content scale (with the named label) or at decorative scale (quiet backdrop).

| Mark | Purpose |
|---|---|
| `orbit-marker` | Single anchored ellipse with a body at one focus. Identifies the subject of an orbit claim. |
| `evidence-field` | Scatter of dots within a bounded region. Marks where samples were taken. |
| `threshold-rail` | Horizontal band defined by a min and a max. Shows watch / consequence boundaries beside a value. |
| `coordinate-stamp` | Tagged anchor at a precise (x, y). Label sits in a small framed chip beside the crosshair. |
| `locator-reticle` | Crosshair with bracket marks around a target. Draws the eye hard — use sparingly. |
| `signal-rings` | Concentric arcs decaying outward. Implies attenuation, decay, broadcast. |
| `uncertainty-fan` | Cone widening with distance. Trajectory uncertainty after a perturbation. |
| `uncertainty-halo` | Ring of decreasing density around a point. Position uncertainty without committing to a direction. |
| `axis-bracket` | Span markers tagged with a value band. Bracket below an axis names the interval as a thing. |
| `route-trace` | Dashed path between two anchored points. Marks the trajectory, not its endpoints. |
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

Pick the mark for the structure of the subject, not its name. Some defaults:

- A network or graph subject → `matrix-grid` or `triangulation-mesh` as backdrop; `coordinate-stamp` for nodes.
- A measurement-over-time subject → `timeline-ticks` as axis, `model-envelope` for the fit, `threshold-rail` for the alert band.
- A trajectory or path subject → `route-trace` for the path, `uncertainty-fan` for forecast, `coordinate-stamp` for waypoints.
- An orbital subject → `orbit-marker` content-scale, `orbital-lattice` as decorative backdrop.
- A signal or transmission subject → `signal-rings` for emitter, `coordinate-fan` for sector coverage.

Lazy defaults to refuse: `orbit-marker` for every artifact regardless of subject, `locator-reticle` as a decoration when no target needs locating, `calibration-grid` everywhere because it looks technical.

If you cannot name why the mark fits the subject's structure, pick a different mark.

---

## Label format

Content-scale marks get a small UPPERCASE label in mono, +0.12em letter-spacing, `--text-muted`, sized 11px. Place the label beneath or beside the mark, never inside it.

Example: `ORBIT MARKER`, `UNCERTAINTY FAN`, `COORDINATE STAMP · 34.05° N, 118.24° W`.

---

## Decorative-scale rules

- Maximum 80px in any dimension.
- Opacity ≤ 0.25.
- Use `--text-on-dark-muted` on ink surfaces, `--text-muted` on paper.
- No label.
- One decorative mark per panel maximum. Two competing marks read as noise.
