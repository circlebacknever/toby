# Backend APIs (Java, Go, TypeScript)

## HTTP retries

Retry in one client wrapper, and pick the handling from the status class:

| Status | Handling |
|---|---|
| 4xx except 408 and 429 | Surface. Do not retry. |
| 408 | Retry on a fresh connection. |
| 429 | Back off, and honor `Retry-After` (seconds or an HTTP date). |
| 5xx except 501 | Retry with backoff when the request is safe to repeat. |
| 501 | Surface. Do not retry. |

A network failure or a timeout rejects the call with no status, so the wrapper retries it the same way as a 5xx. The wrapper sets one `permanent` flag on the error it throws, so callers do not re-derive the class or retry again. One response interceptor turns a sustained outage into "service unavailable" and lets a permanent error reach the caller that can act on it.

## gRPC retries

One helper wraps every RPC and reads the status code:

| Code | Retry? |
|---|---|
| `UNAVAILABLE` | Yes, with backoff. |
| `DEADLINE_EXCEEDED` | Only with a fresh, larger deadline. |
| `RESOURCE_EXHAUSTED` | Only when the server signals throttling. |
| `ABORTED` | Re-read state and retry the whole transaction. |
| `INTERNAL` | No, because it signals a broken invariant. |
| `INVALID_ARGUMENT`, `NOT_FOUND`, `PERMISSION_DENIED`, and every other code | No. |

The helper passes the deadline in `ctx`, stops sleeping when the deadline expires, and skips an attempt that cannot finish before it.

## Timeouts

Give every downstream call a timeout at its healthy p99.9 latency plus padding, so at most 0.1% of healthy calls time out. Without one, a slow downstream holds this service's threads, so the slowdown spreads to every caller upstream. Render a page without a non-critical dependency, such as a recommendations panel, and fill the panel in when it arrives.

## Circuit breakers

Add a circuit breaker only after a measurement or a post-mortem shows calls piling up on a slow downstream. It also needs a call frequent enough to give it a failure rate to read. Leave it out for a low-traffic call, for a downstream that already fails fast, and where the retry policy already handles the failure. A breaker has bugs that appear only during incidents and tuning values that are hard to set. It also hides tripped calls from logs and dashboards.

## Bulk calls

A loop that makes one call per row across a network turns into one batched call. 500 sequential 2 ms round trips add a second before any work runs. The bulk method chunks large input. It returns created or rejected-with-reason for each input, so the caller can act on a partial success. Code inside the process can keep its row-by-row loop.
