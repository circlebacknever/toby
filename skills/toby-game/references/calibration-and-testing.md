# Calibration and testing

Measure balance, and check correctness with a script.

Pull the logic out and run it headless. Resolve and replay are separate, so the outcome function needs no renderer and can run ten thousand times in a loop. Put a clear marker around the pure logic (state, sim, resolver, rng), so a one-line command can copy it into a node test. `scripts/check-single-html.mjs <file>` runs the rote pass. It extracts the largest inline script and syntax-checks it, so a stray paren cannot ship as a blank canvas. It also cross-references every `getElementById`/`$()` against the real element ids, so a stale handler shows up before a player finds the dead button. Assert that the replay never contradicts the result and that the odds stay inside their floor and ceiling. Also assert that a conserved quantity stays conserved and every position and score stays finite over a long run.

A `Number.isFinite` guard catches a physics blow-up the eye misses. Assert exact deltas. A test that checks "the balance dropped, so the fine works" fails falsely when income in the same step outweighed the fine. In headless runs, guard browser-only globals with `typeof`. Give every wait-for-click overlay its own phase that clears its buttons. When a scripted run fails, isolate a minimal repro. Half of the reported failures come from the test stubs.

Use three bots to set the band. A random-input bot finishes near zero, a human-grade bot scores in the target range (often 10–20%), and a superhuman bot scores above it. If random and human-grade score the same, the band is flat, so the game has no skill in it. The tuning pass cannot fix a flat band, because the problem is structural.

The human-grade bot has to model human slack, such as release windows and reaction frames, or it reports a number no human will get. Pool batches before concluding, because a compounding ladder swings 6% to 12% on identical code at n=150. Print the per-round distribution against the curve you meant, since a ladder total hides one round that ends half the runs. A toy has no win to measure, so its band is the parameter range where the sim keeps moving and the surprise reliably shows.

Test the comedy too. Check that every counter the ending reads is one the run tracked, every thread advances, and the feed never goes silent.

Patch a live game with unique-anchor replacements on a working copy. Each anchor must match exactly once. A count of 0 means the code moved, and a count of 2 means the anchor is ambiguous, so re-read the file in either case. Use anchor text with no escapes, and run the syntax check after the patch. Confirm the patch printed success before trusting a measurement. Never rewrite the whole file.

Done means the bot bands hold, the invariants hold, the game plays live in both orientations, and reduced motion is honored.
