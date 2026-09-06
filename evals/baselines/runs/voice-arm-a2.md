## 1
Found the cause on the flaky test. It asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC, so it fails there about one run in nine and passes here every run. Not fixed yet. Next is comparing the assertion in UTC or pinning the test's timezone in CI, and I have not picked.

## 2
That sync job is not idempotent. A partial run writes rows, and a retry replays the same write and duplicates them. A retry wrapper turns two failures a week into duplicate rows on every one of those retries. Put an upsert or a dedupe key on the write first, then wrap it in retries.

## 3
Moves rate-limit checks out of the four route handlers and into one middleware, and deletes the duplicated token-bucket code that lived in each of them. Adds a test for the 429 path, which had none before.

Behavior change: the limit applied per route per account, and now applies per account across all routes.

## 4
I don't know why memory climbed 40 percent after Tuesday's deploy. Nothing in the diff allocates, and I have no profiler data. A heap snapshot from before and after the deploy would settle it.
