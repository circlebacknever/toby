---
name: toby-swd-modules
description: >-
  Decide where code lives and which module owns which knowledge. Use it when
  a task creates, moves, splits, merges, or places code, or when ownership
  crosses functions, classes, services, files, packages, components, hooks,
  store slices, repositories, controllers, native modules, screens, or data
  layers. It owns placement, the split-or-merge call, and the definition of
  a deep module. Skip it when the question is what one signature exposes,
  which `toby-swd-interfaces` owns, and skip it for an edit inside one
  existing module that adds no new boundary.
---

# Toby SWD Modules

Module structure decides who owns which knowledge and how much callers must know to do their job. Get it right and future changes land without rework. Get it wrong and every change racks up interest: a new flag here, a parallel branch there. The system ends up resisting change more than it enables it.

**A good module is deep: a simple interface over substantial functionality.** The interface is the cost the module imposes on the system, and the implementation is the benefit. Maximize benefit per unit of interface cost. "More, smaller modules" is the wrong reflex. Every extra module is an interface to learn, more pieces to track, and a new risk of duplicated logic. The bar for splitting is higher than instinct suggests.

## Bias toward somewhat general-purpose

Design each boundary to serve more than one caller, and stop one named variant short of speculation. A module shaped to exactly one caller leaves a one-call-shaped hole the next caller has to widen. `toby-swd-interfaces` owns the four questions that apply this and the speculative-generality limit. Load it when the placement decision also creates a callable surface.

## The checks

Apply these to any boundary decision. They are cheap, so run all of them. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Decompose by knowledge

State the one design decision or piece of knowledge each module encapsulates. If the split is described as a sequence — "first read, then parse, then write" — that is temporal decomposition. It scatters one piece of knowledge across stages and produces shallow modules. Re-slice so each module owns a body of knowledge end to end.

This check is the single-responsibility principle. "One reason to change" and "one body of knowledge" are the same test. It does not mean one function per file. A long function that is one coherent deep abstraction stays whole.

Two pieces belong together when they share knowledge, or when using one almost always means using the other. They also belong together when they fall under one simple higher-level category, or when one cannot be understood without the other. The "using one means the other" relation must run both ways. A cache uses a hash table, but hash tables serve unrelated callers, so they stay apart.

### 2. Information-leakage check

Take each significant design decision or implementation detail: a file format, a wire protocol, a storage layout, a policy. Count how many modules would need to change if it changed. More than one is leakage, which means the boundary is wrong. Move that knowledge so it lives in exactly one module.

Shared signatures are not leakage when each participant adds distinct functionality. Don't flag an interface known to caller and implementer, a dispatcher and its handlers, several implementations of one interface, or a decorator and its object. Leakage is a hidden decision duplicated across modules.

### 3. Pull complexity downward

Put unavoidable complexity inside the module, when it is related to that module's job. A module has more callers than authors, so the author takes the harder side.

Prefer computing a value internally over exporting a configuration parameter or throwing to the caller. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

Guardrail: only pull down complexity that is related to the module's function, simplifies callers, and simplifies the interface. Pulling unrelated complexity down is leakage under another name. Pulling everything down is a god module. When a boundary is also a serialization or process boundary, crossing it costs a round trip and a serialize/deserialize at runtime. That runtime cost sits on top of the cognitive cost. Prefer one coarse call over many fine-grained ones across that boundary.

### 4. Different layer, different abstraction

Adjacent layers should present different abstractions. Similar abstractions across adjacent layers usually surfaces as:

- **Pass-through method**: does almost nothing but forward arguments to another method with a near-identical signature. Fix by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two.
- **Pass-through variable**: a value threaded through a chain of methods that don't use it (frontend: prop drilling; mobile: param threading across navigation stacks; across a message boundary: a field relayed through an intermediate hop that doesn't read it). Fix with a shared object between the endpoints, or a context, kept small and preferably immutable.

A decorator that adds little is a shallow pass-through that looks like it adds something. Before adding one, ask whether the behavior belongs in the underlying module.

### 5. Prefer composition over implementation inheritance

Watch for two-way coupling: any mechanism where a shared-behavior provider and its consumers can each silently break the other. Implementation inheritance is the common form. Default methods on an interface or trait, or a generic module that makes hidden assumptions about its argument, can reproduce it. A language without implementation inheritance reads this as the general two-way-coupling caution.

Interface inheritance and implementation inheritance carry very different cost profiles.

**Interface inheritance** — a parent declares method signatures with no bodies, and subclasses each implement them differently. This is a tool for depth: one interface, many implementations (a `Storage` interface implemented by disk, S3, memory). Use it freely when the interface captures real shared structure. It is also the open-closed mechanism for cases that own state: a new case is a new implementation, and the code that selects between them does not change.

**Implementation inheritance** — a parent supplies method bodies that subclasses can use or override. This creates a hidden two-way coupling. Subclass authors must read the parent to know what they inherited. Parent authors must check every subclass before changing instance variables or non-final methods. Instance variables visible to both sides are textbook information leakage across modules. Class hierarchies built heavily on implementation inheritance tend to be the hardest parts of a codebase to change.

Default to composition. A "shared logging behavior" or "shared validation behavior" is a helper object the class holds. When you must inherit (a framework demands it, you override one method on a stable parent), keep the surface narrow. Prefer `final`/sealed parents with one or two override points, and separate parent-managed state from subclass-managed state. Don't let both sides write the same fields.

