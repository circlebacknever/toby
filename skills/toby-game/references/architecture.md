# Architecture — the single-file skeleton

Each game is one `.html` file with one `<style>` and one `<script>`. It has no build step and no assets, so it opens by double-click. Use Three.js for 3D, raw canvas for 2D, and plain DOM when the board is cards and panels.

## The shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>your game</title>
<style>/* Put the tokens first, then the layout. */</style>
</head>
<body>
  <!-- The canvas, three.js mount, or DOM board goes here, followed by the floating paper UI. -->
<script type="module">
  // The top comment names what is faked, and the state, sim, render, and wiring sections follow it.
</script>
</body>
</html>
```

For 3D, load a current three.js as a module, which needs no bundler and keeps the game in one file. Pin one version and one CDN, or you get the duplicate-module bug.

```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js" } }
</script>
```

Drop `user-scalable=no` for a reading-heavy DOM game where players need pinch-zoom.

## The spine

Make these decisions once.

- **One state object.** Keep all state in one lowercase `G` with a single `reset()` that re-seeds and rebuilds. Keep it in module scope, because a `window.*` side channel breaks headless tests.
- **Resolve, then replay.** A pure function computes the outcome, and the animation plays that outcome back without changing it. As a result, the picture cannot contradict the result. You can also test the same function headless.
- **Seed the randomness.** Use one seedable generator and store the seed in the result, so a run reproduces and you can replay a bug. Keep `Math.random()` out of the resolver.
- **Control the clock.** Clamp the frame delta so a backgrounded tab does not blow up the sim. Step outcomes at a fixed rate so replays match. Give the player a speed knob. Guard the loop so one thrown error does not blank the screen.
- **Integrate so it cannot blow up.** Sub-step a stiff force so one big push across a frame does not inject energy and fling a body off-screen. Match the scheme to the system (symplectic for mutually attracting bodies, small explicit steps for a swarm of test particles). Cap or soften a force near a singularity. Clamp a runaway speed. A blow-up is a free win, so any search exploits the blow-up before it finds the intended solution.
- **Name the phases.** A readable string (`deploy`, `work`, `flee`) controls the sim and the camera. The camera tracks the moving actor so the view does not jump when the phase changes.
- **Map input from the real camera.** Compute screen-to-world from the actual camera rig by offsetting along its axes and intersecting the ground. Do not compute it from an approximate frustum guess.
- **Make state changes total.** Code that should run once sets its own callback to null first. Every transition resets what it depends on. When you retire a verb, re-grep its call sites.
- **Manage the meshes.** Build each mesh once. On teardown, dispose its geometry, material, and label textures, and then null the slot.
- **Go data-oriented only where the entity count is high enough to require it.** Thousands of particles need flat typed arrays and one draw call, but a few characters do not.

## How real to make it

Match the model to the system. Use a real integrator for something physical, a rate or a curve for something statistical, and a few rules per agent for something behavioral. A different model can fit the same subject, depending on what the game is for.

A market as a backdrop number is statistical. A market whose point is the crash is behavioral, because the crash has to emerge from the agents. Pick the model that still produces the surprise. Then say what you faked in a comment, the way the games do ("physics is vibes-based and labeled as such").

## Sound, and saving

The game has no asset folder, so synthesize audio with a little WebAudio. Use a tone for a blip and a noise burst for a hit. A silent game is also acceptable when the silence is a deliberate choice.

Scale saving to the session. A toy needs only state and a reseed, a bounded run is worth a diagnostic ending, and a campaign is worth a save. Version the saved blob and migrate or discard it on load inside a try/catch, or a later edit breaks old saves.
