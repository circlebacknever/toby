# Worked Examples: The Same Task, Tactical vs Strategic

Each example shows the tactical version, the smallest change that works, and
why it causes problems later. The strategic version follows, with the structure
the code would have had if designed with the change in mind. The code is
illustrative, and the reasoning applies to other code.

---

## Example 1 — A new requirement that "just needs a special case"

A function renders user display names. A new requirement says deleted users
should show as "[deleted]".

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
    return user.display_label()      # the user owns the answer to
                                     # "what do we call this user?"
```

```python
class User:
    def display_label(self):
        if self.deleted:
            return "[deleted]"
        return f"{self.first} {self.last}"
```

The design pass cost a minute and a near-future variant ("there will be more
user states") drove it. Now new states go in one place, callers are untouched,
and the formatter no longer checks for "deleted". The interface got
simpler while the work moved to where it belongs.

---

## Example 2 — A new module's design pass

Task: add retry logic to an HTTP client call.

**Tactical:** wrap the call site in a `for` loop with a `sleep`. It works. Three
weeks later a second call site needs retries, and the loop is copy-pasted with a
slightly different backoff. Now there are two retry policies that drift.

**Strategic — sketch two approaches first:**

- *A: retry decorator on each call site.* Interface: callers add `@retry(...)`.
  The decorator hides the loop, but every call site still chooses its policy
  and can choose the wrong one.
- *B: a retrying transport the client is constructed with.* Interface: callers
  call the client normally, and retry is a property of the client, configured
  once.

B has the simpler caller-side interface, and it handles the "there will be more
call sites" variant at no extra cost. Pick B even though its insides (wrapping
the transport, classifying retryable errors) are more work than a loop. That
extra work is the investment, and it is paid once. Every current and future
call site benefits from it.

---

## Example 3 — Modifying existing code under a real deadline

The existing `PaymentProcessor` hardcodes one gateway. The task, due tomorrow,
is to support a second gateway for one customer.

Apply the test: *what would this look like if designed with two gateways in
mind?* That design is a `Gateway` interface with two implementations and
selection by config. It is the right design, and it is also several hours you
do not have before the deadline. The situation qualifies for a quick fix,
because the deadline is hard and external and the cost is accepted.

So take the tactical path deliberately and label it:

```python
def process(self, payment):
    # TACTICAL: hardcoded gateway switch for ACME only, shipped under the
    # 4/12 deadline. Sound design = a Gateway interface + config selection;
    # do this before adding a third gateway or it compounds. Tracked: JIRA-1234.
    if payment.customer_id == ACME:
        return self._charge_via_stripe(payment)
    return self._charge_via_legacy(payment)
```

You took the shortcut. This fix differs from pure tactical programming because
the shortcut is now visible and bounded, and it has a stated exit. The next
person can see the debt and pay it down. Under a deadline, label the shortcut
and state the exit.

---

## Example 4 — A dispatch that will grow

A function routes a notification to a channel. Today the channels are email and SMS.

**Tactical**

```python
def send(notification, user):
    if notification.channel == "email":
        return email_client.send(user.email, notification.body)
    if notification.channel == "sms":
        return sms_client.send(user.phone, notification.body)
```

It works. Then push is added, then Slack, then a webhook. Each one edits `send`,
and three call sites now have their own copy of the same `if` chain to decide
whether a channel is available for a user.

**Strategic**

The word "today" in the first sentence states the near-future variant, and more
channels are certain, so build the dispatch now:

```python
CHANNELS: dict[str, Channel] = {
    "email": EmailChannel(),
    "sms": SmsChannel(),
}

def send(notification, user):
    channel = CHANNELS[notification.channel]
    return channel.deliver(notification, user)
```

Each `Channel` owns its client, its address lookup, and its own answer to "is
this available for this user." Adding a channel takes one class and one entry. The
call sites lose their copied checks, because `deliver` handles an unavailable
channel internally.

This dispatch is rung 4 of the ladder in `toby-swd-modules`, which is an
interface with one implementation per case. The cost over the tactical version is a dict and an
interface, paid once at design time.

---

## How to calibrate the investment

- The target is roughly 10–20% more effort than the tactical path, spent
  continuously through the change. If you save it for a separate "cleanup
  phase", it never happens. If you spend it all at once on a redesign, you have
  gone outside that range.
- Proactive spending covers trying a second design, choosing names well, and
  writing the interface comment first so the abstraction is stable before the
  code.
- Reactive spending covers fixing a design flaw as soon as you find it, while
  you have the context, plus one opportunistic improvement to code you were
  already in.
- A "strategic" move that touches large parts of the codebase, or goes well past
  that effort range, is the big-bang redesign anti-pattern.
  Scope down to what you can do well inside this change.
