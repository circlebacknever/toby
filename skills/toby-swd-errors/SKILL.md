---
name: toby-swd-errors
description: >-
  Contains Toby's four error steps for deciding how code handles a failure.
  Entry skills open this file by path. Do not trigger it from a user request
  alone.
disable-model-invocation: true
---

# Toby SWD Errors

When you design error handling, reduce the number of places in the code that must contain error-handling logic.

Treat each new special case that a caller must check with a branch as a sign of a design problem first. Merge it into the general case so callers do not have to know it exists.

## Error design

For a new error signal, count the handling code it requires at every level between the failure and the code that can act on it. An error signal is a thrown exception, an error return, a status code, a `Result`, or an `Option`. Work through these four steps in order and stop at the first one that applies.

1. **Define the error out of existence.** Before writing any handling, ask whether the operation's semantics can be redefined so the condition is no longer an error. Redefine the semantics only when the condition needs no response, and keep the error when a reported success would hide a bug.

2. **Mask it at the lowest level.** If a low-level module can fully handle the condition without the caller ever knowing, handle it there. Transient errors include a network blip, a database deadlock, and a rate-limit response. Put a bounded retry for them inside the module when logs show the error recurring or the caller cannot resend the request. When a limit the caller set is reached, such as its timeout, stop retrying and return the error. Retry only an operation that is safe to repeat, which means an idempotent one or one with an idempotency key the server dedupes on.

3. **Aggregate.** When the error must surface, let it propagate to one handler, such as the top of a request loop, and remove the per-call-site handlers. When that handler replies to an untrusted caller, return the error category the caller needs, and log the detail as `toby-swd-observability` describes. The reply contains no stack trace, internal identifier, or query text.

4. **Stop in the safest reachable state.** Callers cannot act on resource exhaustion, unrecoverable I/O, or a violated internal invariant. For those errors, record what diagnostics you can, and bring the failing program, process, or task to its safest available stopping point. Put that stop inside one wrapper function that checks for the condition, so call sites don't each repeat the check. Open `references/safe-stop.md` to pick that stopping point. Do not stop on an error only because it is hard to handle.

When a failure cannot be defined away, masked, or aggregated, and stopping does more harm, continue in a degraded mode designed for it.

Never redefine or mask a security or authorization outcome so the caller sees success. Such outcomes include an auth denial, a validation rejection, and a permission failure. Return each one as a result the caller acts on.

Do not throw a condition to the caller only because you cannot choose how to handle it. Prefer a design whose error handler a test can run.

## Brownfield Work

Before adding an error, validation, or retry path, find the existing ones nearby. When the same handling repeats across call sites, report the copies at file:line and the consolidation that would remove them. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a behavior change.

## Red flags

- An error signaled for a condition the API could define away.
- The same error handled at many call sites when one handler would do.
- An error eliminated or masked that callers needed.
- Elaborate recovery for a rare unrecoverable error that should stop in its safest state.
- A retry added above a client or SDK that already retries.
- Retry backoff with no jitter.
- Callers of shared state that each take locks or assume an order of tasks. Put the rules for shared mutable state and the ordering of concurrent tasks in one module.

## References

Read the stack file that matches the code.

- `references/examples.md` has one worked case each for error steps 1, 3, and 4, and the masking limit. Open it when you cannot tell which error step applies.
- `references/web.md` covers React, Solid, and Svelte error boundaries and async errors.
- `references/mobile.md` covers React Native network errors and native module errors.
- `references/backend-apis.md` covers HTTP and gRPC retries, timeouts, and circuit breakers.
- `references/databases.md` covers transaction retry and concurrent writes.
