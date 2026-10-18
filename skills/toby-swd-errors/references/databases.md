# Databases and Data Access

This file covers transaction retry wrappers and optimistic versus pessimistic concurrency guards.

## Transaction retry

Add a `WithRetry(ctx, db, fn)` wrapper when a transaction runs at `SERIALIZABLE` or `REPEATABLE READ`, or when deadlocks or transient connection resets can occur and the caller can't resend the request. Omit the wrapper when a job queue or caller above already retries the operation. Keep the retry safe with three rules:

- Retry a connection reset only when it occurred before `COMMIT` was sent, or when `fn` records an `idempotency key` under a unique constraint and returns the existing result on a constraint conflict.
- Keep external side effects (emails, HTTP calls, queue publishes) outside `fn` and run them after commit (`toby-swd-hardening`'s `references/messages.md`).
- Read every row that `fn` computes from inside `fn`, so each retry recomputes on fresh rows and doesn't overwrite concurrent updates with stale values.

## Concurrent writes

Under `READ COMMITTED`, two concurrent transactions can read the same row and both pass a check. Pick one guard per contended table and use it consistently:

- **Optimistic:** `UPDATE ... SET version = version + 1 WHERE id = $1 AND version = $2`. When zero rows change, reload the row and re-evaluate. Use this when conflicts are rare.
- **Pessimistic:** `SELECT ... FOR UPDATE` inside a short transaction that locks rows in a fixed primary-key order to prevent deadlocks. Use this under high contention.

Don't mix optimistic and pessimistic updates on the same table, because a writer skipping the version bump or lock reopens the race.
