# Worked Examples

The code and structures below are original. The reasoning in them also applies to other code.

---

## Example 1 — Backend: temporal decomposition, fixed by merging

A team builds request handling as two classes. `RequestReader` reads bytes off
the socket into a string. `RequestParser` parses the string into a
structured request. The team describes the design as "first read, then parse",
which is a sign of temporal decomposition.

The defect is that the reader cannot know where the request ends without
parsing the headers, because the length header determines body size. So both
classes know the request format. That knowledge is a single design decision
written in two modules, which is leakage. The parsing code is also duplicated. Callers also have to
invoke two objects in a fixed order.

The decompose-by-knowledge, information-leakage, and split/merge checks give the fix.
The knowledge is "the request wire format," which should be in one module. Merge into one `Request` module that reads and
parses behind a single `Request.receive(socket)`. The format knowledge is now in
one place, the inter-module string-passing interface disappears, and callers
make one call. The merged module is deeper than either original.

---

## Example 2 — Backend: pull complexity downward

A retrying transport needs a retry interval. The tactical move is to export
`retry_interval_ms` as a configuration parameter and let operators set it.

Apply the pull-complexity-down check by asking whether the caller can pick a
better value than the module can. For a retry interval, the caller almost never
can, because the module measures the round-trip times but the operator is
guessing. So the module should compute it by measuring observed response
latency and using a multiple of it, adapting as conditions change. The parameter
is removed from the interface. If a hard override is needed for some
environment, keep it as an optional argument with that computed value as the
default. Callers in the common case then pass nothing.

The guardrail check passes. This complexity is related to the transport's own
job. Pulling it down is correct here because it simplifies every caller.

---

## Example 3 — Frontend: prop drilling is a pass-through variable

`currentUser` is needed by `AvatarMenu`, four levels deep. Today it is passed
`App → Layout → Header → Toolbar → AvatarMenu`. Every intermediate
component's props list includes `currentUser` though only the leaf uses it.

`currentUser` is a pass-through variable (the different-layer check). The intermediate
components are forced to know about a value they have no use for. Adding the
next such value means editing the whole chain again. Fix it with a shared object
scoped to the endpoints, such as a `CurrentUserContext` provided near `App` and
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

The subdivision cost (the split/merge check / classitis) is five interfaces to
learn, five files to switch between, and dependencies hidden across them. No
boundary hides any information, because none contains a distinct piece of knowledge.
All the relatedness signals favor merging, because the components share state,
are always used together, and none can be understood alone. Merge them into one `<Row>` component. It is longer, but it
is one coherent deep abstraction with a simple prop interface. Under the depth
check, that one component is better than five shallow ones.

A counter-case shows when a split is correct. If `<Row>` also contained
the logic for formatting currency across locales, that *is* a distinct body of
knowledge with reuse elsewhere. Extract it as a general-purpose helper, and split
on a knowledge boundary. A high line count alone does not justify a split.

---

## The split-or-merge decision, in one place

| Question | Toward merge | Toward split |
|---|---|---|
| Do they share a design decision / knowledge? | Yes | No |
| Is the combined interface simpler for callers? | Yes | No (separate is simpler) |
| Does it remove duplicated nontrivial code? | Yes | n/a |
| Are the pieces independently understandable? | They are not — merge | They are — split is safe |
| Must callers use both halves and pass state between them? | Then do not split | — |
| Does each resulting interface beat the original's? | — | Required for the split to be worth it |
