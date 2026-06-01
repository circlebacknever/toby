---
name: toby-swd-modules
description: >-
  Module boundaries determine where complexity hides or dies. Use this skill
  when a task creates, moves, splits, merges, or places code, or when a change
  raises ownership questions across functions, classes, services, files,
  packages, React components, hooks, store slices, repositories, controllers,
  native modules, screens, cache layers, or data-layer modules.
---

# Toby SWD Modules

Module structure is not organizational tidying. It is a decision about who owns which knowledge and how much callers must know to do their job. Get it right and future changes land cleanly. Get it wrong and every change racks up interest — a new flag here, a parallel branch there — until the system resists change more than it enables it.

**A good module is deep: a simple interface over substantial functionality.** The interface is the cost the module imposes on the system; the implementation is the benefit. Maximize benefit per unit of interface cost. "More, smaller modules" is the wrong reflex — every extra module is an interface to learn, more pieces to track, and a new risk of duplicated logic. The bar for splitting is higher than instinct suggests.

## Bias toward somewhat general-purpose

Before the checks, one framing decision. When you design a module's interface, the functionality reflects your current needs — but the interface should support more than one. A module designed for exactly one caller produces a one-call-shaped hole that the next caller cannot use without widening it.

Four questions, asked early:

- What is the simplest interface that covers all your current needs? (Fewer methods, broader semantics — not more methods.)
- In how many situations will this method be used? A method serving one call site is a candidate for inlining or for redesign into something serving more.
- Is this API easy to use for the common case today? General-purpose interfaces fail when they make the easy thing hard.
- Will this generalize without becoming a god interface? Generality with a clear single purpose is depth. Generality across unrelated purposes is sprawl.

The mistake to avoid in the other direction is speculative generality — adding parameters or extension points for futures that never arrive. "Somewhat" is the operative word. Cover today's needs and one or two near-future variants that you can name, not every imaginable one.

## The checks

Apply these to any boundary decision. They are cheap; run all of them. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Decompose by knowledge, not execution order

State the one design decision or piece of knowledge each module encapsulates. If the split is described as a sequence — "first read, then parse, then write" — that is temporal decomposition. It scatters one piece of knowledge across stages and produces shallow modules. Re-slice so each module owns a body of knowledge end to end.

Two pieces belong together when they share knowledge, when using one almost always means using the other (the relation must run both ways — a cache uses a hash table but hash tables serve unrelated callers, so they stay apart), when they fall under one simple higher-level category, or when one cannot be understood without the other.

### 2. Information-leakage check

For each significant design decision or implementation detail — a file format, a wire protocol, a storage layout, a policy — count how many modules would need to change if it changed. More than one is leakage: the boundary is wrong. Move that knowledge so it lives in exactly one module.

Shared signatures are not leakage when each participant adds distinct functionality. Don't flag: an interface known to caller and implementer, a dispatcher and the handlers it selects, several implementations of one interface, or a decorator and the object it wraps. Leakage is a hidden decision duplicated across modules, not a deliberately shared contract.

### 3. Pull complexity downward

When complexity is unavoidable and related to a module's job, the module absorbs it — callers don't. A module has more callers than authors. The author should take the harder side.

Prefer computing a value internally over exporting a configuration parameter or throwing to the caller. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

Guardrail: only pull down complexity that is related to the module's function, simplifies callers, and simplifies the interface. Pulling unrelated complexity down is leakage with a new hat. Pulling everything down is a god module.

### 4. Different layer, different abstraction

Adjacent layers should present different abstractions. Similar abstractions across adjacent layers usually surfaces as:

- **Pass-through method**: does almost nothing but forward arguments to another method with a near-identical signature. Fix by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two.
- **Pass-through variable**: a value threaded through a chain of methods that don't use it (frontend: prop drilling; mobile: param threading across navigation stacks). Fix with a shared object between the endpoints, or a context, kept small and preferably immutable.

A decorator that adds little is a shallow pass-through in disguise. Before adding one, ask whether the behavior belongs in the underlying module.

### 5. Prefer composition over implementation inheritance

Two kinds of inheritance, two very different cost profiles.

**Interface inheritance** — a parent declares method signatures with no bodies; subclasses each implement them differently. This is a tool for depth: one interface, many implementations (a `Storage` interface implemented by disk, S3, memory). Use it freely when the interface captures real shared structure.

**Implementation inheritance** — a parent supplies method bodies that subclasses can use or override. This creates a hidden two-way coupling. Subclass authors must read the parent to know what they inherited; parent authors must check every subclass before changing instance variables or non-final methods. Instance variables visible to both sides are textbook information leakage across modules. Class hierarchies built heavily on implementation inheritance tend to be the hardest parts of a codebase to change.

