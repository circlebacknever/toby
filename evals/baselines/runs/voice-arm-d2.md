## 1
Found the cause on the flaky test: it asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC. That's the one-in-nine failure. Not fixed yet — still need to pick between a timezone-fixed assertion and forcing the test to run in a fixed zone.

## 2
The sync job isn't idempotent, so a retry after a partial run writes the same rows again. Wrapping it in a retry turns a twice-a-week failure into a twice-a-week duplication bug that's harder to spot than the original. Fix the partial-write case or add a dedup key before adding retries.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none.

Behavior change: the limit is now per-account instead of per-route-per-account. A user hitting three rate-limited routes used to get three separate budgets; now they share one.

## 4
I don't know why memory climbed 40 percent after Tuesday's deploy. Nothing in the diff allocates, and I have no profiler data pointing at a cause. Next step is a heap snapshot from an instance on the new build compared against one on the old build.
