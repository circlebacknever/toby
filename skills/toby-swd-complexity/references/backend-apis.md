# Worked Examples — Backend APIs (Java, Go, TypeScript)

In distributed systems, things fail. The complexity
question is where in the system each kind of failure gets absorbed, and at
what cost. The error ladder applies directly. Performance design at the
network layer is mostly about keeping the failure modes bounded.

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
The error ladder isn't applied, so everything propagates uniformly.

The HTTP status codes already carry a category signal, so use it:

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

What this absorbs (rung 2, mask at lowest level): transient 5xx, 408, 429,
network blips, and the timeout abort. What it surfaces: 4xx (caller did
something wrong) and sustained 5xx (real outage). The thrown `HttpError`
carries a `permanent` flag so callers don't re-retry. The flag is set in one
place, which spares every call site from re-deriving the categorization.

Automatic retry is safe only when repeating the request is safe — an
idempotent method (GET, PUT, DELETE) or a request carrying an idempotency key
the server dedupes on. Retrying a non-idempotent POST after a 5xx or a timeout
can create the resource twice, because the first attempt may have committed
before the response was lost. Scope the wrapper to safe methods, or require
the key. And `res.text()` rides along for logging at the boundary. A handler
replying to an external caller maps it to a category and a safe message first,
since a downstream body can carry stack traces or query text (rung 3).

Callers handle the typed errors at one place — usually a response
interceptor that catches `permanent: false` (sustained outage → user-facing
"service unavailable") and lets `permanent: true` bubble up where the
caller can decide if it's a 404, a validation failure, an auth problem.

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
The retryability decision lives in one place (`isRetryableGRPC`), which
reads the gRPC status code and applies the table above.

Per-call-site retry logic is where this goes wrong. Each site writes its
own retry-or-not check, gets it slightly wrong, misses the deadline
propagation, double-retries on `ABORTED`. The ladder collapses into one
helper, masking the transient cases. Permanent errors bubble up where the
caller can act.

Deadline propagation matters. `ctx` carries a deadline, and `sleepCtx`
returns early if it expires during backoff. The loop stops retrying once
the deadline is gone, and it won't sleep past it. To also skip an attempt that
can't finish in time, compare `ctx`'s remaining time against the next backoff
before the call. This is the kind of complexity that lives in the
helper, which is what keeps it out of 50 call sites.

---

## Example 3 — Timeouts as performance design

The forgotten complexity. A service calls a downstream service:

```ts
async function getRecommendations(userId: string): Promise<Recommendation[]> {
  return await downstreamClient.getRecommendations(userId);
}
```

No timeout. The downstream service is slow today: 30 seconds, against a
usual 50ms. This service's threads/event-loop hang on
those calls. The user's page-load takes 30 seconds. The failure cascades.
This service now appears slow to *its* callers, which back up, which
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
without it; fetch in the background; insert when it arrives." This is a
design move. It defines the recommendation's slowness out of the user's
critical path entirely, so the timeout never even comes into play.

This is the same shape as `examples.md` Example 1 ("define the error out
of existence") applied to latency. The most reliable way to handle a slow
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
- Low-traffic call (a daily cron job to a partner API). The breaker has
  no recent-failure signal, so you're paying complexity for nothing.
- The retry policy already handles the failure mode adequately. Adding a
  breaker on top is duplicated machinery.
- The downstream is "fail-fast", so a quick error from an unhealthy
  downstream doesn't pile up threads. A breaker prevents nothing.

The mistake — adding a circuit breaker because "we should" — produces a
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
contention because of the partial import.

The design-time fix: a bulk path through the service down to a single
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

One round trip. The cost is bounded. The complexity concentrates in one
place. `insertMany` in the repository owns the bulk semantics — how big a
batch is too big (chunk the input above some threshold), and what a partial
failure looks like to the caller. The return type decides that contract. A
typed outcome per input (created, or rejected with a reason) lets the caller
act on a partial success. An all-or-nothing variant rejects the whole batch
and names the row that broke it. A flat array of successes can express
neither.

This is the same shape as the mobile bridge example — N+1 over a network.
The cure is bulk APIs at the boundary that crosses the network. Within
the application, the row-by-row code can stay (it's clearer), but at the
network boundary, batch.

---

## Example 6 — Shared mutable state behind one owner

An in-memory rate limiter several handlers consult. The tactical version
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

The locking discipline lives at the call sites. One handler forgets to lock
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
critical section is one short block — no network call inside it, one
structure, one lock — so there's no ordering left to get wrong. Shared
mutable state is complexity like any other. It costs least when one module
owns it and the rules for touching it live in one place.

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
