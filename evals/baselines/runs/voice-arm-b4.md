## 1
Found the cause of the flaky test, haven't fixed it yet. It fails on CI about one run in nine, passes locally every time, because the assertion checks a timestamp formatted in the machine's local timezone and CI runs UTC. My local clock happens to agree with the assertion's assumption; a runner in a different timezone would fail every time, not one run in nine. Fix is to format both sides to the same timezone before comparing. Haven't touched the code.

## 2
A retry wrapper turns a twice-a-week failure into a data-corruption bug. The job isn't idempotent: a partial run already writes rows, so retrying it replays those inserts on top of the ones already there. Right now a failure is visible — the job stops, you see it in the logs. Wrap it in a retry and the failure disappears while the duplicate rows stay. Make the job idempotent first, or wrap each run in a transaction that rolls back on partial failure. The retry sits on top of that fix, once it exists.

## 3
Moves rate-limit checks out of four route handlers into one middleware and deletes the duplicated token-bucket implementation. Adds a test for the 429 path, which didn't have one.

Behavior change: the limit used to apply per route per account. Now it applies per account, across every route. An account hammering three routes at once hits the limit sooner than it would have before.

## 4
Don't know yet. The diff for Tuesday's deploy has nothing that allocates, so whatever's driving the 40 percent climb isn't in what changed that day. No profiler data collected. A heap snapshot before and after, or an allocation diff under load, would settle it — haven't run either.
</content>
</invoke>
