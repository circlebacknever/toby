# Worked Examples

The code and structures below are original, and the reasoning is the part that transfers to other code.

---

## Example 1 — Backend: temporal decomposition, fixed by merging

A team builds request handling as two classes. `RequestReader` reads bytes off
the socket into a string, and `RequestParser` parses the string into a
structured request. The team describes the design as "first read, then parse",
which signals temporal decomposition.

The defect is that the reader cannot know where the request ends without
parsing the headers, because the length header determines body size. So both
classes know the request format. That knowledge is a single design decision
written in two modules, which is leakage, and parsing code ends up duplicated. Callers also have to
invoke two objects in a fixed order.

The decompose-by-knowledge, information-leakage, and split/merge checks give the fix.
The knowledge is "the request wire format," and it should be in one module. Merge into one `Request` module that reads and
parses behind a single `Request.receive(socket)`. The format knowledge is now in
one place, the inter-module string-passing interface disappears, and callers
make one call. The merged module is deeper than either original.

---

## Example 2 — Backend: pull complexity downward

A retrying transport needs a retry interval. The tactical move is to export
`retry_interval_ms` as a configuration parameter and let operators set it.

Apply the pull-complexity-down check by asking whether the caller can pick a
better value than the module can. For a retry interval, the caller almost never
can, because the module sees the actual round-trip times and the operator is
guessing. So compute it. Measure observed response
latency and use a multiple of it, adapting as conditions change. The parameter
leaves the interface entirely. If a hard override is needed for some
environment, keep it as an optional argument with that computed value as the
default. The common case then specifies nothing.

The guardrail check passes. This complexity is related to the transport's own
job and it simplifies every caller, so pulling it down is correct here.

---

## Example 3 — Frontend: prop drilling is a pass-through variable

`currentUser` is needed by `AvatarMenu`, four levels deep. Today it is passed
`App → Layout → Header → Toolbar → AvatarMenu`, and every intermediate
component's props list includes `currentUser` though only the leaf uses it.

`currentUser` is a pass-through variable (the different-layer check). The intermediate
components are forced to know about a value they have no use for. Adding the
next such value means editing the whole chain again. Fix it with a shared object
scoped to the endpoints, such as a `CurrentUserContext` provided near `App` and
read in `AvatarMenu`. The intermediates lose the prop entirely. Keep the context small
and its value stable, because a context that becomes a grab-bag has the
downsides of global state.

A related frontend case: a `<UserMenuWrapper>` that renders `<UserMenu>` and
only forwards its props is a pass-through method. Delete it and let callers use
`UserMenu` directly, or give the wrapper a real responsibility.

---

## Example 4 — Frontend: classitis from over-componentization

A team splits a list row into `<RowContainer>`, `<RowInner>`, `<RowText>`,
`<RowMeta>`, and `<RowChrome>`. Each of the five components is a handful of
lines, only the component above it ever uses it, and none means anything alone.

The subdivision cost (the split/merge check / classitis) is five interfaces to
learn, five files to flip between, and dependencies hidden across them. No
boundary hides any information, because none owns a distinct piece of knowledge.
All the relatedness signals favor merging, because the components share state,
are always used together, and none can be understood alone. Collapse to one `<Row>` component. It is longer, and it
is one coherent deep abstraction with a simple prop interface. Under the depth
check, that one component beats five shallow ones.

A counter-case shows that the rule is not "never split". If `<Row>` also contained
the logic for formatting currency across locales, that *is* a distinct body of
knowledge with reuse elsewhere. Extract it as a general-purpose helper, and split
on a knowledge boundary. Line count never justifies a split on its own.

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
