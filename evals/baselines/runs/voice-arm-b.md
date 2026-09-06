## 1
Found the flaky test. It fails on CI about one run in nine, passes locally every time, because the assertion checks a timestamp formatted in local time and CI runs in UTC. Not fixed yet. Next step is to format both sides in UTC before comparing and rerun the suite until nine passes in a row.

## 2
A retry on this job writes the same rows twice. The sync job isn't idempotent — a partial run already wrote rows, so a retry reruns the whole thing and duplicates them. A wrapper turns a job that fails twice a week into one that corrupts data twice a week, silently. Give me a day to make the writes idempotent (upsert on the natural key, or a run id to dedupe against) and the retry wrapper becomes safe to add on top.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none.

Behavior change: the limit is now per-account, not per-route-per-account. An account hitting three routes hard will get throttled sooner than before.

Test plan: new 429 test passes; manually hit two routes back to back on one account and confirm the second one throttles.

## 4
I don't know why memory climbed 40 percent after Tuesday's deploy. The diff doesn't allocate anything new, and I don't have profiler data from before or after to point at a specific object growing. To find it I'd want a heap snapshot from a pod on the new build compared against one on the old build — that would show what's actually accumulating instead of guessing from the diff.
