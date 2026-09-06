## 1
Found the cause of the CI flake: the test asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC. The two zones disagree on some runs and agree on others, which is the one-in-nine failure rate and the always-passing local runs. Not fixed yet.

## 2
A retry on this job writes rows twice, because a partial run already wrote data before it failed. Wrapping the whole thing in a retry turns a twice-a-week failure into duplicate rows on whatever cadence the job happens to fail. Make the job idempotent first — an upsert on the row's natural key covers it — then add the retry.

## 3
Moves rate-limit checks out of four route handlers and into one middleware, and deletes the duplicated token-bucket code that lived in each handler. Adds a test for the 429 path, which had none before.

One behavior change: the limit was per-route-per-account, and is now per-account.

## 4
I don't know why memory climbed 40 percent after Tuesday's deploy. Nothing in that diff allocates, and I have no profiler data to look further. A heap snapshot from before and after the deploy would settle it.