This check applies hardest in Java, Kotlin, C#, Swift, and Python OOP-heavy code. It applies less to Go (no inheritance, and composition is the default) and to Rust (traits are interface inheritance). For TypeScript and JS, the same rule holds. Extending a class to inherit behavior is the costly form, and mixins, hooks, and helper objects are usually better.

### 6. Separate general from special; remove special cases

Special-purpose conditions that exist for one caller don't belong inside a general mechanism. Push them up to that caller. Better when possible: redesign the semantics so the special case stops existing. Make the common-case path handle the edge input with no branch. Relocating a special case is second best to eliminating it.

### 7. Split or merge — decide deliberately

**Merge** when pieces share knowledge, when the combined interface is simpler than the separate ones (it can do something automatically that callers previously coordinated), or when it removes duplicated nontrivial code.

**Split** only when the resulting pieces are independently understandable and each interface is simpler than the original. For methods specifically: the reflex to keep functions small is subordinate to depth. Length alone is not a reason to split, and over-splitting is the more common error. A long method that is one coherent deep abstraction with a simple signature is fine. Two valid splits: extract a general-purpose subtask (parent keeps its interface, child stands alone), or divide a method doing unrelated things into separate caller-visible methods. Take the second only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods, so don't.

**Conjoined-methods test**: if you can't understand one method's implementation without reading another's, they are conjoined — a red flag whether or not they sit in the same file.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally and invisibly. Strong asymmetry toward internal means deep, and rough parity means shallow.

Sharper test: write the module's interface comment. If it has to be long or describe internals to be complete, the module is shallow. The fix is a better decomposition. More caller-facing documentation only hides the shallowness.

Exception: some small utilities are unavoidably shallow. Acceptable. Don't inflate a trivial helper into artificial depth.

### 9. Proportionality

The checks above are cheap and apply on every edit. A full restructuring proposal is reserved for modules that are exported, have several callers, cross a service boundary, or are costly to change.

## Replace the growing conditional

Two forms of conditional are a design smell. The first gains a branch every time the domain gains a case. The second is the same branch decision copied across call sites. Both are a module that is not closed to modification. The next case edits shared code, or several files at once. A `switch` over a set that has been stable for a year is fine, so leave it alone.

Work down this ladder and stop at the first rung that fits.

1. **Remove the branch** — the type answers for itself, or the common path takes the edge input. Often the whole fix.
2. **Data-driven dispatch** — a lookup map, when the branch selects a small behavior by a tag value.
3. **Discriminated union with an exhaustive switch** — when branches read different fields. Guard it with `assertNever`.
4. **Polymorphism** — when each case owns behavior, private state, or its own dependencies.
5. **Registry** — when new cases must be addable without editing a central file. The heaviest rung.

Move up a rung only when the case bodies carry weight. Rungs 4 and 5 need two conditions at once: a case set that visibly grows, and case bodies that own state or dependencies. `references/replace-the-conditional.md` carries the reasoning per rung and a worked example of each.

Greenfield: build the dispatch from the start. Brownfield: a scattered conditional is a scoped refactor. Offer it with its cost and benefit, and keep it out of an unrelated change.

## Brownfield Work

When placing code in an existing module, inspect where the surrounding code already puts that knowledge. If the new work fits awkwardly, name the current ownership problem and suggest the smallest local boundary cleanup that would make the change fit. Do not turn a local placement issue into a module-tree redesign. If a touched meaningful module has no AGENTS.md, offer to create one after the boundary is understood.

## Red flags

Run this list against the diff before calling a boundary decision done.

- **Information leakage**: one hidden decision reflected in several modules.
- **Temporal decomposition**: structure follows execution order, so one body of knowledge ends up scattered across stages.
- **Special-general mixture**: caller-specific conditions inside a general mechanism.
- **Shallow module**: interface nearly as complex as the implementation.
- **Pass-through method**: forwards arguments, adds no functionality.
- **Pass-through variable**: threaded through methods that don't use it; prop drilling; nav-param threading.
- **Conjoined methods**: one can't be understood without the other.
- **Repetition**: nontrivial code repeated, so factor it to one place.
- **Classitis / over-subdivision**: many shallow modules whose interfaces sum to more complexity than they remove (frontend: over-componentization).
- **Deep implementation-inheritance hierarchy**: subclasses you can't read without reading the parent, parents you can't change without checking the subclasses. Two-way coupling that gets called reuse.
- **Accessors as the public surface**: a module whose surface is mostly per-field get/set is definitionally shallow. The `toby-swd-interfaces` red flags carry the replacement and the plain-data exception.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy applied for its own sake, when the problem does not have the structure the pattern solves. Patterns earn their place by removing complexity.
- **Conditional that grows per domain change**: a `switch` or `if` chain that takes a new arm every time the domain gains a case, or the same branch decision copied across call sites. Convert it with the ladder in "Replace the growing conditional." A single stable dispatch point over a closed set is not this flag.

## References

Open one. Read the stack file matching the code you are placing, and open a subject file only when that subject is the change:

- `references/examples.md` — Python backend and React web. The canonical starting cases.
- `references/replace-the-conditional.md` — the five-rung ladder with a worked example per rung, then React, React Native, and backend forms.
- `references/web.md` — React, Solid, Svelte. Hooks/composables/runes, server state, store slices, headless components.
- `references/mobile.md` — React Native, navigation state, native modules, async storage.
- `references/backend-apis.md` — Java/Spring, Go, TypeScript backends. Composition vs inheritance shows up most concretely here.
- `references/databases.md` — Repository pattern, schema as interface, ORMs, transactions.
- `references/caching.md` — Cache as a deep module, invalidation, stampedes.
