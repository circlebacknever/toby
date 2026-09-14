# Worked Examples — Backend APIs (Java, Go, TypeScript)

Distributed systems fail in many places, so the complexity
question is where the system handles each kind of failure, and at
what cost. The error ladder applies directly. Performance design at the
network layer is mostly about keeping the failure modes bounded.

---

## Example 1 — HTTP error categorization: retry by class, surface by intent

A client wrapper built up one change at a time:

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
The error ladder isn't applied, so everything propagates uniformly.

The HTTP status codes already signal a category, so use it:

| Status range | Class | Handling |
|---|---|---|
| 2xx | Success | Return body |
| 4xx (except 408, 429) | Client error — caller's fault | Surface; no retry |
| 408 | Transient — request never completed | Retry on a fresh connection |
| 429 | Throttled — caller is over a limit | Back off; honor `Retry-After` (delta-seconds or an HTTP date) |
| 5xx (except 501) | Transient — server issue | Retry with backoff, only when the request is safe to repeat |
| 501 | Permanent — not implemented | Surface; no retry |

A wrapper that applies the categorization:

```ts
async function callApi<T>(path: string, opts?: RequestOpts): Promise<T> {
  const maxAttempts = 3;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const res = await fetch(path, { ...opts, signal: timeoutSignal(10_000) });
      if (res.ok) return res.json();

      if (isTransient(res.status) && attempt < maxAttempts) {
        await sleep(retryAfter(res) ?? backoff(attempt));
        continue;
      }
      throw new HttpError(res.status, await res.text(), { permanent: !isTransient(res.status) });
    } catch (e) {
      // a network failure or the 10s timeout rejects fetch — it never returns a status,
      // so the transient handling above never sees it. Catch it here and retry the same way.
      if (isNetworkOrTimeout(e) && attempt < maxAttempts) {
        await sleep(backoff(attempt));
        continue;
      }
      throw e;
    }
  }
  throw new Error('unreachable');
}
```

The wrapper masks transient 5xx, 408, 429, network blips, and the timeout
abort, which is rung 2, masking at the lowest level. It surfaces 4xx, where the
caller did something wrong, and sustained 5xx, which means a real outage. The thrown `HttpError`
has a `permanent` flag so callers don't re-retry. The flag is set in one
place, which spares every call site from re-deriving the categorization.

Automatic retry is safe only when repeating the request is safe. That means an
idempotent method (GET, PUT, DELETE) or a request with an idempotency key
the server dedupes on. Retrying a non-idempotent POST after a 5xx or a timeout
can create the resource twice, because the first attempt may have committed
before the response was lost. Scope the wrapper to safe methods, or require
the key. The wrapper also passes `res.text()` along for logging at the boundary. A handler
replying to an external caller maps it to a category and a safe message first,
since a downstream body can contain stack traces or query text (rung 3).

Callers handle the typed errors in one place, usually a response
interceptor. The interceptor catches `permanent: false` (sustained outage → user-facing
"service unavailable"). It lets `permanent: true` bubble up to where the
caller can decide if it's a 404, a validation failure, or an auth problem.

---

## Example 2 — gRPC error codes: retryable vs not

gRPC defines explicit retryability via status codes:

| Code | Retry? |
|---|---|
| `UNAVAILABLE` | Yes, with backoff |
| `DEADLINE_EXCEEDED` | Only with a fresh, larger deadline |
| `RESOURCE_EXHAUSTED` | Only when the server signals throttling, with backoff |
| `ABORTED` (transaction conflict) | Retry the whole transaction with backoff, after re-reading state |
| `INTERNAL` | No — signals a broken invariant, so a bare retry hides a bug |
| `INVALID_ARGUMENT`, `NOT_FOUND`, `PERMISSION_DENIED`, and the rest | No — caller error |

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
The retryability decision is in one place (`isRetryableGRPC`), which
reads the gRPC status code and applies the table above.

Per-call-site retry logic is where this design goes wrong. When each site has
its own retry-or-not check, each check gets something slightly wrong, such as
missing the deadline propagation or double-retrying on `ABORTED`. The helper
applies the ladder in one place and masks the transient cases. Permanent errors bubble up where the
caller can act.

Deadline propagation matters. `ctx` has a deadline, and `sleepCtx`
returns early if it expires during backoff. The loop stops retrying once
the deadline is gone, and it won't sleep past it. To also skip an attempt that
can't finish in time, compare `ctx`'s remaining time against the next backoff
before the call. Deadline handling belongs in the helper, because
putting it there keeps it out of 50 call sites.

---

## Example 3 — Timeouts as performance design

The forgotten complexity is the timeout, in a service that calls a downstream service:

```ts
async function getRecommendations(userId: string): Promise<Recommendation[]> {
  return await downstreamClient.getRecommendations(userId);
}
```

The call has no timeout, and the downstream service is slow today, taking 30
seconds against a usual 50ms. This service's threads or event loop hang on
those calls, so the user's page load takes 30 seconds. The failure then
spreads, because this service now looks slow to *its* callers, which back
up their own callers in turn.

Timeout choice is a performance design decision. The cheap design-time
move:

```ts
async function getRecommendations(userId: string): Promise<Recommendation[]> {
  return await downstreamClient.getRecommendations(userId, { timeoutMs: 200 });
}
```

