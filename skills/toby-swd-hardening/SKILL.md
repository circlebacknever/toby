---
name: toby-swd-hardening
description: >-
  Contains Toby's checks that production code survives bad input, retries,
  outages, and deploys. Entry skills open this file by path. Do not trigger it
  from a user request alone.
disable-model-invocation: true
---

# Toby SWD Hardening

Check new production code against the list for its kind. State the checks that apply before you write the code.

| Code the change adds | Checks |
| --- | --- |
| HTTP or RPC endpoint | bounds, auth, outcome log, idempotent writes in the cases below |
| Queue consumer | bounds, idempotent writes, outcome log, poison messages in `references/messages.md` |
| Scheduled job | idempotent writes, outcome log |
| CLI or script | pool limits from Bounds, and idempotent writes when it writes data |
| Library | pool limits from Bounds |
| A write that depends on a value read from its row, when two requests or job runs can reach that row at once | concurrent writes |
| A call to another service | outbound calls |
| A database write plus a message or a call | dual writes in `references/messages.md` |
| A message, cache entry, stored field, or migration | `references/deploys.md` |

`toby-swd-twelve-factor` covers shutdown, health checks, and state kept in the process. `toby-swd-observability` defines the outcome log.

## Bounds

Give each input to an endpoint or a consumer a limit at the boundary. A body limit in the framework or the proxy counts, such as Express `json()` at 100 kB or Django's `DATA_UPLOAD_MAX_MEMORY_SIZE`. Add limits for list length, page size, and uploads the framework does not cap. Reject input over a limit with an error the caller can read.

In every kind of code, limit each pool, worker count, cache, and fan-out of parallel calls. Size a database pool so its size times the processes on every instance, doubled during a rolling deploy, stays under the database's connection limit. Give a database pool a size and a short acquire timeout, such as SQLAlchemy `pool_timeout=2` or node-postgres `connectionTimeoutMillis: 2000`, because node-postgres waits forever by default.

## Auth

Check authentication and authorization on the server for each new entry point, with the repo's middleware. Check that the caller may act on the record it names, such as by looking up the order within the caller's account. When a check fails or throws, deny the request. For an entry point that requires sign-in, test that a signed-out request is denied. When the entry point reads or changes an account's records, seed records for two accounts. Test that the caller cannot read or change the other account's record.

Limit failed attempts per account and per IP on each endpoint that checks a password, a one-time code, or a reset token, as `references/logins.md` says. Add other rate limits only where the repo already has one you can cite at path:line. Also limit sends per IP and per recipient on a new endpoint that emails or texts an address a signed-out caller enters.

## Idempotent writes

Make a write safe to run twice in each of these, because each one can run again after a timeout or a redelivery:

- a webhook
- a queue consumer
- a scheduled job
- a money movement
- an endpoint whose client retries on its own

For any other endpoint, add an idempotency key only where the repo already uses them.

When the write changes a row's status, make it conditional on the old status, such as `AND status = 'open'`, and re-read the row when zero rows change. For an insert or an increment, store the id the caller sends, such as the webhook's event id, under a unique constraint. Return the first result when that id repeats. Insert the id in the same transaction as the write it guards, so a crash rolls back both.

Before an email or another effect outside the database, check for a sent record under the business id, such as the invoice id. Write the record after the send. A crash between the send and the write can still send twice, so pass the provider an idempotency key when its API takes one.

When two runs of a scheduled job, or two deliveries of one message, can overlap, claim the row before the send, as `references/messages.md` shows. Runs overlap when cron runs on several hosts or a run outlasts its interval. A Kubernetes CronJob can also start one run twice. Two deliveries overlap when a consumer runs longer than the queue's visibility timeout, such as the SQS default of 30 seconds.

In a test, send the same message twice and check for one effect.

## Concurrent writes

Make the write conditional, or lock the row, when the write depends on a value read from its row. Such writes include a ticket claim, a counter, and a status change allowed only from certain statuses. Skip this check when only one request or job run can reach the row at a time.

An example of a conditional write is `UPDATE tickets SET agent_id = $1 WHERE id = $2 AND agent_id IS NULL`. Zero changed rows means the ticket already has an agent or does not exist. Re-read the row, and return success when the caller already holds the ticket. `toby-swd-errors`'s `references/databases.md` covers the choice.

Test the operation directly, below the entry point. Load the row twice, run the first write, then run the second with a different value, and assert that the first value stays. A test that sends two claims in sequence passes even when the read and the write are separate statements.

## Outbound calls

Give each call to another service a timeout, because Python `requests` and Go's `http.Client` wait forever by default. `toby-swd-errors`'s `references/backend-apis.md` says how to pick the value. Decide in the design whether the feature fails, degrades, or queues the work when the service is down, and test that path. Retry only a call that is safe to repeat, as step 2 of `toby-swd-errors` defines.
