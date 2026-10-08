# Worked Examples

A deep module hides a lot of work behind a small interface. A shallow module has an interface about as complex as the work behind it.

---

## Example 1 — Backend: the comment test finds a shallow interface

Task: a module to rate-limit API requests per client.

**First quick interface (reject this one):**

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
bucket mechanism before a caller can use it. The comment fails the test
because it is long, order-dependent, and leaks internals. The
design splits the work by the order the steps run and wraps those steps in a class.

**Redesigned interface, built around the one question the module answers, which is
whether this client may send a request right now:**

```python
class RateLimiter:
    def allow(self, client_id) -> bool:
        """Return True if a request from client_id may proceed now, and
        record it. Return False if the client is over its limit. The method is thread-safe.
        Refill and accounting are internal, so callers need no notion of
        buckets, tokens, or time."""
```

The complete contract is four sentences and mentions none of its internals. The token count,
the refill rate, and the clock are now internal to the class. The interface got smaller while the
class took on more of the work. Step 5 in `SKILL.md` asks whether the redesign hid
anything the caller needs. If callers must show a retry-after hint, expose that one value
(`allow` returns `RetryAfter | None`) and keep the bucket internal.

---

## Example 2 — Frontend: overexposure and leakage in a component

Task: a `UserCard` used in a list, a profile header, and a search result.

**First quick props (reject these):**

```tsx
<UserCard
  user={user} variant="list" showEmail={true} showAvatar={true}
  avatarSize={40} onClick={fn} isSelected={false} truncateNameAt={20}
  theme={theme} dense compactOnMobile />
```

The interface comment for this is a paragraph. A caller rendering the common
case still has to make eight decisions. Making callers choose eight options is overexposure,
because rarely used options make the common call harder. `theme` passed through here only for a child component
is information leakage, because `UserCard` does not use it.

**Design it twice.** Option A keeps one component and gives the options
sensible defaults. Option B uses one shared inner component plus a few small wrapper components, one for each use.
Option B is the better choice because the three real call sites each use the card for a different purpose:

```tsx
// Each renders the common case with zero required decisions beyond `user`.
<UserListItem user={user} onSelect={fn} />
<UserProfileHeader user={user} />
<UserSearchResult user={user} query={q} />
// All compose one deep core that handles layout/truncation/theming internally.
```

Callers now make one decision, which component to use, down from eight. Theme is read from context
inside the shared inner component, so theme stops being leaked through props. The shared inner
component does most of the work. Each wrapper is small and covers one use.

---

## Example 3 — The design-it-twice comparison, written out

Task: an interface for a client to upload a file to storage.

| Design | Caller's common-case burden | Generality | Hides | Verdict |
|---|---|---|---|---|
| A: `open()`, `writeChunk()`, `close()` | Manage handle, loop chunks, order calls, handle partial failure | Low | Little, because the caller runs the protocol | Hides little and makes callers run the steps in order |
| B: `upload(bytes, key)` | One call | Medium | Chunking, retries, multipart threshold | Deep, but assumes all-in-memory |
| C: `upload(source, key)` where source is bytes or a stream | One call | High | Same as B, plus large-file streaming | Deepest, and covers today's needs and the expected next ones |

Design C splits the work differently from B. C exists because B loads the whole
file into memory, which uses a lot of memory on large files. The interface
comment for C is short and mentions no internals, so it passes the test.

A caller may need to know that the upload is durable when `upload`
returns, so `upload` returns only after the data is durably stored. The comment states that guarantee.
