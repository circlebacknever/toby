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

Module structure decides who owns which knowledge and how much callers must know to do their job. When the structure is right, future changes need no rework. When it is wrong, every change costs more than the last, because each one adds a new flag or a parallel branch. As a result, the code gets harder to change over time.

**A good module is deep, which means it offers a simple interface to substantial functionality.** The interface is the cost the module imposes on the system, and the implementation is the benefit. Maximize benefit per unit of interface cost. "More, smaller modules" is the wrong reflex. Every extra module is an interface to learn, more pieces to track, and a new risk of duplicated logic. Split a module only for a stronger reason than first instinct gives.

## Bias toward somewhat general-purpose

Design each boundary to serve more than one caller, and support no variant beyond the ones someone has named. A module written for exactly one caller forces the next caller to widen its interface. `toby-swd-interfaces` owns the four questions that apply this rule and the speculative-generality limit. Load it when the placement decision also creates a callable surface.

## The checks

Apply these to any boundary decision. They are cheap, so run all of them. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Decompose by knowledge

State the one design decision or piece of knowledge each module encapsulates. If someone describes the split as a sequence, such as "first read, then parse, then write", that split is temporal decomposition. It scatters one piece of knowledge across stages and produces shallow modules. Divide the code again so each module owns one whole body of knowledge.

This check is the single-responsibility principle. "One reason to change" and "one body of knowledge" are the same test. It does not mean one function per file. A long function that is one coherent deep abstraction stays whole.

Two pieces belong together when they share knowledge, or when using one almost always means using the other. They also belong together when they fall under one simple higher-level category, or when one cannot be understood without the other. The "using one means the other" relation must hold in both directions. A cache uses a hash table, but hash tables serve unrelated callers, so they stay apart.

### 2. Information-leakage check

Take each significant design decision or implementation detail: a file format, a wire protocol, a storage layout, a policy. Count how many modules would need to change if it changed. More than one is leakage, which means the boundary is wrong. Move that knowledge so exactly one module has it.

Shared signatures are not leakage when each participant adds distinct functionality. Don't flag an interface known to caller and implementer, a dispatcher and its handlers, several implementations of one interface, or a decorator and its object. Leakage is a hidden decision duplicated across modules.

### 3. Pull complexity downward

Put unavoidable complexity inside the module, when it is related to that module's job. A module has more callers than authors, so the author should handle the hard part.

Prefer computing a value internally over exporting a configuration parameter or throwing to the caller. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

Guardrail: pull down only the complexity that relates to the module's function and simplifies both the callers and the interface. Pulling unrelated complexity down is another form of leakage, and pulling everything down produces a god module. When a boundary is also a serialization or process boundary, crossing it costs a round trip and a serialize/deserialize at runtime. That runtime cost adds to the cognitive cost. Prefer one coarse call over many fine-grained ones across that boundary.

### 4. Different layer, different abstraction

Adjacent layers should present different abstractions. When adjacent layers present similar abstractions, the problem usually appears in one of two forms.

- A **pass-through method** does almost nothing except forward arguments to another method with a near-identical signature. Fix it by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two methods.
- A **pass-through variable** is a value passed through a chain of methods that don't use it. In frontend code it is prop drilling, and in mobile code it is a parameter passed across navigation stacks. Across a message boundary, it is a field that an intermediate hop relays without reading it. Fix it with a shared object between the endpoints, or with a context that stays small and preferably immutable.

A decorator that adds little is a shallow pass-through that looks like it adds something. Before adding one, ask whether the behavior belongs in the underlying module.

### 5. Prefer composition over implementation inheritance

Watch for two-way coupling, which is any mechanism where a shared-behavior provider and its consumers can each silently break the other. Implementation inheritance is the common form. Default methods on an interface or trait, or a generic module that makes hidden assumptions about its argument, can reproduce it. In a language without implementation inheritance, apply this check as a general caution against two-way coupling.

Interface inheritance and implementation inheritance have very different costs.

In **interface inheritance**, a parent declares method signatures with no bodies, and subclasses each implement them differently. This form is a tool for depth, because one interface can have many implementations, such as a `Storage` interface implemented by disk, S3, and memory. Use it freely when the interface captures real shared structure. It is also the open-closed mechanism for cases that own state. A new case is a new implementation, and the code that selects between cases does not change.

In **implementation inheritance**, a parent supplies method bodies that subclasses can use or override. This form creates a hidden two-way coupling. Subclass authors must read the parent to know what they inherited. Parent authors must check every subclass before changing instance variables or non-final methods. Instance variables visible to both sides are textbook information leakage across modules. Class hierarchies built heavily on implementation inheritance tend to be the hardest parts of a codebase to change.

Default to composition. A "shared logging behavior" or "shared validation behavior" is a helper object the class holds. When you must inherit, because a framework demands it or you override one method on a stable parent, keep the inherited interface narrow. Prefer `final`/sealed parents with one or two override points, and separate parent-managed state from subclass-managed state. Don't let both sides write the same fields.

This check applies hardest in Java, Kotlin, C#, Swift, and Python OOP-heavy code. It applies less to Go (no inheritance, and composition is the default) and to Rust (traits are interface inheritance). For TypeScript and JS, the same rule holds. Extending a class to inherit behavior is the costly form, and mixins, hooks, and helper objects are usually better.

### 6. Separate general from special; remove special cases

