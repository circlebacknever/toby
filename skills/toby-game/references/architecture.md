# Architecture — the single-file skeleton

Each game is one `.html` file with one `<style>` and one `<script>`. It has no build step and no assets, so it opens by double-click. Use Three.js for 3D, raw canvas for 2D, and plain DOM when the board is cards and panels.

Set the viewport meta to `width=device-width, initial-scale=1, user-scalable=no`, and order the script as state, sim, render, and wiring.

## The shell

For 3D, load a current three.js as a module, which needs no bundler and keeps the game in one file. Pin one version from one CDN. Otherwise the page can load three.js twice from two URLs, and the two copies do not work together.

```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js" } }
</script>
```

Drop `user-scalable=no` for a reading-heavy DOM game where players need pinch-zoom.

## Core decisions

Make these decisions once.

- **One state object.** Keep all state in one lowercase `G` with a single `reset()` that re-seeds and rebuilds. Keep `G` in module scope, because state stored on `window.*` breaks tests that run the game without a browser.
- **Resolve, then replay.** A pure function computes the outcome, and then the animation plays that outcome back without changing it. As a result, the picture cannot contradict the result. You can also test the same function headless.
- **Seed the randomness.** Use one seedable generator and store the seed in the result, so a run reproduces and you can replay a bug. Keep `Math.random()` out of the resolver.
- **Control the clock.** Cap the time between frames. Then a tab that returns from the background does not push simulation values to huge or infinite numbers. Step outcomes at a fixed rate so replays match. Give the player a speed knob. Guard the loop so one thrown error does not blank the screen.
- **Keep the physics stable.** Split each frame into several smaller physics steps when a strong force changes quickly. Then one large step cannot add energy and throw an object off-screen. Match the scheme to the system (symplectic for mutually attracting bodies, small explicit steps for a swarm of test particles). Cap or soften a force near a singularity. Clamp a runaway speed. When the physics produces runaway values, a player or a test bot can win for free. Either one finds that exploit before the intended solution.
- **Name the phases.** A readable string (`deploy`, `work`, `flee`) controls the sim and the camera. The camera tracks the moving actor so the view does not jump when the phase changes.
- **Map input from the real camera.** Compute screen-to-world from the actual camera rig by offsetting along its axes and intersecting the ground. Do not compute it from an approximate frustum guess.
- **Make every state change complete.** Code that should run once sets its own callback to null first. Every transition resets what it depends on. When you remove a player action, search the file again for every place that calls it.
- **Manage the meshes.** Build each mesh once. On teardown, dispose its geometry, material, and label textures, and then null the slot.
- **Go data-oriented only where the entity count is high enough to require it.** Thousands of particles need flat typed arrays and one draw call, but a few characters do not.

## How real to make it

Match the model to the system. Use a real integrator for something physical, a rate or a curve for something statistical, and a few rules per agent for something behavioral. A different model can fit the same subject, depending on what the game is for.

A market as a backdrop number is statistical. A market whose point is the crash is behavioral, because the crash has to emerge from the agents. Pick the model that still produces the one surprising behavior the creator asked for. Then state what you faked in a comment at the top of the script, such as "physics is vibes-based and labeled as such".

## Sound, and saving

The game has no asset folder, so synthesize audio with a little WebAudio. Use a tone for a blip and a noise burst for a hit. A silent game is also acceptable when the silence is a deliberate choice.

Match saving to the length of play. A toy needs only its current state and a way to reseed it. A run with a fixed end is worth an end screen that reports how the player played. A campaign over several sessions is worth a save. Version the saved blob and migrate or discard it on load inside a try/catch, or a later edit breaks old saves.
