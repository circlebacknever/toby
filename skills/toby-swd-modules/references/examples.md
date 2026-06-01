# Worked Examples

Original code and structures. The reasoning is what transfers.

---

## Example 1 — Backend: temporal decomposition, fixed by merging

A team builds request handling as two classes: `RequestReader` reads bytes off
the socket into a string; `RequestParser` parses the string into a structured
request. Described as "first read, then parse" — the tell.

The defect: the reader cannot know where the request ends without parsing the
headers (the length header determines body size). So both classes know the
request format. That knowledge is a single design decision living in two
modules — leakage — and parsing code ends up duplicated. Callers also have to
invoke two objects in a fixed order.

Fix per checks 1, 2, 6: the knowledge is "the request wire format," and it
should live in one module. Merge into one `Request` module that reads and
parses behind a single `Request.receive(socket)`. The format knowledge is now in
one place, the inter-module string-passing interface disappears, and callers
make one call. The merged module is deeper than either original.

---

## Example 2 — Backend: pull complexity downward instead of a config knob

A retrying transport needs a retry interval. Tactical move: export
`retry_interval_ms` as a configuration parameter and let operators set it.

Apply check 3. Ask: can the caller pick a better value than the module can? For
a retry interval, almost never — the module sees the actual round-trip times and
the operator is guessing. So compute it: measure observed response latency and
use a multiple of it, adapting as conditions change. The parameter leaves the
interface entirely. If a hard override is truly needed for some environment,
keep it as an optional argument with that computed value as the default, so the
common case specifies nothing.

Guardrail check: this complexity is related to the transport's own job and it
simplifies every caller, so pulling it down is correct rather than leakage.

---

## Example 3 — Frontend: prop drilling is a pass-through variable

`currentUser` is needed by `AvatarMenu`, four levels deep. Today it is passed
`App → Layout → Header → Toolbar → AvatarMenu`, and every intermediate
component's props list carries `currentUser` though only the leaf uses it.

This is a pass-through variable (check 4). The intermediate components are
forced to know about a value they have no use for, and adding the next such
value means editing the whole chain again. Fix with a shared object scoped to
the endpoints: a `CurrentUserContext` provided near `App` and read in
`AvatarMenu`. The intermediates lose the prop entirely. Keep the context small
and its value stable; a context that becomes a grab-bag has the downsides of
global state.

A related frontend case: a `<UserMenuWrapper>` that renders `<UserMenu>` and
only forwards its props is a pass-through method — delete it and let callers use
`UserMenu` directly, or give the wrapper a real responsibility.

---

## Example 4 — Frontend: classitis from over-componentization

A list row is split into `<RowContainer>`, `<RowInner>`, `<RowText>`,
`<RowMeta>`, `<RowChrome>` — five components, each a handful of lines, each only
ever used by the one above it, none independently meaningful.

Subdivision cost (check 6 / classitis): five interfaces to learn, five files to
flip between, dependencies hidden across them, and no information hidden by any
boundary because none owns a distinct piece of knowledge. The relatedness
signals all point one way — they share state, are always used together, and none
can be understood alone. Collapse to one `<Row>` component. It is longer but it
is one coherent deep abstraction with a simple prop interface, which the depth
check (7) prefers over five shallow ones.

Counter-case so this is not read as "never split": if `<Row>` also contained
the logic for formatting currency across locales, that *is* a distinct body of
knowledge with reuse elsewhere — extract it as a general-purpose helper. Split
on a real knowledge boundary, never on line count.

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
