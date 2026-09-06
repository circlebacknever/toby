## 1
The CI flake is a timezone bug. The test asserts on a timestamp formatted in the machine's local zone, and CI runs UTC, so it fails whenever the two zones disagree on the hour. That is the one-in-nine. Not fixed yet.

## 2
A retry replays a job that already wrote rows, and the second run writes them again. Wrapping the sync job in a retry doubles the twice-a-week failure into a duplicate-data problem, on top of it. Fix idempotency first, or the retry is a bug generator with a schedule.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none. The limit changes from per-route-per-account to per-account: a user hitting two routes now shares one bucket instead of getting one each.

## 4
I don't know. I read the diff from last Tuesday's deploy and nothing in it allocates, and I have no profiler data from before or after. A heap snapshot from before and after the deploy would tell us whether the growth is a leak or a larger resident working set.
