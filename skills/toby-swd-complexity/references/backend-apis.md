# Worked Examples — Backend APIs (Java, Go, TypeScript)

Distributed systems fail in many places, so the complexity
question is where the system handles each kind of failure, and at
what cost. The error ladder applies directly. Performance design at the
network layer is mostly about keeping the failure modes bounded.

---

## Example 1 — HTTP error categorization: retry based on the error class, and surface errors based on their intent

This client wrapper was built up one change at a time:

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
treat 503 as a real "service is down" failure, and surface 500 to the user.
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

This wrapper applies the categorization:

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
      // a network failure or the 10s timeout rejects fetch. The rejected fetch returns no status,
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

The wrapper masks transient 5xx, 408, 429, brief network failures, and the timeout
abort. That masking at the lowest level is rung 2. It surfaces 4xx, where the
caller did something wrong, and sustained 5xx, which means a real outage. The thrown `HttpError`
has a `permanent` flag so callers don't re-retry. The flag is set in one
place, so call sites do not have to re-derive the categorization.

Automatic retry is safe only when repeating the request is safe. That means an
idempotent method (GET, PUT, DELETE) or a request with an idempotency key
the server dedupes on. Retrying a non-idempotent POST after a 5xx or a timeout
can create the resource twice. This happens because the first attempt may have committed
before the response was lost.

Scope the wrapper to safe methods, or require
the key. The wrapper also passes `res.text()` along for logging at the boundary. A handler
replying to an external caller maps it to a category and a safe message first. It does this
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
| `INTERNAL` | No. It signals a broken invariant, so a bare retry hides a bug |
| `INVALID_ARGUMENT`, `NOT_FOUND`, `PERMISSION_DENIED`, and the rest | No — caller error |

Here is a Go server-to-server client:

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

Every RPC client method wraps its call in the one function `retryGRPC`.
The retryability decision is in one place (`isRetryableGRPC`), which
reads the gRPC status code and applies the table above.

Per-call-site retry logic is where this design goes wrong. When each site has
its own retry-or-not check, each check gets something slightly wrong, such as
missing the deadline propagation or double-retrying on `ABORTED`. The helper
applies the ladder in one place and masks the transient cases. Permanent errors bubble up where the
caller can act.

The helper propagates the deadline in `ctx`. `sleepCtx`
returns early if it expires during backoff. The loop stops retrying once
the deadline passes. The loop also does not sleep past the deadline. To also skip an attempt that
can't finish in time, compare `ctx`'s remaining time against the next backoff
before the call. Deadline handling belongs in the helper, because
putting it there keeps it out of 50 call sites.

---

## Example 3 — Timeouts as performance design

The timeout is the complexity that people forget, as in this service that calls a downstream service:

```ts
async function getRecommendations(userId: string): Promise<Recommendation[]> {
  return await downstreamClient.getRecommendations(userId);
}
```

The call has no timeout. The downstream service is slow today, taking 30
seconds against a usual 50ms. This service's threads or event loop hang on
those calls, so the user's page load takes 30 seconds. The failure then
spreads, because this service now looks slow to *its* callers, which back
up their own callers in turn.

Timeout choice is a performance design decision. This code shows the cheap design-time
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
higher. The reason is that "wait forever" is worse than "give up after 5 seconds."

Some dependencies are non-critical, such as the recommendations panel on a page that
also loads the page content. For these, the right move is often to render the page
without the panel, fetch the panel in the background, and insert it when it
arrives. That design move removes the recommendation's slowness from the
user's critical path, so the timeout never applies.

Removing the panel from the critical path applies `examples.md` Example 1
("define the error out of existence") to latency. The most reliable way to handle a slow
dependency is to remove it from your critical path.

---

## Example 4 — Circuit breakers: when the complexity is worth its cost

A circuit breaker is a stateful wrapper around a downstream call that:

- Tracks recent failure rate.
- "Trips" (stops calling) when failures cross a threshold.
- Periodically tests the downstream to see if it's healthy again.
- "Closes" (resumes calling) when test calls succeed.

Libraries: `resilience4j` (Java), `gobreaker` (Go), `cockatiel` (TypeScript).

When is the complexity worth its cost?

**Earned**:
- The downstream's failure mode is "slow", so calls hang for the full
  timeout. A retry-and-timeout policy alone causes threads to pile up. The
  breaker prevents the pile-up by short-circuiting calls when the downstream
  is unhealthy.
- The downstream is called frequently, so the breaker has signal to act
  on.
- Backpressure has business value, because serving "I can't reach
  recommendations right now" immediately is better than holding the user's
  page for the timeout duration.

