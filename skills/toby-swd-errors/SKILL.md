---
name: toby-swd-errors
description: >-
  Contains Toby's four error steps for deciding how code handles a failure. Use
  it for a failure case, a retry, a timeout, or validation. Skip it for a bug
  in error handling that already exists, which toby-bug-fix covers.
---

# Toby SWD Errors

Reduce the number of places that must contain error-handling logic. When callers don't need to act on a special case, fold it into the normal path so callers don't write a branch.

## Error design

For a new error signal (`Exception`, `Result`, `Option`, or status code), count the handling code it adds between the failure and the caller. Work through these four steps in order and stop at the first one that fits:

1. **Define the error out of existence.** Redefine the function so the condition is normal behavior (such as `remove_session` ensuring the session is absent) when success won't hide a bug.
2. **Mask it at the lowest level.** Handle transient failures (a network blip, database deadlock, or rate-limit response) inside the low-level module when callers don't need to know. Retry with jittered backoff only on operations that are safe to repeat (reads, idempotent writes, or writes with an `idempotency key`), and stop at the caller's deadline. Never mask or retry a cancellation signal (`CancelledError`, `context.Canceled`, `AbortError`).
3. **Aggregate.** Let errors that must surface propagate to one top-level handler, and wrap the underlying error (`raise ... from err`, `%w`, `{ cause: err }`) so the handler logs the root cause (`toby-swd-observability`). At module boundaries, translate internal storage or transport errors into only the cases callers handle differently. Return only safe error categories to untrusted clients, without stack traces, internal ids, or SQL text.
4. **Stop in a safe state.** On resource exhaustion, unrecoverable I/O failure, or a broken invariant, log diagnostics and stop the failing request, task, or process inside one wrapper (`references/safe-stop.md`).

When none of the four steps fits and stopping would cause worse harm, degrade the non-critical feature intentionally. For bulk or batch operations, state in the contract whether a failure rolls back the whole batch or returns per-item results.

Never mask an authentication, authorization, or validation failure as success, and design error handlers so a test can trigger them on demand.

## Brownfield Work

Before adding an error, validation, or retry path to existing code, check nearby handlers and report duplicated handling at `file:line`. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a change.

## Red flags

- Code signals an error for a condition the contract could define away.
- Many call sites catch the same error when one top-level handler would cover it.
- Code swallows or masks an error or cancellation signal that the caller needs.
- Code runs complex recovery logic for an unrecoverable invariant failure.
- Code adds a retry on top of an SDK or caller that already retries, or retries without jitter.
- Callers acquire locks or order concurrent tasks across sites when one module should manage that state.

## References

Read the reference that matches the stack:

- `references/examples.md` shows worked cases for error steps 1, 3, and 4, and over-masking.
- `references/safe-stop.md` lists the safe stopping point for each kind of program.
- `references/web.md` covers React, Solid, and Svelte error boundaries and async errors.
- `references/mobile.md` covers React Native network and native-module errors.
- `references/backend-apis.md` covers HTTP and gRPC retries, deadlines, timeouts, and circuit breakers.
- `references/databases.md` covers transaction retries and concurrent writes.
