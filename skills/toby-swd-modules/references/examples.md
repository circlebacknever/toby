# Worked Examples

A deep module hides a lot of work behind a small interface. A shallow module has an interface about as complex as the work behind it.

---

## Example 1 — Backend: temporal decomposition, fixed by merging

A team builds request handling as two classes. `RequestReader` reads bytes off
the socket into a string. `RequestParser` parses the string into a
structured request. The team describes the design as "first read, then parse",
which is a sign of temporal decomposition.

The defect is that `RequestReader` cannot know where the request ends without
parsing the headers, because the length header determines body size. So both
classes know the request format. That knowledge is a single design decision
written in two modules, which is leakage. The parsing code is also duplicated. Callers also have to
invoke two objects in a fixed order.

Checks 1, 2, and 7 give the fix.
The knowledge is "the request wire format," which should be in one module. Merge into one `Request` module that reads and
parses behind a single `Request.receive(socket)`. The format knowledge is now in
one place, the string that one class passed to the other is gone, and callers
make one call. The merged module is deeper than either original.

---

## Example 2 — Backend: pull complexity downward

A retrying transport needs a retry interval. The quick fix is to expose
`retry_interval_ms` as a configuration parameter and let operators set it.

Apply check 3 by asking whether the caller can pick a
better value than the module can. For a retry interval, the caller almost never
can, because the module measures the round-trip times but the operator is
guessing. So the module should compute the interval itself. The module measures response
latency, waits a multiple of that latency, and updates the interval as latency changes. The parameter
is removed from the interface.

If a hard override is needed for some
environment, keep it as an optional argument with that computed value as the
default. Callers in the common case then pass nothing.

This change follows check 3 in `SKILL.md`. The interval calculation is part of the transport's own
job, and moving the calculation inside removes a setting from every caller.

---

## Example 3 — Frontend: prop drilling is a pass-through variable

`currentUser` is needed by `AvatarMenu`, four levels deep. Today it is passed
`App → Layout → Header → Toolbar → AvatarMenu`. Every intermediate
component's props list includes `currentUser` though only the leaf uses it.

`currentUser` is a pass-through variable (check 4). The intermediate
components are forced to know about a value they have no use for. Adding the
next such value means editing the whole chain again. Fix it with a value that only the
top and bottom components touch, such as a `CurrentUserContext` provided near `App` and
read in `AvatarMenu`. The prop is removed from the intermediates. Keep the context small
and its value stable, because a context that collects unrelated values has the
downsides of global state.

In a related frontend case, a `<UserMenuWrapper>` that renders `<UserMenu>` and
only forwards its props is a pass-through method. Delete it and let callers use
`UserMenu` directly, or give the wrapper a real responsibility.

---

## Example 4 — Frontend: classitis from over-componentization

A team splits a list row into `<RowContainer>`, `<RowInner>`, `<RowText>`,
`<RowMeta>`, and `<RowChrome>`. Each of the five components is a handful of
lines. Only the component above each one uses it. None makes sense on its own.

Splitting the row this way costs five interfaces to
learn, five files to switch between, and dependencies hidden across them. Check 7 and the
classitis red flag cover this case. No
boundary hides any information, because none contains a distinct piece of knowledge.

Every sign from check 1 that code belongs in one module points to a merge. The components share state,
are always used together, and none can be understood alone. Merge them into one `<Row>` component. It is longer, but it
is one coherent deep abstraction with a simple prop interface. Under check 8,
that one component is better than five shallow ones.

A counter-case shows when a split is correct. If `<Row>` also contained
the logic for formatting currency across locales, that *is* a separate piece of
knowledge that other code also needs. Extract it as a general-purpose helper, so that each
piece hides one decision. A high line count alone does not justify a split.
