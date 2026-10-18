# Visual identity

Every game uses the Toby palette and typography while adapting its rendering technique to 3D, 2D canvas, or DOM cards.

## Palette and typography

Use paper `#fdfaf1`, ink `#1a1c1f`, consequence red `#c44e3f` (reserved for a denial, a hazard, or the one irreversible button), and dark canvas `#0e0f12`. Draw other accents from teal `#2e6a78`, green `#4d7a30`, amber `#b07020`, and rust `#7a2d22` under `--toby-*` CSS variables. Set numbers in tabular monospace and prose in humanist sans, keep subtle idle motion running (honoring `prefers-reduced-motion`), and omit decorative toolbars and external image assets.

## Render modes

- **3D (Three.js):** build characters and props from scaled low-poly spheres (or boxes and lines for austere premises) with flat matte shading, one directional light, and phase-offset idle bobbing.
- **2D canvas:** use the dark `#0e0f12` field, additive blending where highlights overlap, and a low-alpha frame wash for motion trails.
- **DOM cards:** build scrolling upgrade or card lists once and update row values in place ordered by base cost so rows don't jump under the player's thumb. Toggle visibility with explicit `display: 'block'` or `'flex'`.
- **Dread register:** stop idle motion and warm lights, hold a fixed camera, and place unlabeled red markers where a threat is already present.