**Not earned**:
- The call is low-traffic, such as a daily cron job to a partner API. The breaker has
  no recent-failure signal, so its complexity gives no benefit.
- The retry policy already handles the failure mode adequately. Adding a
  breaker on top duplicates that handling.
- The downstream is "fail-fast", so a quick error from an unhealthy
  downstream doesn't pile up threads. A breaker then has nothing to prevent.

Adding a circuit breaker because "we should" is a mistake. It produces a
piece of stateful complexity that:

- Has bugs that only surface during incidents (the worst time to find
  them).
- Has tuning parameters (window size, threshold, half-open timing) that
  are hard to understand well enough to set correctly.
- Hides downstream failures from operators (the breaker has tripped, so
  calls don't appear in logs and the dashboard is misleading).

If you don't have *measured* evidence that a piling-up failure mode is
hurting users today, the circuit breaker is speculative complexity.
Don't ship it. When you get the evidence (an outage post-mortem says
"thread pool saturated on slow downstream"), add the breaker for that
specific dependency.

---

## Example 5 — Bulk vs row-by-row API: avoid many small round trips

This batch import endpoint has grown to create orders one at a time:

```ts
// POST /api/orders/import
// body: { orders: Order[] }
app.post('/api/orders/import', async (req, res) => {
  const created: Order[] = [];
  for (const order of req.body.orders) {
    const result = await ordersService.create(order);     // each order makes one DB round-trip
    created.push(result);
  }
  res.json(created);
});
```

500 orders means 500 sequential database round-trips. With a 2ms DB ping,
that's 1 second of network latency before any other work. The endpoint
takes 5 seconds, but the client times out at 3. When the user retries, the
retry contends with the partial import.

The design-time fix is a bulk path through the service down to a single
batched insert.

```ts
app.post('/api/orders/import', async (req, res) => {
  const result = await ordersService.createBulk(req.body.orders);
  res.json(result);
});

// this method is in OrdersService
async createBulk(orders: NewOrder[]): Promise<ImportOutcome[]> {
  // this runs one transaction in one round-trip. Each input maps to a typed outcome
  return await this.repo.insertMany(orders);
}
```

The import makes one round trip, so the cost is bounded. All the
complexity is in one place. `insertMany` in the repository defines the bulk semantics. It defines how
big a batch is too big (chunk the input above some threshold), and what a partial
failure looks like to the caller.

The return type states that contract. A
typed outcome per input (created, or rejected with a reason) lets the caller
act on a partial success. An all-or-nothing variant rejects the whole batch
and names the row that broke it. A flat array of successes can express
neither.

The row-by-row import is the same N+1 problem over a network as the mobile
bridge example. The fix is a bulk API at the boundary that crosses the network. Within
the application, the row-by-row code can stay (it's clearer), but at the
network boundary, send the rows as one batch.

---

## Example 6 — Shared mutable state behind one owner

Several handlers use an in-memory rate limiter. The tactical version
exposes the state and requires every caller to lock it:

```go
type RateLimiter struct {
    Mu     sync.Mutex
    Counts map[string]int
}

// this code repeats at every call site:
rl.Mu.Lock()
rl.Counts[userID]++
over := rl.Counts[userID] > limit
rl.Mu.Unlock()
```

The locking discipline is spread across the call sites. One handler skips the lock
and reads a torn value. Another holds the lock across a network call and
stalls everyone. A third takes this lock and a second one in the opposite
order and deadlocks. Every new call site is another chance to get one wrong.

Move the locking inside the type that holds the state:

```go
type RateLimiter struct {
    mu     sync.Mutex                 // unexported, so only methods touch it
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
structure, and one lock. With one lock, lock ordering cannot go wrong. Shared
mutable state is one more source of complexity. It costs least when one module
owns it and the rules for touching it are in one place.

---

## Cheat sheet — backend API complexity

| Symptom | Move |
|---|---|
| Every caller catches and retries HTTP errors | Categorize by status class; retry in the client wrapper |
| gRPC retry logic at every call site | One `retryGRPC` helper; retryability decision in one place |
| No timeouts on downstream calls | Always set a timeout to prevent a slow cascading failure |
| Circuit breaker because "we should" | Add only when measured thread-pile-up is hurting users |
| Loop of API calls (N+1 over the network) | Bulk endpoint; one round trip |
| Slow non-critical dependency on critical path | Move it off the critical path; render the page, then fill in the panel |
| `mutex` locked at every call site | Put the state and its lock in one type; expose methods and keep the lock hidden |
