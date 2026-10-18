# Backend APIs

This file covers HTTP and gRPC retry rules, deadlines, timeouts, and circuit breakers in backend services.

## HTTP retries

When step 2 of `toby-swd-errors` calls for a retry, put it in one client wrapper with jittered exponential backoff:

| Status | Handling |
|---|---|
| 4xx except 408 and 429 | Surface immediately without retrying. |
| 408 | Retry on a fresh connection only when the request is safe to repeat. |
| 429 | Retry at the `Retry-After` time (or with backoff), unless that time exceeds the caller's deadline. |
| 5xx except 501, or network timeout | Retry with jittered backoff only when the request is safe to repeat. |
| 501 | Surface immediately without retrying. |

Cap total attempts across service hops with a propagated deadline or a retry budget so retries at multiple layers don't multiply load during an outage. Mark terminal errors on the thrown error object so callers above the wrapper don't retry them a second time.

## gRPC retries

Wrap RPC calls in one helper that checks the status code and respects the deadline on `ctx`:

| Code | Retry? |
|---|---|
| `UNAVAILABLE` | Yes, with jittered backoff, when the RPC is safe to repeat. |
| `DEADLINE_EXCEEDED` | Only with a new deadline when the caller initiates a fresh retry and the RPC is safe to repeat. |
| `RESOURCE_EXHAUSTED` | Only on explicit server throttling when the RPC is safe to repeat. |
| `ABORTED` | Re-read state and retry the full transaction. |
| `INTERNAL`, `INVALID_ARGUMENT`, `NOT_FOUND`, `PERMISSION_DENIED` | Never retry. |

## Timeouts

Set each outbound timeout to the dependency's healthy p99.9 latency plus margin, or match the repo's existing outbound clients (defaulting to a few seconds). Without a timeout, a slow dependency ties up worker threads and cascades upstream. When a dependency is non-critical (such as a recommendations panel), degrade gracefully when its timeout expires.

## Circuit breakers

Add a circuit breaker only after measurements or an incident show requests queuing behind a slow, high-traffic downstream service. Omit circuit breakers on low-traffic calls or services that already fail fast.
