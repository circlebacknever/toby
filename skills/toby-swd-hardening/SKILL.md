---
name: toby-swd-hardening
description: >-
  Contains Toby's checks that production code survives bad input, retries,
  outages, and deploys. Use it for a new entry point, job, consumer, or
  outbound call, or when the user asks to harden code. Skip it for throwaway
  code, which toby-swd-experiment covers.
---

# Toby SWD Hardening

Check new production code against the row for its kind, and state the checks that apply before writing the code.

| Code the change adds | Checks |
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

Give every endpoint and consumer input a size limit at the boundary (body size, list length, page size, upload size), rejecting oversized input with a 4xx error. In scheduled jobs and batch commands, process rows in bounded pages or batches so the job never loads an unbounded table into memory. When building a file or object-storage path from user input, use server-generated storage keys or verify that the resolved canonical path stays inside the target base directory.

Bound every connection pool, worker pool, in-memory cache, and parallel fan-out. Size database pools so `pool_size * processes_per_host * hosts` (doubled during a rolling deploy) stays below the database connection limit, and set a short connection acquire timeout (`pool_timeout=2` in SQLAlchemy, `connectionTimeoutMillis: 2000` in `node-postgres`).

## Auth

Enforce authentication and authorization on the server for every entry point using the repo's middleware, and scope record lookups to the authenticated account or tenant. Deny the request whenever an auth check fails or throws. Write a test proving signed-out requests are rejected, and seed two accounts to test that Account A can't read or mutate Account B's record.

For inbound webhooks, verify the provider's cryptographic signature against the raw request body using a constant-time comparison and check the timestamp window before parsing or queuing. Limit failed attempts per account and per IP on endpoints that check passwords, one-time codes, or reset tokens (`references/logins.md`), and limit sends per IP and per recipient on unauthenticated endpoints that send emails or SMS messages. Add other rate limits where the repo already uses them.

## Idempotent writes

Make writes safe to repeat in webhooks, queue consumers, scheduled jobs, money movements, and endpoints whose clients retry automatically:

- For status transitions, update conditionally on the prior status (`WHERE id = $1 AND status = 'open'`) and re-read the row when zero rows change.
- For inserts, increments, or payments, store the caller's `idempotency key` or webhook event id under a unique constraint in the same transaction as the write. Return the stored result when the key repeats with the same parameters, reject with `422` when the parameters differ, and return `409` while the first request is still running.
- Before sending an email or calling an external API, claim the row with an expiring lease (`references/messages.md`) when runs or redeliveries can overlap, pass the provider an `idempotency key` when supported, and record the completed send afterward.
- Test idempotency by sending the same request or message twice and asserting the side effect happened once.

## Concurrent writes

When a write depends on a value read from its row (such as claiming a ticket, decrementing stock, or transitioning status) and two requests or jobs can race, use a conditional `UPDATE ... WHERE` or `SELECT ... FOR UPDATE` (`toby-swd-errors`'s `references/databases.md`). Test concurrency below the entry point by loading the row twice, running the first write, running the second write with a different value, and asserting the first write wins.

## Outbound calls

Set an explicit timeout on every outbound HTTP, RPC, or SDK call (`toby-swd-errors`'s `references/backend-apis.md`), and never hold a database transaction or row lock open across an outbound call. When an outbound URL comes from user or webhook input, resolve the host and block loopback, private-network, link-local, and cloud-metadata IP ranges on both the initial connection and redirects. Decide in the design whether the feature fails, degrades, or queues work when the downstream service is down, and test that path.
