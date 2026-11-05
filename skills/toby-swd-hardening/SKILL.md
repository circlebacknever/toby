---
name: toby-swd-hardening
description: >-
  Contains Toby's checks that production code survives bad input, retries,
  outages, and deploys. Use it when a change affects input bounds, auth,
  writes, retries, concurrency, external calls, or stored formats, including
  existing paths, or when the user asks to harden code. Skip it for throwaway
  code, which toby-swd-experiment covers.
---

# Toby SWD Hardening

Check added or changed production behavior against the applicable rows, and state the relevant failure and invariant checks before writing the code. Reusing an existing entry point doesn't waive them.

| Code the change affects | Checks |
| --- | --- |
| HTTP or RPC endpoint | bounds, auth, outcome log, idempotent writes in the cases below |
| Queue consumer | bounds, idempotent writes, outcome log, poison messages in `references/messages.md` |
| Scheduled job | bounds, idempotent writes, outcome log |
| CLI or script | pool and batch limits from Bounds, and idempotent writes when it writes data |
| Library | pool and concurrency limits from Bounds |
| A write that depends on a value read from its row under concurrency | concurrent writes |
| A call to another service | outbound calls |
| A database write plus a message or external call | dual writes in `references/messages.md` |
| A message, cache entry, stored field, or migration | `references/deploys.md` |

`toby-swd-twelve-factor` covers graceful shutdown, health checks, and process state, and `toby-swd-observability` defines the outcome log.

## Bounds

Cap every endpoint and consumer input at the boundary (body size, list length, page size, upload size), and reject oversized input with a 4xx status. In scheduled jobs and batch commands, process rows in bounded pages or batches so the job never loads an unbounded table into memory. When building a file or storage path from user input, generate server-side storage keys or verify that the resolved path stays inside the base directory.

Bound every connection pool, worker pool, in-memory cache, and parallel fan-out. Size database pools so `pool_size * processes_per_host * hosts` (doubled during a rolling deploy) stays below the database connection limit. Set a short connection acquire timeout (`pool_timeout=2` in SQLAlchemy, `connectionTimeoutMillis: 2000` in `node-postgres`).

## Auth

Enforce authentication and authorization on the server for every entry point using the repo's middleware, and scope record lookups to the authenticated account or tenant. Deny the request whenever an auth check fails or throws. Write a test proving the server rejects signed-out requests, and seed two accounts to test that Account A can't read or mutate Account B's record.

For inbound webhooks, verify the provider's signature on the raw request body with a constant-time comparison and check the timestamp window before parsing. Limit failed attempts per account and per IP on password, one-time-code, and reset-token endpoints (`references/logins.md`). Also limit sends per IP and per recipient on unauthenticated endpoints that send emails or SMS messages, and add other rate limits where the repo uses them.

## Idempotent writes

Make writes safe to repeat in webhooks, queue consumers, scheduled jobs, money movements, and endpoints whose clients retry automatically:

- For status transitions, update conditionally on the prior status (`WHERE id = $1 AND status = 'open'`) and re-read the row when zero rows change.
- For inserts, increments, or payments, save the caller's `idempotency key` or webhook event id under a unique constraint in the same transaction. Return the stored result when the key repeats with identical parameters, reject with `422` when parameters differ, and return `409` while the first request is running.
- When runs or redeliveries can overlap before an email or external API call, claim the row with an expiring lease (`references/messages.md`). Pass the provider an `idempotency key` when the provider accepts one, and record the completed send afterward.
- Test idempotency by sending the same request or message twice and asserting the side effect happened once.

## Concurrent writes

When a concurrent write depends on a value read from its row, use a conditional `UPDATE ... WHERE` or `SELECT ... FOR UPDATE`. See `toby-swd-errors`'s `references/databases.md` for transaction handling. Check the invariant with the repo's test database and separate transactions or connections.

Coordinate contenders so the second reaches the contested operation while the first is active. Use a barrier or latch at a safe point. Bound the wait, release both operations, and assert the permitted final state and side-effect count.

Two sequential writes check stale data handling but don't prove locking or race safety. When the environment can't run an overlapping test, state that limit.

## Outbound calls

Set an explicit timeout on every outbound HTTP, RPC, or SDK call (`toby-swd-errors`'s `references/backend-apis.md`), and never keep a database transaction or row lock open across an outbound call. When an outbound URL comes from user or webhook input, resolve the host and block loopback, private-network, link-local, and cloud-metadata IPs on the request and any redirect. Decide in the design whether the feature fails, degrades, or queues work when the downstream service is down, and test that path.