Special-purpose conditions that exist for one caller don't belong inside a general mechanism. Push them up to that caller. When possible, redesign the semantics so the special case stops existing, which is the better fix. Make the common-case path handle the edge input with no branch. Relocating a special case is second best to eliminating it.

### 7. Split or merge

**Merge** when pieces share knowledge, when the combined interface is simpler than the separate ones (it can do something automatically that callers previously coordinated), or when it removes duplicated nontrivial code.

**Split** only when the resulting pieces are independently understandable and each interface is simpler than the original. For methods, depth matters more than the reflex to keep functions small. Length alone is not a reason to split, and over-splitting is the more common error. A long method that is one coherent deep abstraction with a simple signature is fine. One valid split extracts a general-purpose subtask, so the parent keeps its interface and the child method works on its own. The other valid split divides a method doing unrelated things into separate caller-visible methods. Take the second split only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods, so don't.

Apply the **conjoined-methods test**. If you can't understand one method's implementation without reading another's, the two methods are conjoined. That pair is a red flag even when the methods share a file.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally and invisibly. When the module handles far more internally than the caller manages, the module is deep. When the two are roughly equal, the module is shallow.

For a sharper test, write the module's interface comment. If it has to be long or describe internals to be complete, the module is shallow. The fix is a better decomposition. More caller-facing documentation only hides the shallowness.

As an exception, some small utilities are unavoidably shallow, and that shallowness is acceptable. Don't inflate a trivial helper into artificial depth.

### 9. Proportionality

The checks above are cheap and apply on every edit. A full restructuring proposal is reserved for modules that are exported, have several callers, cross a service boundary, or are costly to change.

## Replace the growing conditional

Treat a conditional as a design smell when it gains a branch every time the domain gains a case. Copying the same branch decision across call sites is the same smell. In both forms the module is not closed to modification, so adding the next case means editing shared code or several files at once. A `switch` over a set that has been stable for a year is fine, so leave it alone.

Work down this ladder and stop at the first rung that fits.

1. **Remove the branch** when the type can hold the answer, or when the common path can handle the edge input. This rung is often the whole fix.
2. **Data-driven dispatch** uses a lookup map when the branch selects a small behavior by a tag value.
3. **Discriminated union with an exhaustive switch** fits when branches read different fields. Guard it with `assertNever`.
4. **Polymorphism** fits when each case owns behavior, private state, or its own dependencies.
5. **Registry** fits when new cases must be addable without editing a central file. It is the heaviest rung.

Move up a rung only when the case bodies are substantial. Rungs 4 and 5 need two conditions at once, which are a case set that visibly grows and case bodies that own state or dependencies. `references/replace-the-conditional.md` gives the reasoning per rung and a worked example of each.

In greenfield code, build the dispatch from the start. In brownfield code, fixing a scattered conditional is a scoped refactor. Offer it with its cost and benefit, and keep it out of an unrelated change.

## Brownfield Work

When placing code in an existing module, inspect where the surrounding code already puts that knowledge. If the new work fits awkwardly, name the current ownership problem and suggest the smallest local boundary cleanup that would make the change fit. Do not turn a local placement issue into a module-tree redesign. If a touched meaningful module has no AGENTS.md, offer to create one after the boundary is understood.

## Red flags

Run this list against the diff before calling a boundary decision done.

- **Information leakage**: one hidden decision reflected in several modules.
- **Temporal decomposition**: structure follows execution order, so one body of knowledge ends up scattered across stages.
- **Special-general mixture**: caller-specific conditions inside a general mechanism.
- **Shallow module**: interface nearly as complex as the implementation.
- **Pass-through method**: forwards arguments, adds no functionality.
- **Pass-through variable**: a value passed through methods that don't use it, such as prop drilling or passing a parameter through navigation.
- **Conjoined methods**: one can't be understood without the other.
- **Repetition**: nontrivial code repeated, so factor it to one place.
- **Classitis / over-subdivision**: many shallow modules whose interfaces sum to more complexity than they remove (frontend: over-componentization).
- **Deep implementation-inheritance hierarchy**: subclasses you can't read without reading the parent, parents you can't change without checking the subclasses. This hierarchy is two-way coupling that people call reuse.
- **Accessors as the public surface**: a module whose surface is mostly per-field get/set is definitionally shallow. The `toby-swd-interfaces` red flags give the replacement and the plain-data exception.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy applied for its own sake, when the problem does not have the structure the pattern solves. A pattern is worth adding only when it removes complexity.
- **Conditional that grows per domain change**: a `switch` or `if` chain that takes a new arm every time the domain gains a case, or the same branch decision copied across call sites. Convert it with the ladder in "Replace the growing conditional." A single stable dispatch point over a closed set is not this flag.

## References

Open one. Read the stack file that matches the code you are placing, and open a subject file only when that subject is the change.

- `references/examples.md` covers Python backend and React web, and its cases are the ones to start with.
- `references/replace-the-conditional.md` — the five-rung ladder with a worked example per rung, then React, React Native, and backend forms.
- `references/web.md` — React, Solid, Svelte. Hooks/composables/runes, server state, store slices, headless components.
- `references/mobile.md` — React Native, navigation state, native modules, async storage.
- `references/backend-apis.md` — Java/Spring, Go, TypeScript backends. Composition vs inheritance shows up most concretely here.
- `references/databases.md` — Repository pattern, schema as interface, ORMs, transactions.
- `references/caching.md` — Cache as a deep module, invalidation, stampedes.
