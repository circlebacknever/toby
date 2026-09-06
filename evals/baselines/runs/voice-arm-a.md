## 1
Found the flaky test. It fails on CI about one run in nine and passes locally every time. The assertion checks a timestamp formatted in the machine's local timezone, and CI runs in UTC, so the check only breaks when local time and UTC land on different sides of a boundary the test never accounts for. Not fixed yet.

## 2
A retry wrapper on this job duplicates rows. The job isn't idempotent: a partial run writes rows, and a retry runs the whole job again on top of them. Twice-a-week failures become twice-a-week duplicate writes, invisible until someone finds two of everything in the table. Fix the idempotency first, or put a cleanup step before the retry that removes the partial rows from the failed run.

## 3
Rate-limit checks move out of four route handlers into one middleware, and the duplicated token-bucket code goes with them. Adds a test for the 429 path, which had none.

One behavior change: the limit is now per-account, replacing the old per-route-per-account limit. An account that hits its cap on one route now blocks its other routes too.

## 4
I don't know why memory use climbed 40 percent after Tuesday's deploy. Nothing in the diff allocates, and I don't have profiler data to say what does. A profiler run comparing pre- and post-deploy would settle it.