The 200ms timeout is a bound on the worst case. If the downstream takes
longer, the call fails fast. The retry wrapper handles that failure as a
transient, and surfaces "recommendations unavailable" if it persists
through retries. The page loads in a bounded time, even when downstream
is unhealthy.

A typical timeout is a few multiples of the downstream's P99 latency when it
is healthy. If the healthy P99 is 50ms, 200ms is generous. If the downstream
is a critical-path dependency and you must wait, keep a timeout and set it
higher, because "wait forever" is worse than "give up after 5 seconds."

For non-critical dependencies (the recommendations panel on a page that
also loads the actual content), the right move is often to render the page
without the panel, fetch the panel in the background, and insert it when it
arrives. That design move defines the recommendation's slowness out of the
user's critical path, so the timeout never applies.

Removing the panel from the critical path applies `examples.md` Example 1
("define the error out of existence") to latency. The most reliable way to handle a slow
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
- The downstream's failure mode is "slow", so calls hang and burn the full
  timeout. A retry-and-timeout policy alone causes threads to pile up, and the
  breaker prevents the pile-up by short-circuiting calls when the downstream
  is unhealthy.
- The downstream is called frequently, so the breaker has signal to act
  on.
- Backpressure has business value, because serving "I can't reach
  recommendations right now" immediately is better than holding the user's
  page for the timeout duration.

**Not earned**:
- The call is low-traffic, such as a daily cron job to a partner API. The breaker has
  no recent-failure signal, so you're paying complexity for nothing.
- The retry policy already handles the failure mode adequately. Adding a
  breaker on top is duplicated machinery.
- The downstream is "fail-fast", so a quick error from an unhealthy
  downstream doesn't pile up threads, and a breaker has nothing to prevent.

Adding a circuit breaker because "we should" is a mistake, and it produces a
piece of stateful complexity that:

- Has bugs that only surface during incidents (the worst time to find
  them).
- Has tuning parameters (window size, threshold, half-open timing) that
  nobody understands well enough to set correctly.
- Hides downstream failures from operators (the breaker has tripped, so
  calls don't appear in logs and the dashboard is misleading).

If you don't have *measured* evidence that a piling-up failure mode is
hurting users today, the circuit breaker is speculative complexity.
Don't ship it. When the evidence arrives (an outage post-mortem says
"thread pool saturated on slow downstream"), add the breaker for that
specific dependency.

---

## Example 5 — Bulk vs row-by-row API: avoid the death-by-thousand-cuts

A batch import endpoint that grew, and now creates orders one at a time:

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

500 orders means 500 sequential database round-trips. With a 2ms DB ping,
that's 1 second of network latency before any other work. The endpoint
takes 5 seconds and the client times out at 3, so the user retries, and the
retry contends with the partial import.

The design-time fix is a bulk path through the service down to a single
batched insert.

```ts
app.post('/api/orders/import', async (req, res) => {
  const result = await ordersService.createBulk(req.body.orders);
  res.json(result);
});

// in OrdersService
async createBulk(orders: NewOrder[]): Promise<ImportOutcome[]> {
  // one transaction, one round-trip; each input maps to a typed outcome
  return await this.repo.insertMany(orders);
}
```

The import makes one round trip, so the cost is bounded and all the
complexity is in one place. `insertMany` in the repository owns the bulk semantics. It decides how
big a batch is too big (chunk the input above some threshold), and what a partial
failure looks like to the caller. The return type states that contract. A
typed outcome per input (created, or rejected with a reason) lets the caller
act on a partial success. An all-or-nothing variant rejects the whole batch
and names the row that broke it. A flat array of successes can express
neither.

The row-by-row import is the same N+1 problem over a network as the mobile
bridge example. The fix is a bulk API at the boundary that crosses the network. Within
the application, the row-by-row code can stay (it's clearer), but at the
network boundary, batch.

---

## Example 6 — Shared mutable state behind one owner

Several handlers consult an in-memory rate limiter. The tactical version
exposes the state and trusts every caller to guard it:

```go
type RateLimiter struct {
    Mu     sync.Mutex
    Counts map[string]int
}

// at every call site:
rl.Mu.Lock()
rl.Counts[userID]++
over := rl.Counts[userID] > limit
rl.Mu.Unlock()
```

The locking discipline is spread across the call sites. One handler forgets to lock
and reads a torn value. Another holds the lock across a network call and
stalls everyone. A third takes this lock and a second one in the opposite
order and deadlocks. Every new call site is another chance to get one wrong.

Concentrate the discipline inside the owner:

```go
type RateLimiter struct {
    mu     sync.Mutex                 // unexported; only methods touch it
    counts map[string]int
    limit  int
}

func (rl *RateLimiter) Allow(userID string) bool {
    rl.mu.Lock()
    defer rl.mu.Unlock()
    rl.counts[userID]++
    return rl.counts[userID] <= rl.limit
}
```

Callers write `rl.Allow(userID)` and know nothing about the lock. The
critical section is one short block with no network call inside it, one
structure, and one lock, so no lock ordering can go wrong. Shared
mutable state is complexity like any other. It costs least when one module
owns it and the rules for touching it are in one place.

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
| `mutex` locked at every call site | Put the state and its lock in one type; expose methods and keep the lock hidden |
