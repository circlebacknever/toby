# Calibration and testing

Verify game syntax, invariants, and difficulty balance with automated scripts before calling a build finished.

## Mechanical and invariant checks

1. Wrap the pure simulation logic (`G`, `reset`, `step`, seeded RNG) between clear markers so a Node test script can import and run it ten thousand times without a browser.
2. Run `node <this skill's folder>/scripts/check-single-html.mjs <file>` after each edit to syntax-check the inline script and confirm every `getElementById`/`$()` call matches an HTML id.
3. Assert invariants across long runs: every position, velocity, and score satisfies `Number.isFinite`, conserved quantities stay bounded, and single-step balance deltas match the formula. Remove overlay buttons as soon as their game phase ends.

## Bot calibration bands

Run three automated test bots across multiple batches of at least 150 runs each, printing per-round and total win rates:

- **Random bot:** finishes near 0% win rate.
- **Human-grade bot** (with realistic reaction delay and release jitter): finishes inside the target band (typically 10–20%).
- **Superhuman bot:** finishes well above the human band.

When the random and human-grade bots score nearly the same, the game lacks a skill curve, so fix the gameplay structure (`references/gameplay.md`) before tuning numbers. For a pure sandbox toy, verify the parameter range where the simulation stays active and shows its surprising behavior. Also confirm that play increments every ending stat counter and can reach the final step of every storyline.
