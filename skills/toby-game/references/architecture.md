# Architecture — the single-file skeleton

One game is one `.html` file: one `<style>`, one `<script>`, opens by double-click, no build step, no assets. Three.js for 3D, raw canvas for 2D, plain DOM when the board is cards and panels.

## The shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>your game</title>
<style>/* tokens first, then layout */</style>
</head>
<body>
  <!-- canvas, three.js mount, or DOM board, then floating paper UI -->
<script type="module">
  // top comment names what's faked, then state, sim, render, wiring
</script>
</body>
</html>
```

For 3D, pull a current three.js as a module — no bundler, one file still. Pin one version and one CDN, or the duplicate-module bug finds you.

```html
<script type="importmap">
{ "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.184.0/build/three.module.js" } }
</script>
```

Drop `user-scalable=no` for a reading-heavy DOM game that wants pinch-zoom.

## The spine

Make these calls once.

- **One state object.** Everything in one lowercase `G` with a single `reset()` that re-seeds and rebuilds. Keep it in module scope, because a `window.*` side channel breaks headless tests.
- **Resolve, then replay.** A pure function decides the outcome. The animation plays it back and changes nothing. The picture cannot contradict the result, and the same function tests headless.
- **Seed the randomness.** One seedable generator, the seed stored in the result, so a run reproduces and you can replay a bug. Keep `Math.random()` out of the resolver.
- **Own the clock.** Clamp the frame delta so a backgrounded tab does not detonate the sim, step outcomes at a fixed rate so replays match, and give the player a speed knob. Guard the loop so one thrown error does not blank the screen.
- **Integrate so it cannot blow up.** Sub-step a stiff force so one big push across a frame does not inject energy and fling a body off-screen. Match the scheme to the system (symplectic for mutually attracting bodies, small explicit steps for a swarm of test particles). Cap or soften a force near a singularity. Clamp a runaway speed. A blow-up is a free win, and any search will take it before it ever learns the real thing.
- **Name the phases.** A readable string (`deploy`, `work`, `flee`) drives sim and camera. The camera tracks the moving actor so focus does not teleport on a phase flip.
- **Map input from the real camera.** Screen-to-world comes from the actual camera rig — offsets along its axes, intersect the ground — never an approximate frustum guess.
- **Make state changes total.** Anything that should happen once nulls its own callback first. Every transition resets what it depends on. Retire a verb and re-grep its call sites.
- **Own the meshes.** Build each once. Dispose geometry, material, and label textures on teardown. Null the slot.
- **Go data-oriented only where it earns it.** Thousands of particles want flat typed arrays and one draw call. A few characters do not.

## How real to make it

Match the model to the system: a real integrator for something physical, a rate or a curve for something statistical, a few rules per agent for something behavioral. The same subject moves between models by intent. A market as a backdrop number is statistical. A market whose point is the crash is behavioral, because the crash has to emerge from the agents. Pick the model that keeps the surprise alive, then say what you faked in a comment, the way the games do ("physics is vibes-based and labeled as such").

## Sound, and saving

No asset folder, so synthesize audio with a little WebAudio — a tone for a blip, a noise burst for a hit. Silence is a fine choice made on purpose.

Scale to the session: a toy needs only state and a reseed, a bounded run earns a diagnostic ending, a campaign earns a save. Version the saved blob and migrate or discard it on load inside a try/catch, or a later edit breaks old saves.
