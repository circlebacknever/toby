# Worked Examples

This file shows how the comment test exposes shallow interfaces in a rate limiter, a UI component, and a file uploader.

---

## 1. Shallow rate limiter

Task: rate-limit API requests per client.

**First quick interface (reject this one):**

```python
class RateLimiter:
    def get_bucket(self, client_id) -> Bucket: ...
    def get_tokens(self, bucket) -> int: ...
    def refill(self, bucket, now) -> None: ...
    def consume(self, bucket, n) -> bool: ...
```

The comment fails the test because callers must fetch a bucket, refill it with the current time, check tokens, and consume in that exact order. That leaks the token-bucket mechanism and call order into every caller.

**Redesigned interface around the single question callers ask:**

```python
class RateLimiter:
    def allow(self, client_id) -> bool:
        """Return True if a request from client_id may proceed now, and
        record it. Return False if the client is over its limit. The method is thread-safe.
        Refill and accounting stay inside the class, so callers don't manage
        buckets, tokens, or timestamps."""
```

The complete contract is four sentences and mentions none of its internals. If callers must return a `Retry-After` header, expose that one value (`allow` returns `RetryAfter | None`) while keeping buckets and refill timestamps private.

---

## 2. Overexposed component

Task: render a user summary in a list, a profile header, and a search result.

**First quick props (reject these):**

```tsx
<UserCard
  user={user} variant="list" showEmail={true} showAvatar={true}
  avatarSize={40} onClick={fn} isSelected={false} truncateNameAt={20}
  theme={theme} dense compactOnMobile />
```

Callers rendering the common case must choose eight props, and the component only forwards `theme` to a child. Replace the single component with one wrapper per use case over a shared internal component, and read `theme` from context:

```tsx
// Each renders the common case with zero required decisions beyond `user`.
<UserListItem user={user} onSelect={fn} />
<UserProfileHeader user={user} />
<UserSearchResult user={user} query={q} />
```

---

## 3. Design comparison

Task: upload a file to object storage.

| Design | Caller's common-case burden | Generality | Hides | Verdict |
|---|---|---|---|---|
| A: `open()`, `writeChunk()`, `close()` | Manage handle, loop chunks, order calls, handle partial failure | Low | Little, because the caller runs the protocol | Shallow and order-dependent |
| B: `upload(bytes, key)` | One call | Medium | Chunking, retries, multipart threshold | Deep, but loads whole file in memory |
| C: `upload(source, key)` where source is bytes or a stream | One call | High | Same as B, plus large-file streaming | Deepest, and covers both small and large files |

Design C passes the comment test and states in its comment that `upload` returns only after object storage durably saves the file.
