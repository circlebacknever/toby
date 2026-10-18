# Worked Examples: The Shortcut and the Sound Design

Each example shows the quick shortcut, why it causes problems later, and the design you would build with the change in mind.

---

## 1. New module design pass

Task: add retry logic to the HTTP client's GET calls in `billing/sync.py` and `orders/sync.py`. Both calls fail on transient 503s today.

**Shortcut:** wrap each call site in a `for` loop with a `sleep`. You copy the loop into both files with a slightly different backoff, so the repo now has two retry policies that drift apart over time.

**Sound design, with two approaches sketched first:**

- *A: retry decorator on each call site.* Callers add `@retry(...)`. The decorator hides the loop, but every call site still chooses its own retry policy and can pick the wrong one.
- *B: a retrying transport you pass to the client constructor.* Callers call the client normally, and you configure retries once on the client.

B has the simpler caller-side interface. Pick B even though wrapping the transport takes more work than a loop. You write the transport once, and every call site gets retries automatically.

---

## 2. Deadline shortcut

`PaymentProcessor` hardcodes one gateway, and a deadline tomorrow requires supporting a second gateway for one customer.

With two gateways in mind, the sound design is a `Gateway` interface with two implementations selected by config. When the deadline is hard and external and the user accepts the cleanup cost, take the shortcut and label it in the code:

```python
def process(self, payment):
    # SHORTCUT: hardcodes ACME to Stripe for the 4/12 deadline.
    # Replace with a Gateway interface selected by config before adding a third gateway (JIRA-1234).
    if payment.customer_id == ACME:
        return self._charge_via_stripe(payment)
    return self._charge_via_legacy(payment)
```
