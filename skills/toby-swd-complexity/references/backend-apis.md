# Worked Examples — Backend APIs (Java, Go, TypeScript)

Distributed systems have one defining property: things fail. The complexity
question is not "how to prevent failures" but "where in the system does
each kind of failure get absorbed, and at what cost." The error ladder
applies directly; performance design at the network layer is mostly about
keeping the failure modes bounded.

---

## Example 1 — HTTP error categorization: retry by class, surface by intent

A client wrapper that grew organically:

```ts
async function callApi(path: string, opts?: RequestOpts): Promise<any> {
  try {
    const res = await fetch(path, opts);
    if (!res.ok) {
      throw new HttpError(res.status, await res.text());
    }
    return res.json();
  } catch (e) {
    throw e;
  }
}
```

Every caller now handles every HTTP status. Callers retry on their own,
treat 503 as a real "service is down" failure, surface 500 to the user.
The error ladder isn't applied; everything propagates uniformly.

The HTTP status codes already carry a category signal — use it:

| Status range | Class | Handling |
|---|---|---|
| 2xx | Success | Return body |
| 4xx (except 408, 429) | Client error — caller's fault | Surface; no retry |
| 408, 429 | Transient — retry-after applies | Retry with backoff (honor `Retry-After` header) |
| 5xx (except 501) | Transient — server issue | Retry with backoff |
| 501 | Permanent — not implemented | Surface; no retry |

A wrapper that applies the categorization:

```ts
async function callApi<T>(path: string, opts?: RequestOpts): Promise<T> {
  const maxAttempts = 3;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    const res = await fetch(path, { ...opts, signal: timeoutSignal(10_000) });
    if (res.ok) return res.json();

    if (isTransient(res.status) && attempt < maxAttempts) {
      const wait = retryAfter(res) ?? backoff(attempt);
      await sleep(wait);
      continue;
    }

    throw new HttpError(res.status, await res.text(), { permanent: !isTransient(res.status) });
  }
  throw new Error('unreachable');
}
```

What this absorbs (rung 2, mask at lowest level): transient 5xx, 408, 429,
network blips. What it surfaces: 4xx (caller did something wrong) and
sustained 5xx (real outage). The thrown `HttpError` carries a `permanent`
flag so callers don't re-retry; one flag, set in one place, instead of
re-deriving the categorization at every call site.

Callers handle the typed errors at one place — usually a response
interceptor that catches `permanent: false` (sustained outage → user-facing
"service unavailable") and lets `permanent: true` bubble up where the
caller can decide if it's a 404, a validation failure, an auth problem.

---

## Example 2 — gRPC error codes: retryable vs not

gRPC defines explicit retryability via status codes:

| Code | Retry? |
|---|---|
| `UNAVAILABLE` | Yes |
| `DEADLINE_EXCEEDED` | Maybe (with new deadline) |
| `RESOURCE_EXHAUSTED` | With backoff |
| `ABORTED` (transaction abort) | Yes |
| `INTERNAL` | Sometimes (server-defined) |
| `INVALID_ARGUMENT`, `NOT_FOUND`, `PERMISSION_DENIED`, etc. | No — caller error |

A Go server-to-server client:

```go
func (c *OrdersClient) GetOrder(ctx context.Context, id string) (*Order, error) {
    return retryGRPC(ctx, 3, func(ctx context.Context) (*Order, error) {
        return c.stub.GetOrder(ctx, &orderspb.GetOrderRequest{Id: id})
    })
}

func retryGRPC[T any](ctx context.Context, maxAttempts int, fn func(context.Context) (T, error)) (T, error) {
    var zero T
    for attempt := 1; ; attempt++ {
        result, err := fn(ctx)
        if err == nil {
            return result, nil
        }
        if !isRetryableGRPC(err) || attempt >= maxAttempts {
            return zero, err
        }
        if err := sleepCtx(ctx, backoff(attempt)); err != nil {
            return zero, err
        }
    }
}
```

`retryGRPC` is one function. Every RPC client method wraps its call in it.
The retryability decision lives in one place (`isRetryableGRPC`), which
reads the gRPC status code and applies the table above.

Compare to the alternative — every RPC call site writing its own
retry-or-not logic, getting it slightly wrong, missing the deadline
propagation, double-retrying on `ABORTED`. The ladder collapses into one
helper, masking the transient cases. Permanent errors bubble up where the
caller can act.

Deadline propagation matters: `ctx` carries a deadline; if the deadline
is near or past, don't retry. `retryGRPC` reads the deadline from `ctx`
and exits when there isn't enough time for another attempt. This is the
kind of complexity that lives in the helper, not in 50 call sites.

---

## Example 3 — Timeouts as performance design

The forgotten complexity. A service calls a downstream service:

```ts
async function getRecommendations(userId: string): Promise<Recommendation[]> {
  return await downstreamClient.getRecommendations(userId);
}
```

No timeout. The downstream service is slow today, taking 30 seconds
instead of its usual 50ms. This service's threads/event-loop hang on
those calls. The user's page-load takes 30 seconds. Cascading failure:
this service now appears slow to *its* callers, which back up, which
... and so on.

Timeout choice is a performance design decision. The cheap design-time
move:

