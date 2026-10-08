# Databases and Data Access

## Transaction retry

Retry deadlocks, serialization failures, and connection resets in one `WithRetry(ctx, db, fn)` wrapper with a bounded attempt count and jittered backoff. Callers then see only conflicts that persist. Two rules keep the retry correct:

- `fn` makes no call outside the database, such as an email or an API request, because a retry repeats it. Run those calls after the commit.
- `fn` reads the rows it computes from. When `fn` uses rows read before `WithRetry` started, each retry repeats the calculation on old data. The commit then overwrites another writer's change and reports no error.

## Concurrent writes

`READ COMMITTED` lets two transactions read the same stock count and both sell the last unit. Pick one guard for each contended resource and use it everywhere:

- Optimistic: `UPDATE ... SET version = version + 1 WHERE id = $1 AND version = $2`. When zero rows change, another writer updated the row first, so reload it and decide again. Use it when conflicts are rare.
- Pessimistic: `SELECT ... FOR UPDATE`, then update. Use it under heavy contention, keep the transaction short, and lock rows in a fixed order so the lock does not cause a deadlock.

`SERIALIZABLE` makes the database abort one of two conflicting transactions, which `WithRetry` then retries. Mixing optimistic and pessimistic access on one row reopens the race.
