## 1
Found it. The test asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC, so the assertion drifts about once in nine runs. Not fixed yet. The fix is either freezing the clock in the test or asserting on a timezone-aware value, and I want to check which one the other timestamp tests already assume before picking.

## 2
The sync job isn't idempotent, so a retry wrapper turns a twice-a-week failure into a twice-a-week duplicate-row problem. A partial run already writes rows before it fails. Retry it and those same rows get written again. Fix the write path first, either with an upsert on a natural key or a run-id checkpoint. Once it's idempotent, the retry wrapper is safe to add.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none before.

The limit is now per-account rather than per-route-per-account. That's the one behavior change here, so a user hitting the ceiling on one route now blocks their other routes too.

## 4
I don't know. The diff from Tuesday's deploy has nothing in it that allocates, and I don't have profiler data to say where the extra 40 percent is going. A heap snapshot from before and after the deploy would settle it.
