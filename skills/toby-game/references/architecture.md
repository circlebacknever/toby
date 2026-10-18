# Architecture

Build each game as one `.html` file with one `<style>` and one `<script>` so it opens in a browser without a bundler or external assets. Order the script as state, simulation, rendering, and input wiring. Set the viewport to `width=device-width, initial-scale=1, user-scalable=no` (omitting `user-scalable=no` on text-heavy DOM games).

## 3D import map

For 3D games, pin a single Three.js ES module URL in an `importmap` so the page never loads two copies:

```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js" } }
</script>
```

## Core rules

- **Single state object:** keep all mutable game state in one module-scoped `G` object with a `reset()` function. Keep state off `window.*` so Node tests can import the logic headlessly.
- **Deterministic tick and seeded RNG:** advance physics and outcomes in a pure tick function driven by a seeded PRNG (never `Math.random()`) and a clamped frame delta (`dt`).
- **Stable integration:** sub-step fast forces, soften singularities, and clamp velocities so values stay finite and players or bots can't exploit physics blow-ups.
- **Named phases and clean transitions:** drive camera and UI state from a phase string (`deploy`, `work`, `flee`), compute pointer rays from the active camera rig, and dispose Three.js geometries, materials, and textures on teardown.
- **Flat typed arrays only at scale:** use typed arrays and instanced draw calls when simulating thousands of particles, and plain objects for a handful of characters.

## Model fidelity, audio, and saves

Match the simulation model to the premise (kinematics for physics, rates for macro stats, per-agent rules for emergent crashes) and state what the model simplifies in a top-of-script comment. Synthesize sound effects with WebAudio (or keep the game silent), and version any `localStorage` save payload inside a `try/catch`.