```ts
async function getRecommendations(userId: string): Promise<Recommendation[]> {
  return await downstreamClient.getRecommendations(userId, { timeoutMs: 200 });
}
```

The 200ms timeout is a bound on the worst case. If the downstream takes
longer, the call fails fast (handled as a transient by the retry
wrapper, then surfaced as "recommendations unavailable" if it persists
through retries). The page loads in a bounded time, even when downstream
is unhealthy.

How to choose the timeout: typically a few multiples of the P99 latency
of the downstream's healthy behavior. If P99 is 50ms healthy, 200ms is
generous. If the downstream is a critical-path dependency and you must
wait, the timeout still exists — just higher — because "wait forever" is
worse than "give up after 5 seconds."

For non-critical dependencies (the recommendations panel on a page that
also loads the actual content), the right move is often "render the page
without it; fetch in the background; insert when it arrives." That is
not a timeout move — it's a design move that defines the recommendation's
slowness out of the user's critical path entirely.

This is the same shape as `examples.md` Example 1 ("define the error out
of existence") applied to latency: the most reliable way to handle a slow
dependency is to remove it from your critical path.

---

## Example 4 — Circuit breakers: when complexity is earned

A circuit breaker is a stateful wrapper around a downstream call that:

- Tracks recent failure rate.
- "Trips" (stops calling) when failures cross a threshold.
- Periodically tests the downstream to see if it's healthy again.
- "Closes" (resumes calling) when test calls succeed.

Libraries: `resilience4j` (Java), `gobreaker` (Go), `cockatiel` (TypeScript).

When does the complexity pay for itself?

**Earned**:
- The downstream's failure mode is "slow" rather than "fast error." A
  retry-and-timeout policy alone causes threads to pile up; the breaker
  prevents the pile-up by short-circuiting calls when the downstream is
  unhealthy.
- The downstream is called frequently, so the breaker has signal to act
  on.
- Backpressure has business value: serving "I can't reach recommendations
  right now" immediately is better than holding the user's page for the
  timeout duration.

**Not earned**:
- Low-traffic call (a daily cron job to a partner API). The breaker has
  no recent-failure signal; you're paying complexity for nothing.
- The retry policy already handles the failure mode adequately. Adding a
  breaker on top is duplicated machinery.
- The downstream is "fail-fast" — a quick error from an unhealthy
  downstream doesn't pile up threads. A breaker prevents nothing.

The mistake — adding a circuit breaker because "we should" — produces a
piece of stateful complexity that:

- Has bugs that only surface during incidents (the worst time to find
  them).
- Has tuning parameters (window size, threshold, half-open timing) that
  nobody understands well enough to set correctly.
- Hides downstream failures from operators (the breaker has tripped, so
  calls don't appear in logs; the dashboard is misleading).

If you don't have *measured* evidence that a piling-up failure mode is
hurting users today, the circuit breaker is speculative complexity.
Don't ship it. When the evidence arrives (an outage post-mortem says
"thread pool saturated on slow downstream"), add the breaker for that
specific dependency.

---

## Example 5 — Bulk vs row-by-row API: avoid the death-by-thousand-cuts

A batch import endpoint that grew:

```ts
// POST /api/orders/import
// body: { orders: Order[] }
app.post('/api/orders/import', async (req, res) => {
  const created: Order[] = [];
  for (const order of req.body.orders) {
    const result = await ordersService.create(order);     // one DB round-trip each
    created.push(result);
  }
  res.json(created);
});
```

500 orders means 500 sequential database round-trips. With a 2ms DB ping
that's 1 second of network latency before any actual work. The endpoint
takes 5 seconds. The client times out at 3. The user retries. Now there's
contention because of the partial import. Operationally a disaster.

The design-time fix: a bulk path through the service down to a single
batched insert.

```ts
app.post('/api/orders/import', async (req, res) => {
  const created = await ordersService.createBulk(req.body.orders);
  res.json(created);
});

// in OrdersService
async createBulk(orders: NewOrder[]): Promise<Order[]> {
  return await this.repo.insertMany(orders);   // one transaction, one round-trip
}
```

One round trip. The cost is bounded. The complexity gain: `insertMany`
in the repository owns the bulk semantics — what happens if some inserts
violate constraints (all-or-nothing transaction, or per-row reporting),
how big a batch is too big (chunk the input above some threshold), what
returns to the caller (typed results per input).

This is the same shape as the mobile bridge example — N+1 over a network.
The cure is bulk APIs at the boundary that crosses the network. Within
the application, the row-by-row code can stay (it's clearer), but at the
network boundary, batch.

---

## Cheat sheet — backend API complexity

| Symptom | Move |
|---|---|
| Every caller catches and retries HTTP errors | Categorize by status class; retry in the client wrapper |
| gRPC retry logic at every call site | One `retryGRPC` helper; retryability decision in one place |
| No timeouts on downstream calls | Always set a timeout; cascading failure is a slow death |
| Circuit breaker because "we should" | Add only when measured thread-pile-up is hurting users |
| Loop of API calls (N+1 over the network) | Bulk endpoint; one round trip |
| Slow non-critical dependency on critical path | Move it off the critical path; render-then-fill |
