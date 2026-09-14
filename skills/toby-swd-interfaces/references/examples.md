# Worked Examples

The code below is original and illustrates the procedure. The reasoning
transfers to any language.

---

## Example 1 — Backend: the comment-as-test catching a shallow interface

Task: a module to rate-limit API requests per client.

**Tactical interface (the one to reject):**

```python
class RateLimiter:
    def get_bucket(self, client_id) -> Bucket: ...
    def get_tokens(self, bucket) -> int: ...
    def refill(self, bucket, now) -> None: ...
    def consume(self, bucket, n) -> bool: ...
```

The full interface comment is long. The caller must fetch a bucket, refill
it with the current time, check tokens, and then consume. If those calls
happen out of order, the rate limiter breaks. The comment has to describe the
bucket mechanism before a caller can use it. The comment fails the test three
ways at once, because it is long, order-dependent, and leaks internals. The
design is temporal decomposition with a class around it.

**Redesigned interface (designed by knowledge: "whether this client may proceed
right now"):**

```python
class RateLimiter:
    def allow(self, client_id) -> bool:
        """Return True if a request from client_id may proceed now, and
        record it. False if the client is over its limit. Thread-safe.
        Refill and accounting are internal; callers need no notion of
        buckets, tokens, or time."""
```

The complete contract is two sentences and names none of its internals. Tokens,
refill cadence, and the clock moved inside. The interface shrank while the
module got deeper. The guardrail check asks whether anything the caller
needs is now hidden. If callers must show a retry-after hint, expose that one value
(`allow` returns `RetryAfter | None`) and keep the bucket internal.

---

## Example 2 — Frontend: overexposure and leakage in a component

Task: a `UserCard` used in a list, a profile header, and a search result.

**Tactical props (reject):**

```tsx
<UserCard
  user={user} variant="list" showEmail={true} showAvatar={true}
  avatarSize={40} onClick={fn} isSelected={false} truncateNameAt={20}
  theme={theme} dense compactOnMobile />
```

The interface comment for this is a paragraph, and a caller rendering the common
case still has to make eight decisions. Those eight decisions are overexposure,
because rare knobs get in the way of the common use. `theme` threaded through here only to reach a child
is information leakage, because `UserCard` does not use it.

**Design it twice.** Option A keeps one component and moves the knobs to
sensible defaults. Option B uses a small core plus thin presets. Option B wins because the
three real call sites are three named intents:

```tsx
// Each renders the common case with zero required decisions beyond `user`.
<UserListItem user={user} onSelect={fn} />
<UserProfileHeader user={user} />
<UserSearchResult user={user} query={q} />
// All compose one deep core that owns layout/truncation/theming internally.
```

Callers make one decision (which intent), down from eight. Theme is read from context
inside the core, so it stops being leaked through props. The core is deep, and the
presets are thin wrappers that each encode one distinct intent.

---

## Example 3 — The design-it-twice comparison, written out

Task: an interface for a client to upload a file to storage.

| Design | Caller's common-case burden | Generality | Hides | Verdict |
|---|---|---|---|---|
| A: `open()`, `writeChunk()`, `close()` | Manage handle, loop chunks, order calls, handle partial failure | Low | Little — caller drives the protocol | Shallow, temporal |
| B: `upload(bytes, key)` | One call | Medium | Chunking, retries, multipart threshold | Deep, but assumes all-in-memory |
| C: `upload(source, key)` where source is bytes or a stream | One call | High | Same as B, plus large-file streaming | Deepest; covers current and near needs |

C is a different decomposition, and B's flaw (high memory use on large
files) drove it. It is the kind
of synthesis the design-it-twice step is supposed to produce. The interface
comment for C is short and mentions no internals, so it passes the test.
Guardrail: if a caller must know whether the upload was durably committed
before `upload` returns, that need is real. `upload` returns once the data is
durably stored, and the comment states that guarantee.
