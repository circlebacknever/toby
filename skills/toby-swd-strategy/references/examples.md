# Worked Examples: The Shortcut and the Sound Design

Each example shows the shortcut, the smallest change that works, and why it
causes problems later. The sound design follows, with the structure the code
would have had if designed with the change in mind.

---

## Example 1 — A new module's design pass

Task: add retry logic to the HTTP client's GET calls in `billing/sync.py` and
`orders/sync.py`. Both calls fail on transient 503s today.

**Shortcut:** wrap each call site in a `for` loop with a `sleep`, which works.
The loop is copied into both files with a slightly different backoff. Now there
are two retry policies, and their settings become more different over time.

**Sound design, with two approaches sketched first:**

- *A: retry decorator on each call site.* Interface: callers add `@retry(...)`.
  The decorator hides the loop, but every call site still chooses its policy
  and can choose the wrong one.
- *B: a retrying transport the client is constructed with.* Interface: callers
  call the client normally. Retry is a property of the client, configured
  once.

B has the simpler caller-side interface. Pick B even though its implementation
(wrapping the transport, classifying retryable errors) is more work than a loop. The
transport is written once, and every call site gets retries from it.

---

## Example 2 — Modifying existing code under a real deadline

The existing `PaymentProcessor` hardcodes one gateway. The task, due tomorrow,
is to support a second gateway for one customer.

Apply the test: *what would this look like if designed with two gateways in
mind?* That design is a `Gateway` interface with two implementations and
selection by config. It is the right design, but it takes several hours you
do not have before the deadline. The situation qualifies for the shortcut,
because the deadline is hard and external and the cost is accepted.

So take the shortcut deliberately and label it:

```python
def process(self, payment):
    # SHORTCUT: this gateway switch is hardcoded for ACME only and shipped under the
    # 4/12 deadline. The sound design is a Gateway interface with config selection.
    # Do this before adding a third gateway, or the problem grows. Tracked: JIRA-1234.
    if payment.customer_id == ACME:
        return self._charge_via_stripe(payment)
    return self._charge_via_legacy(payment)
```

Under a deadline, label the shortcut and state when and how to replace it.
