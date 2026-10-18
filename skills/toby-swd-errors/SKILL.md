---
name: toby-swd-errors
description: >-
  Contains Toby's four error steps for deciding how code handles a failure. Use
  it for a failure case, a retry, a timeout, or validation. Skip it for a bug
  in error handling that already exists, which toby-bug-fix covers.
---

# Toby SWD Errors

Reduce the number of places that must contain error-handling logic. Treat a special case that callers must check with a branch as a design problem first, and fold it into the general path whenever callers don't need to act on it.

## Error design

For a new error signal (an exception, error return, status code, `Result`, or `Option`), count the handling code it adds between the failure and the caller that acts on it. Work through these four steps in order and stop at the first one that fits:

1. **Define the error out of existence.** Redefine the operation so the condition is normal behavior (such as `remove_session` ensuring the session is absent), provided a reported success wouldn't hide a bug.
2. **Mask it at the lowest level.** Handle transient failures (a network blip, database deadlock, or rate-limit response) inside the low-level module when the caller doesn't need to know. Use a bounded retry with jittered backoff only when the operation is safe to repeat (a read, an idempotent write, or a write with an `idempotency key` the server deduplicates), and stop retrying when the caller's deadline expires. Never mask or retry a cancellation signal (`CancelledError`, `context.Canceled`, `AbortError`).
3. **Aggregate.** Let errors that must surface propagate to one top-level handler (such as request middleware), wrapping the underlying error (`raise ... from err`, `%w`, `{ cause: err }`) so the root cause reaches the log (`toby-swd-observability`). Translate internal storage or transport errors at module boundaries into only the cases callers handle differently, and return only caller-safe categories to untrusted clients (omitting stack traces, internal ids, and SQL text).
4. **Stop in the safest reachable state.** On resource exhaustion, unrecoverable I/O failure, or a broken internal invariant, record diagnostics and stop the failing request, task, or process inside one checked wrapper (`references/safe-stop.md`).

When a failure can't be defined away, masked, or aggregated, and stopping does more harm, run a deliberate degraded mode. For bulk or batch operations, specify in the contract whether a failure rolls back the whole batch or returns per-item results.

Never mask an authentication, authorization, or validation failure as success, and prefer designs whose error handlers a test can trigger deterministically.

## Brownfield Work

Before adding an error, validation, or retry path to existing code, check nearby handlers and report duplicated handling at `file:line`. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a change.

## Red flags

- An error signaled for a condition the contract could define away.
- The same error caught across many call sites when one top-level handler would cover it.
- A caller-needed error or cancellation signal swallowed or masked.
- Elaborate recovery code written for an unrecoverable invariant failure.
- A retry added on top of an SDK or caller that already retries, or backoff without jitter.
- Callers acquiring locks or ordering concurrent tasks across sites when one module should manage that state.

## References

Read the reference that matches the stack:

- `references/examples.md` shows worked cases for error steps 1, 3, and 4, and over-masking.
- `references/safe-stop.md` lists the safe stopping point for each kind of program.
- `references/web.md` covers React, Solid, and Svelte error boundaries and async errors.
- `references/mobile.md` covers React Native network and native-module errors.
- `references/backend-apis.md` covers HTTP and gRPC retries, deadlines, timeouts, and circuit breakers.
- `references/databases.md` covers transaction retries and concurrent writes.
