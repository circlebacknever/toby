## Reply 1
Postgres is choosing the seq scan on cost, not ignorance of the index. With 2M rows, if the last 30 days is a sizable fraction of the table's history, the row estimate for that range is large enough that random-access index lookups plus a heap fetch per row cost more than one sequential read. Run `EXPLAIN (ANALYZE, BUFFERS)` and compare the planner's row estimate to the actual count — if they're far apart, run `ANALYZE events` first, before touching indexes.

## Reply 2
The index on `created_at` already exists and the planner is skipping it on cost grounds, so another index doesn't fix anything here. Two things actually move this: confirm the row estimate with `ANALYZE` (stale stats can make the planner overestimate matches and bail on the index for no real reason), or drop `SELECT *` for the columns you need so an index-only scan becomes possible.

## Reply 3
That's the mechanism. A seq scan reads pages in order; an index scan pays a random-access lookup plus a heap fetch for every matching row. Once the match count crosses some fraction of the table — often in the 5-10% range — those per-row costs add up past a single sequential pass, and the planner flips to seq scan. A 30-day window out of a 2M-row table can easily be past that line.

## Reply 4
Right. Next time this happens, check `EXPLAIN ANALYZE`'s row estimate before touching anything — that number tells you which side of the line you're on.
