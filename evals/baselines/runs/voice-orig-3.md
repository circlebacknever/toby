## 1
Found the flaky test. It asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC, so about one run in nine the two disagree. Not fixed yet. Next step is to force the assertion onto a fixed timezone or format the expected value the same way the code under test does.

## 2
A retry wrapper doubles the damage instead of fixing it. The sync job isn't idempotent: a partial run writes rows, and a retry on top of that writes them again, so twice a week you'd go from one failure to one failure plus a pile of duplicate rows to clean up by hand. Fix the job to be safe to retry first, then wrap it.

## 3
Moves rate-limit checks out of the four route handlers and into one middleware, and deletes the duplicated token-bucket code that lived in each one. Adds a test for the 429 path, which had none.

One behavior change: the limit is now per-account instead of per-route-per-account. An account hitting two routes now shares one budget instead of getting one per route.

## 4
I don't know. The diff from Tuesday's deploy doesn't show anything that allocates, and I don't have profiler data from before or after the climb. A heap snapshot from a process at the higher baseline, compared against one from before the deploy, would tell us whether it's a leak, a bigger cache, or a bigger working set from more traffic.
