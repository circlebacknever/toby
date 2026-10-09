# Databases and Data Access

## Transaction retry

Add one `WithRetry(ctx, db, fn)` wrapper only when a transaction runs at `SERIALIZABLE` or `REPEATABLE READ`, or when logs or tests show deadlocks. The wrapper retries deadlocks, serialization failures, and connection resets with a bounded attempt count and jittered backoff. Callers then see only conflicts that persist. Leave it out when a caller above already retries the whole operation, such as a webhook sender, a job queue, or the next scheduled run. These rules keep the retry correct:

- Retry a connection reset that happened before COMMIT was sent. After COMMIT is sent, the server may have committed, so retry only when `fn` inserts a row under an idempotency key that the caller sends. When that retry fails on the key's unique constraint, return the first result.
- `fn` makes no call outside the database, such as an email or an API request, because a retry repeats it. Run those calls after the commit, as `toby-swd-hardening`'s `references/messages.md` describes for dual writes.
- `fn` reads the rows it computes from. When `fn` uses rows read before `WithRetry` started, each retry repeats the calculation on old data. The commit then overwrites another writer's change and reports no error.

## Concurrent writes

`READ COMMITTED` lets two transactions read the same stock count and both sell the last unit. Pick one guard for each contended resource and use it everywhere:

- Optimistic: `UPDATE ... SET version = version + 1 WHERE id = $1 AND version = $2`. When zero rows change, another writer updated the row first, so reload it and decide again. Use it when conflicts are rare.
- Pessimistic: `SELECT ... FOR UPDATE`, then update. Use it under heavy contention, keep the transaction short, and lock rows in a fixed order so the lock does not cause a deadlock.

`SERIALIZABLE` makes the database abort one of two conflicting transactions, which `WithRetry` then retries. Mixing optimistic and pessimistic access on one row reopens the race.
