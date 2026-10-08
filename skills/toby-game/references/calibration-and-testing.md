# Calibration and testing

Measure balance, and check correctness with a script.

Pull the logic out and run it headless. Resolve and replay are separate, so the outcome function needs no renderer and can run ten thousand times in a loop. Put a clear marker around the pure logic (state, sim, resolver, rng), so a one-line command can copy it into a node test.

`scripts/check-single-html.mjs <file>` runs the mechanical checks. It extracts the largest inline script and syntax-checks it. A missing parenthesis is then caught before release, when the player would see only a blank canvas. It also cross-references every `getElementById`/`$()` against the real element ids, so a stale handler shows up before a player finds the dead button.

Assert that the replay never contradicts the result and that the odds stay inside their floor and ceiling. Also assert that a conserved quantity stays conserved and every position and score stays finite over a long run.

A `Number.isFinite` guard catches a physics blow-up the eye misses. Assert exact deltas. A test can check "the balance dropped, so the fine works". That test fails even when the fine works, if income in the same step was larger. In headless runs, guard browser-only globals with `typeof`. Give every overlay that waits for a click its own named game phase, and remove that overlay's buttons when the phase ends. When a scripted run fails, isolate a minimal repro. Check the test stubs before the game code, because stubs caused about half of the past failures.

Use three bots to set the band, which is the target range of scores. A random-input bot finishes near zero, a human-grade bot scores in the target range (often 10–20%), and a superhuman bot scores above it. If random and human-grade score the same, the band is flat, so the game has no skill in it. The tuning pass cannot fix a flat band, because the problem is structural.

The human-grade bot has to imitate human limits, such as imprecise release timing and reaction delays, or it reports a number no human will get. Combine several batches of runs before you draw a conclusion. In a game of several rounds in a row, the win rate moved between 6% and 12% across batches of 150 runs on identical code. Print the win rate for each round next to the rate you intended, because the total can hide one round that ends half the runs. A toy has no win to measure, so its band is the parameter range where the sim keeps moving and the surprise reliably shows.

Test the comedy too. Check that every counter the ending reads is one the run tracked, every storyline advances, and the news feed never goes silent.

Patch a working copy with exact-text replacements that each match once, and re-read the file when a replacement matches zero places or several. Run the syntax check after each patch, and never rewrite the whole file.

Done means each bot scores inside its band, the invariants hold, the game plays live in both orientations, and reduced motion is honored.