Default to composition. A "shared logging behavior" or "shared validation behavior" is a helper object the class holds, not a base class it extends. When you must inherit (a framework demands it, you truly override one method on a stable parent), keep the surface narrow: prefer `final`/sealed parents with one or two override points, and separate parent-managed state from subclass-managed state — don't let both sides write the same fields.

This check applies hardest in Java, Kotlin, C#, Swift, and Python OOP-heavy code. It applies less to Go (no inheritance; composition is the default) and to Rust (traits are interface inheritance). For TypeScript and JS, the same rule holds: extending a class to inherit behavior is the costly form; mixins, hooks, and helper objects are usually better.

### 6. Separate general from special; remove special cases

Special-purpose conditions that exist for one caller don't belong inside a general mechanism. Push them up to that caller, or — better when possible — redesign the semantics so the special case stops existing: make the common-case path handle the edge input with no branch. Relocating a special case is second best to eliminating it.

### 7. Split or merge — decide deliberately

**Merge** when pieces share knowledge, when the combined interface is simpler than the separate ones (it can do something automatically that callers previously coordinated), or when it removes duplicated nontrivial code.

**Split** only when the resulting pieces are independently understandable and each interface is simpler than the original. For methods specifically: length alone is not a reason to split, and over-splitting is the more common error. A long method that is one coherent deep abstraction with a simple signature is fine. Two valid splits: extract a general-purpose subtask (parent keeps its interface, child stands alone), or divide a method doing unrelated things into separate caller-visible methods — the second only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods; don't.

**Conjoined-methods test**: if you can't understand one method's implementation without reading another's, they are conjoined — a red flag whether or not they sit in the same file.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally and invisibly. Strong asymmetry toward internal means deep; rough parity means shallow.

Sharper test: write the module's interface comment. If it has to be long or describe internals to be complete, the module is shallow. The fix is a better decomposition, never more caller-facing documentation.

Exception: some small utilities are unavoidably shallow. Acceptable. Don't inflate a trivial helper into artificial depth.

### 9. Proportionality

The checks above are cheap and apply on every edit. A full restructuring proposal is reserved for modules that are exported, have several callers, cross a service boundary, or are costly to change.

## Brownfield Work

When placing code in an existing module, inspect where the surrounding code already puts that knowledge. If the new work fits awkwardly, name the current ownership problem and suggest the smallest local boundary cleanup that would make the change fit. Do not turn a local placement issue into a module-tree redesign. If a touched meaningful module has no AGENTS.md, offer to create one after the boundary is understood.

## Red flags

- **Information leakage**: one hidden decision reflected in several modules.
- **Temporal decomposition**: structure follows execution order, not knowledge.
- **Special-general mixture**: caller-specific conditions inside a general mechanism.
- **Shallow module**: interface nearly as complex as the implementation.
- **Pass-through method**: forwards arguments, adds no functionality.
- **Pass-through variable**: threaded through methods that don't use it; prop drilling; nav-param threading.
- **Conjoined methods**: one can't be understood without the other.
- **Repetition**: nontrivial code repeated; factor it to one place.
- **Classitis / over-subdivision**: many shallow modules whose interfaces sum to more complexity than they remove (frontend: over-componentization).
- **Deep implementation-inheritance hierarchy**: subclasses you can't read without reading the parent, parents you can't change without checking the subclasses. Two-way coupling masquerading as reuse.
- **Getters and setters as the public surface**: a class whose interface is mostly `getFoo`/`setFoo` is exposing its instance variables with extra syntax. The interface and the implementation are the same shape — definitionally shallow. Replace with methods that express intent (`reserve()`, `markPaid()`) and keep state private.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy applied because patterns are good, not because the problem has the shape the pattern solves. Patterns earn their place by removing complexity, not by being applied.

## References

Worked examples organized by domain. Read the file matching the code you are in:

- `references/examples.md` — Python backend and React web. The canonical starting cases.
- `references/web.md` — React, Solid, Svelte. Hooks/composables/runes, server state, store slices, headless components.
- `references/mobile.md` — React Native, navigation state, native modules, async storage.
- `references/backend-apis.md` — Java/Spring, Go, TypeScript backends. Composition vs inheritance shows up most concretely here.
- `references/databases.md` — Repository pattern, schema as interface, ORMs, transactions.
- `references/caching.md` — Cache as a deep module, invalidation, stampedes.
