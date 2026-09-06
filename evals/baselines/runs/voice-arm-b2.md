## 1
Spent the afternoon on the flaky test. Found the cause: it asserts on a timestamp formatted in local timezone, and CI runs in UTC, so it fails there about one run in nine and never locally. Not fixed yet — next step is making the assertion timezone-independent.

## 2
A retry on that job writes the rows again. The sync isn't idempotent — a partial run already wrote some rows, so a retry duplicates them instead of recovering. Wrapping it in retries turns a twice-a-week failure into a data problem you won't notice until the totals are wrong. Fix the idempotency first, or gate the retry on a check for rows already written.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket implementations. Adds a test for the 429 path, which had none.

Behavior change: the limit is now enforced per-account instead of per-route-per-account. An account hitting several routes will throttle sooner than before.

## 4
I don't know. I read the diff from last Tuesday's deploy and nothing in it allocates, but I have no profiler data, so I can't point to where the memory is going. Getting a heap snapshot from before and after the deploy would settle it.
