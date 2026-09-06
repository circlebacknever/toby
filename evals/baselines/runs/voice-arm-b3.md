## 1
Found the flaky test. It fails on CI about one run in nine and passes locally every time because the assertion checks a timestamp formatted in the machine's local timezone, and CI runs in UTC — local matches by coincidence, UTC doesn't. I have the cause, not the fix yet. Patch is to format both sides in a fixed timezone before comparing; I'll do that next.

## 2
A retry wrapper doubles the damage here. The job isn't idempotent — a partial run already wrote rows, and a retry writes them again — so wrapping it keeps the failure rate at twice a week and adds duplicate rows every time it fires. Fix the idempotency (make the write upsert on a key, or checkpoint what already landed) or gate the retry behind a check that the last run didn't partially complete. Either is smaller than the cleanup job you'd be writing in a month to de-dupe production.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code behind them. Adds a test for the 429 path, which had none.

One behavior change: the limit now applies once per account across all four routes, where before each route tracked its own quota per account. An account hitting all four routes could burn four times the intended rate before; now it can't.

## 4
I don't know. I read the diff for Tuesday's deploy and nothing in it allocates — no new caches, no buffers, nothing that explains a 40 percent jump. I don't have profiler data, so I can't say where the memory's actually going. Need a heap snapshot from a prod instance, or a repro I can run under a profiler, before I can name the source instead of guessing at it.
