# Toby Artifact geometry

Load this file when placing a geometric mark on a slide, panel, or page. Marks appear at one of two scales: content scale (`120–220 px`, studied as a diagram figure) or decorative scale (`40–80 px`, faint background texture). Never size a mark between `80 px` and `120 px`.

## Two scales and placement

- **Content scale (`120–220 px`):** place the mark beside the claim it clarifies, and pair it with an 11px UPPERCASE mono label (`+0.12em` letter-spacing, `--text-muted`) beneath or beside the mark. Never place a content-scale mark without a label or on a slide that makes no claim.
- **Decorative scale (`40–80 px`):** set opacity to `<= 0.16` without a label, using `--text-on-dark-muted` on ink and `--text-muted` on paper. Place at most one decorative mark on a title, cover, section-divider, or closing slide.

## Stroke and color

- Draw marks as 1px monochromatic outlines in `currentColor` or `--text-primary` with no fill, except a solid dot for an anchor point or orbital focus.
- Use a single `--toby-accent` red dot only to mark where a consequence, threshold breach, or periapsis occurs, and otherwise draw the mark in ink only.

---

## The 20 named marks

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

## Pairing marks with subjects

Pick the mark that matches the structure of the subject:

- **Network or graph:** `matrix-grid` or `triangulation-mesh` backdrop with `coordinate-stamp` nodes.
- **Time series:** `timeline-ticks` axis, `model-envelope` fit, and `threshold-rail` alert band.
- **Trajectory or path:** `route-trace` path, `uncertainty-fan` forecast, and `coordinate-stamp` waypoints.
- **Orbital mechanics:** `orbit-marker` at content scale and `orbital-lattice` at decorative scale.
- **Signal or broadcast:** `signal-rings` emitter and `coordinate-fan` sector coverage.

Never default to `orbit-marker`, `locator-reticle`, or `calibration-grid` when the subject has a different structure.
