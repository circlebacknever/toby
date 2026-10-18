# Worked Examples

This file shows four module boundary fixes: merging steps that share a format, computing parameters internally, replacing prop drilling, and merging tiny components.

---

## 1. Merging steps that share a format

A team splits HTTP handling into `RequestReader` (which reads socket bytes into a string) and `RequestParser` (which parses the string into a request object), describing the design as "first read, then parse".

Because the `Content-Length` header determines where the body ends, `RequestReader` must also parse headers. Both classes depend on the HTTP wire format, and callers must invoke both in sequence.

Merge both into one `Request` module behind `Request.receive(socket)`. The wire format stays in one module, the intermediate string disappears, and callers make one call.

---

## 2. Pulling complexity down

A retrying transport needs a retry interval, and the first draft exposes `retry_interval_ms` as a required parameter for operators to set.

Ask whether the caller can pick a better value than the transport can. Because the transport already measures round-trip latency while the caller would guess, compute the backoff interval inside the transport from observed latency. Expose an optional override parameter with the computed default only when a test or environment requires it.

---

## 3. Pass-through variables

`AvatarMenu`, four levels below `App`, needs `currentUser`. Passing `currentUser` through `App → Layout → Header → Toolbar → AvatarMenu` forces three intermediate components to declare a prop they don't read.

Provide a small, stable `CurrentUserContext` near `App` and read it in `AvatarMenu`, removing the prop from the intermediate components. Likewise, delete a `<UserMenuWrapper>` component that only forwards props to `<UserMenu>`.

---

## 4. Shallow components

A team splits a list row into `<RowContainer>`, `<RowInner>`, `<RowText>`, `<RowMeta>`, and `<RowChrome>`. Each component is five lines, has one caller, and shares state with the others.

None of the five boundaries hides a separate design decision. Merge them into one `<Row>` component with a small prop interface. Extract a helper only for a general-purpose rule that other components also call, such as locale currency formatting.
