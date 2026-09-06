## 1
Found the cause of the flaky test: it asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC, so the assertion breaks whenever the two clocks land on different sides of midnight or a DST boundary. That's why it passes locally every time and fails on CI about once in nine — the local machine and the code under test share a timezone, CI doesn't. Not fixed yet. Next step is formatting the timestamp in UTC in both places.

## 2
The job isn't idempotent: a run that writes rows through 60 percent, then fails, gets retried from the top, and the first 60 percent of rows get written twice. A retry wrapper here papers over the twice-a-week failure and doubles data on every partial run. Fix idempotency before adding retries, or scope retries to a step that's already safe to repeat.

## 3
Moves rate-limit checks out of the four route handlers that each ran their own copy, into one middleware, and deletes the token-bucket code duplicated across them. Adds a test for the 429 path, which had none.

One behavior change: the limit is now per-account instead of per-route-per-account. An account that used to get four separate allowances, one per route, now gets one shared allowance across all four.

## 4
I don't know why memory climbed 40 percent after Tuesday's deploy. The diff doesn't allocate anything new, so if the deploy caused it, the cause is indirect — a retained reference, a cache that grows without an eviction path, something the change triggers rather than contains. I don't have profiler data. A heap snapshot from before and after the deploy would show where the memory is actually going.
