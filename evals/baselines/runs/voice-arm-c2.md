## 1
Found it. The flaky test asserts on a timestamp formatted in the machine's local timezone. CI runs UTC, so the string mismatches about one run in nine, and locally it always matches because the box never changes zones. Not fixed yet — next step is to format both sides to UTC before comparing.

## 2
The sync job is not idempotent. A partial run writes rows, and a retry on top of that writes them again, so a retry wrapper turns a twice-a-week failure into a twice-a-week duplication bug that shows up somewhere downstream, later, and harder to trace. Fix the retry only after the job can tell "already wrote this" from "haven't yet" — a run id per batch, or an upsert instead of an insert.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket code behind them. Adds a test for the 429 path, which had none.

Behavior change: the limit is now per-account, not per-route-per-account. An account hitting three routes now shares one bucket across all three instead of getting three separate ones.

## 4
I don't know. I read the diff from last Tuesday's deploy and nothing in it allocates, so the change isn't an obvious source. I have no profiler data — no heap snapshot, no before/after comparison — and without one I'm guessing if I name a cause. Getting a heap snapshot from before and after the climb would settle it.
