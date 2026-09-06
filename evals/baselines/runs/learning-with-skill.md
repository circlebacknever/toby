## Reply 1
The index existing doesn't make the planner use it. Postgres picks whichever plan it estimates is cheaper, and past some fraction of the table, reading everything sequentially beats jumping through an index one row at a time to fetch scattered pages.

30 days out of 2M rows could be a large slice if events land continuously. If that slice is 20-30% of the table, a seq scan is the cheaper plan.

Run this and tell me the number: `SELECT count(*) FROM events WHERE created_at > now() - interval '30 days'`. What fraction of 2M does that come out to?

## Reply 2
More indexes won't move this one. The index on `created_at` is already there — the planner is weighing its cost against a seq scan and picking seq scan, so a second index gets weighed the same way and loses the same way.

Indexes aren't free either: every insert on `events` now writes to the index as well as the table.

Say that 30-day window matched 0.1% of rows instead of 20%. Does the planner's answer change, and why?

## Reply 3
Right — and chase the "not sure." What is the planner comparing the index scan's cost against, and what's the actual number that tips it toward seq scan?

## Reply 4
That's the rule: past some row-count threshold, the random I/O of index lookups costs more than reading the table straight through, and the planner is pricing that trade, not ignoring your index.

Run the count query from the first message. If recent rows are more than roughly 5-10% of the table, seq scan is the correct plan as it stands, and the fix (if you want one) is a partial index scoped to a narrow recent window, not a second index on the same column. Unverified until you've run the count and seen the real ratio.
