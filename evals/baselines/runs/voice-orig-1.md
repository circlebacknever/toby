## 1
Found it. The flaky test asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC, so about one run in nine lands on a value the two disagree on. Not fixed yet.

## 2
A retry wrapper doubles the damage instead of catching it. The job isn't idempotent: a partial run writes rows, so a retry on top writes them again, and the twice-a-week failure turns into duplicate rows instead. Fix idempotency or dedupe on write first, because wrapping it now trades a rare failure for a guaranteed one every time it retries.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none before.

Behavior change: the limit is now per-account. It was per-route-per-account, so an account hitting four routes had four separate budgets. Now it has one shared budget across all of them.

## 4
I don't know. The diff from Tuesday's deploy doesn't allocate anything I can see, and I have no profiler data to say where the 40 percent went. A heap snapshot before and after the same request load would settle it.
