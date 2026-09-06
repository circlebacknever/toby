## 1
Spent the afternoon on the CI flake. Found it: the test asserts on a timestamp rendered in local time, and CI runs in UTC, so the assertion drifts whenever the two clocks disagree — about one run in nine. Not fixed. Next up is pinning the test to UTC before I call it closed.

## 2
The job isn't idempotent. A partial run already writes rows, so a retry replays those writes and doubles them. Wrapping it in a retry means the job now fails in a way that quietly corrupts data on top of failing outright. Fix the partial-write case first, then add the retry.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none before.

One behavior change: the limit is now enforced per account, so a user hitting three endpoints shares a single bucket across all three, where before each route kept its own.

## 4
Don't know yet. The diff from Tuesday's deploy has nothing that allocates, and I don't have profiler data to say what's holding the extra memory. Next step is pulling a heap snapshot from a canary pod before and after the deploy to see what's actually growing.
