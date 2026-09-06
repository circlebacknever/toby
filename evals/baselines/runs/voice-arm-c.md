## 1
Found the flaky test. It asserts on a timestamp formatted in local time, and CI runs UTC, so the assertion drifts whenever the machine's offset changes the rendered string. That explains the one-in-nine rate and why it never reproduces locally. Not fixed yet — next step is switching the assertion to a fixed timezone or a UTC-normalized format.

## 2
A retry on this job writes the rows twice. The sync isn't idempotent: a partial run already writes rows, so a retry after a partial failure duplicates them instead of recovering. A wrapper would turn a twice-a-week failure into a twice-a-week data-corruption incident, just a quieter one. Fix the write path to upsert or track a watermark first, then retries are safe to add.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code. Adds a test for the 429 path, which had none before.

Behavior change: the limit is now per-account instead of per-route-per-account. An account hitting three routes now shares one bucket instead of getting three, so accounts near the old ceiling will throttle sooner.

## 4
I don't know. The diff from Tuesday's deploy has nothing that allocates, and I don't have profiler data to say what's actually holding memory. Next step is a heap snapshot from a production instance before and after load, since guessing from the diff alone isn't going to find it.
