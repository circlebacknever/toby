# Worked Examples: The Same Task, Tactical vs Strategic

Each example shows the tactical version (smallest change that works), why it
quietly hurts, and the strategic version (the structure the code would have had
if designed with the change in mind). The code is illustrative; the reasoning
transfers.

---

## Example 1 — A new requirement that "just needs a special case"

A function renders user display names. New requirement: deleted users should
show as "[deleted]".

**Tactical**

```python
def display_name(user):
    if user.deleted:                 # smallest change that works
        return "[deleted]"
    return f"{user.first} {user.last}"
```

Why it hurts: every caller that formats a name now silently depends on this
branch existing. The next special case (banned users, system accounts,
unverified users) adds another branch here or, worse, another branched copy
elsewhere. The "deleted" concept has leaked into name formatting.

**Strategic**

```python
def display_name(user):
    return user.display_label()      # the question "what do we call this user?"
                                     # belongs to the user, not the formatter
```

```python
class User:
    def display_label(self):
        if self.deleted:
            return "[deleted]"
        return f"{self.first} {self.last}"
```

The design pass cost a minute and a near-future variant ("there will be more
user states") drove it. Now new states are one place, callers are untouched,
and the formatter no longer knows what "deleted" means. The interface got
simpler while the work moved to where it belongs.

---

## Example 2 — A new module's design pass

Task: add retry logic to an HTTP client call.

**Tactical:** wrap the call site in a `for` loop with a `sleep`. It works. Three
weeks later a second call site needs retries and the loop is copy-pasted with a
slightly different backoff, and now there are two retry policies that drift.

**Strategic — sketch two approaches first:**

- *A: retry decorator on each call site.* Interface: callers add `@retry(...)`.
  Hides the loop but every call site still chooses and can mis-choose policy.
- *B: a retrying transport the client is constructed with.* Interface: callers
  call the client normally; retry is a property of the client, configured once.

B has the simpler caller-side interface and absorbs the "there will be more call
sites" variant for free, so pick B even though its insides (wrapping the
transport, classifying retryable errors) are more work than a loop. That extra
work is the investment; it is paid once and every current and future call site
collects the return.

---

## Example 3 — Modifying existing code under a real deadline

Existing `PaymentProcessor` hardcodes one gateway. Task, due tomorrow: support a
second gateway for one specific customer.

Apply the test: *what would this look like if designed with two gateways in
mind?* Answer: a `Gateway` interface with two implementations and selection by
config. That is the right design and it is also several hours you do not have
before the deadline — this is a legitimate quick-fix situation (hard external
deadline, accepted cost).

So take the tactical path deliberately and label it:

```python
def process(self, payment):
    # TACTICAL: hardcoded gateway switch for ACME only, shipped under the
    # 4/12 deadline. Clean design = a Gateway interface + config selection;
    # do this before adding a third gateway or it compounds. Tracked: JIRA-1234.
    if payment.customer_id == ACME:
        return self._charge_via_stripe(payment)
    return self._charge_via_legacy(payment)
```

The difference from pure tactical programming is not that you avoided the
shortcut — you took it. The difference is that the shortcut is now visible,
bounded, and has a stated exit, so it is a labeled loan instead of a hidden one.
The strategic move under a deadline is a truthful IOU, not a sound design you
didn't have time for.

---

## How to calibrate the investment

- The target is roughly 10–20% more effort than the tactical path, spent
  continuously, not a separate "cleanup phase" and not a redesign.
- Proactive spend: trying a second design, choosing names well, writing the
  interface comment first so the abstraction is stable before the code.
- Reactive spend: fixing a design flaw you hit instead of routing around it,
  plus one opportunistic improvement to code you were already in.
- If a "strategic" move would touch large parts of the codebase or blow the
  effort well past that band, it is no longer strategic — it is the big-bang
  redesign anti-pattern. Scope down to what you can do well inside this change.
