# Worked Examples

Original code, illustrating the procedure. The reasoning transfers; the
languages do not matter.

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

Write the interface comment truthfully and it gets long: the caller must fetch a
bucket, refill it with the current time, check tokens, then consume — and must
do these in that order or it breaks. The comment has to describe the bucket
mechanism to be usable. That is the test failing on three counts at once: long,
order-dependent, leaks internals. This is temporal decomposition wearing a
class.

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
module got deeper. The guardrail check: is anything the caller truly needs
now hidden? If callers must show a retry-after hint, expose that one value
(`allow` returns `RetryAfter | None`) rather than re-exposing the bucket.

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
case still has to make eight decisions. That is overexposure: rare knobs are in
the way of the common use. `theme` threaded through here only to reach a child
is information leakage — `UserCard` does not use it.

**Design it twice.** Option A: keep one component, push the knobs to sensible
defaults. Option B: a small core plus thin presets. Option B wins because the
three real call sites are three named intents:

```tsx
// Each renders the common case with zero required decisions beyond `user`.
<UserListItem user={user} onSelect={fn} />
<UserProfileHeader user={user} />
<UserSearchResult user={user} query={q} />
// All compose one deep core that owns layout/truncation/theming internally.
```

Callers make one decision (which intent), not eight. Theme is read from context
inside the core, so it stops being leaked through props. The core is deep; the
presets are honest thin wrappers, not pass-through components, because each
encodes a real distinct intent.

---

## Example 3 — The design-it-twice comparison, written out

Task: an interface for a client to upload a file to storage.

| Design | Caller's common-case burden | Generality | Hides | Verdict |
|---|---|---|---|---|
| A: `open()`, `writeChunk()`, `close()` | Manage handle, loop chunks, order calls, handle partial failure | Low | Little — caller drives the protocol | Shallow, temporal |
| B: `upload(bytes, key)` | One call | Medium | Chunking, retries, multipart threshold | Deep, but assumes all-in-memory |
| C: `upload(source, key)` where source is bytes or a stream | One call | High | Same as B, plus large-file streaming | Deepest; covers current and near needs |

C is not the first idea (A is) and not a tweak of B — it is a different
decomposition driven by B's flaw (memory blowup on large files). It is the kind
of synthesis the design-it-twice step is supposed to produce. The interface
comment for C is short and mentions no internals, so it passes the test.
Guardrail: if a caller must know whether the upload was durably committed before
returning, that is a real need — `upload` returns once durably stored, and
that guarantee goes in the comment rather than being hidden.
