---
name: toby-swd-modules
description: >-
  Decide which module code goes in and which module defines each piece of knowledge. Use it when
  a task creates, moves, splits, merges, or places code, or when ownership
  is split across functions, classes, services, files, packages, components, hooks,
  store slices, repositories, controllers, native modules, screens, or data
  layers. It covers placement, the decision to split or merge, and the definition of
  a deep module. Skip it when the question is what one signature exposes,
  which `toby-swd-interfaces` covers, and skip it for an edit inside one
  existing module that adds no new boundary.
---

# Toby SWD Modules

Module structure determines which module stores each piece of knowledge and how much callers must know to do their job. When the structure is right, future changes need no rework. When it is wrong, every change costs more than the last, because each one adds a new flag or a parallel branch.

**A good module is deep, which means it offers a simple interface to substantial functionality.** Treat the interface as the cost the module adds to the system, and treat the implementation as its benefit. Maximize benefit per unit of interface cost. Do not default to "more, smaller modules." Every extra module is an interface to learn, more pieces to track, and a new risk of duplicated logic. Split a module only when the reason is stronger than a first instinct.

## Make modules somewhat general-purpose

Design each boundary to serve more than one caller. Support only the variants someone has named. `toby-swd-interfaces` covers how to apply this rule to a callable surface.

## The checks

Apply these to any boundary decision. They are cheap, so run all of them. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Decompose by knowledge

State the one design decision or piece of knowledge each module encapsulates. If someone describes the split as a sequence, such as "first read, then parse, then write", that split is temporal decomposition. It spreads one piece of knowledge across stages. It also produces shallow modules. Divide the code again so each module contains one whole body of knowledge.

This check is the single-responsibility principle. "One reason to change" and "one body of knowledge" are the same test. It does not mean one function per file. A long function that is one coherent deep abstraction stays whole.

Two pieces belong together when they share knowledge, or when using one almost always means using the other. They also belong together when they fall under one simple higher-level category, or when one cannot be understood without the other. The "using one means the other" relation must hold in both directions. A cache uses a hash table, but hash tables serve unrelated callers, so they stay apart.

### 2. Information-leakage check

Take each significant design decision or implementation detail: a file format, a wire protocol, a storage layout, a policy. Count how many modules would need to change if it changed. More than one is leakage, which means the boundary is wrong. Move that knowledge so exactly one module has it.

Shared signatures are not leakage when each participant adds distinct functionality. Don't flag an interface known to caller and implementer, a dispatcher and its handlers, several implementations of one interface, or a decorator and its object. Leakage is a hidden decision duplicated across modules.

### 3. Pull complexity downward

Put unavoidable complexity inside the module, when it is related to that module's job. A module has more callers than authors, so the author should handle the hard part.

Prefer computing a value internally over exporting a configuration parameter or throwing to the caller. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

Guardrail: pull down only the complexity that relates to the module's function and simplifies both the callers and the interface. Pulling unrelated complexity down is another form of leakage, and in the extreme case it produces a god module. When a boundary is also a serialization or process boundary, crossing it costs a round trip and a serialize/deserialize at runtime. That runtime cost adds to the cognitive cost. Prefer one coarse call over many fine-grained ones across that boundary.

### 4. Give adjacent layers different abstractions

Adjacent layers should present different abstractions. When adjacent layers present similar abstractions, the problem usually appears as a pass-through method or a pass-through variable.

- A **pass-through method** does almost nothing except forward arguments to another method with a near-identical signature. Fix it by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two methods.
- A **pass-through variable** is a value passed through a chain of methods that don't use it. In frontend code it is prop drilling, and in mobile code it is a parameter passed across navigation stacks. Across a message boundary, it is a field that an intermediate hop relays without reading it. Fix it with a shared object between the endpoints, or with a context that stays small and preferably immutable.

A decorator that adds little is a shallow pass-through that looks like it adds something. Before adding one, ask whether the behavior belongs in the underlying module.

### 5. Prefer composition over implementation inheritance

Watch for two-way coupling, which is any mechanism where a shared-behavior provider and its consumers can each silently break the other. Implementation inheritance is the common form. Default methods on an interface or trait, or a generic module that makes hidden assumptions about its argument, can reproduce it. In a language without implementation inheritance, apply this check as a general caution against two-way coupling.

Interface inheritance and implementation inheritance have very different costs.

In **interface inheritance**, a parent declares method signatures with no bodies, and subclasses each implement them differently. This form is a tool for depth, because one interface can have many implementations, such as a `Storage` interface implemented by disk, S3, and memory. Use it freely when the interface captures real shared structure. It is also the open-closed mechanism for cases that own state. A new case is a new implementation, and the code that selects between cases does not change.

In **implementation inheritance**, a parent supplies method bodies that subclasses can use or override. This form creates a hidden two-way coupling. Subclass authors must read the parent to know what they inherited. Parent authors must check every subclass before changing instance variables or non-final methods. Instance variables visible to both sides are a standard example of information leakage across modules. Class hierarchies built heavily on implementation inheritance tend to be the hardest parts of a codebase to change.

Default to composition. A "shared logging behavior" or "shared validation behavior" is a helper object the class holds. When you must inherit, because a framework demands it or you override one method on a stable parent, keep the inherited interface narrow. Prefer `final`/sealed parents with one or two override points, and separate parent-managed state from subclass-managed state. Don't let both sides write the same fields.

This check matters most in class-heavy Java, Kotlin, C#, Swift, Python, and TypeScript code.

### 6. Separate general code from special cases and remove the special cases

Special-purpose conditions that exist for one caller don't belong inside a general mechanism. Push them up to that caller. When possible, redesign the semantics so the special case stops existing, which is the better fix. Make the common-case path handle the edge input with no branch. 

### 7. Split or merge

**Merge** when pieces share knowledge, when the combined interface is simpler than the separate ones (it can do something automatically that callers previously coordinated), or when it removes duplicated nontrivial code.

**Split** only when the resulting pieces are independently understandable and each interface is simpler than the original. For methods, depth matters more than the habit of keeping functions small. Length alone is not a reason to split. Over-splitting is the more common error. A long method that is one coherent deep abstraction with a simple signature is fine. One valid split extracts a general-purpose subtask, so the parent keeps its interface and the child method works on its own. The other valid split divides a method doing unrelated things into separate caller-visible methods. Take the second split only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods, so do not make that split.

Apply the **conjoined-methods test**. If you can't understand one method's implementation without reading another's, the two methods are conjoined. That pair is a red flag even when the methods share a file.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally and invisibly. When the module handles far more internally than the caller manages, the module is deep. When the two are roughly equal, the module is shallow.

For a sharper test, write the module's interface comment. If it has to be long or describe internals to be complete, the module is shallow. The fix is a better decomposition. More caller-facing documentation only hides the shallowness.

As an exception, some small utilities are unavoidably shallow, and that shallowness is acceptable. Don't add artificial depth to a trivial helper.

## Replace the growing conditional

Treat a conditional as a design smell when it gains a branch every time the domain gains a case. Copying the same branch decision across call sites is the same smell. In both forms the module is not closed to modification, so adding the next case means editing shared code or several files at once. A `switch` over a set that has been stable for a year is fine, so leave it alone.

Work through these options in order and stop at the first one that fits.

1. **Remove the branch** when the type can hold the answer, or when the common path can handle the edge input. This option is often the whole fix.
2. **Data-driven dispatch** uses a lookup map when the branch selects a small behavior by a tag value.
3. **Discriminated union with an exhaustive switch** fits when branches read different fields. Guard it with `assertNever`.
4. **Polymorphism** fits when each case owns behavior, private state, or its own dependencies.
5. **Registry** fits when new cases must be addable without editing a central file. It is the most complex option.

Move to the next option only when the case bodies are substantial. Options 4 and 5 need two conditions at once: a case set that visibly grows, and case bodies that own state or dependencies. `references/replace-the-conditional.md` gives the reasoning per option and a worked example of each.

In greenfield code, build the dispatch from the start. In brownfield code, fixing a scattered conditional is a scoped refactor. Offer it with its cost and benefit, and keep it out of an unrelated change.

## Writing a placement note

- Put the file and the place inside it in the first sentence, such as "The retry helper goes in `http/client.ts`, inside `request()`."
- Give each reason as a fact from the code or the request, such as the files that call the code, a limit, a count, or how often a value changes.
- Give a rejected placement its own sentence with its cost, such as "A helper in `billing/sync.ts` would leave `orders/sync.ts` without retries."
- Say what the code or the request shows about each caller. Specify an unknown only when its answer could change the placement.
- Use verbs for what code does, such as calls, reads, writes, stores, and returns. Do not write that a module owns, knows, or decides, or that code lives, sits, or belongs somewhere.
- Terms in this skill, such as deep module, leakage, and pulling complexity down, are for your reasoning. The note states the fact behind the term.
- End after the last reason or unknown, with no restatement of the placement.

## Brownfield Work

When placing code in an existing module, inspect where the surrounding code already puts that knowledge. If the new work fits awkwardly, describe the current placement problem and suggest the smallest local boundary cleanup that would make the change fit. Do not turn a local placement issue into a module-tree redesign. If a touched meaningful module has no AGENTS.md, offer to create one after the boundary is understood.

## Red flags

Run this list against the diff before calling a boundary decision done.

- **Information leakage**: one hidden decision appears in several modules.
- **Temporal decomposition**: structure follows execution order, so one body of knowledge ends up scattered across stages.
- **Special-general mixture**: a general mechanism contains caller-specific conditions.
- **Shallow module**: the interface is nearly as complex as the implementation.
- **Pass-through method**: a method forwards arguments and adds no functionality.
- **Pass-through variable**: a value is passed through methods that don't use it, such as prop drilling or passing a parameter through navigation.
- **Conjoined methods**: one can't be understood without the other.
- **Repetition**: nontrivial code is repeated, so factor it to one place.
- **Classitis / over-subdivision**: many shallow modules have interfaces that sum to more complexity than they remove (frontend: over-componentization).
- **Deep implementation-inheritance hierarchy**: you can't read the subclasses without reading the parent, and you can't change the parent without checking the subclasses. This hierarchy creates two-way coupling, even though people describe it as reuse.
- **Accessors as the public surface**: a module whose surface is mostly per-field get/set is definitionally shallow. The `toby-swd-interfaces` red flags give the replacement and the plain-data exception.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy is applied for its own sake, when the problem does not have the structure the pattern solves. A pattern is worth adding only when it removes complexity.
- **Conditional that grows per domain change**: a `switch` or `if` chain takes a new arm every time the domain gains a case, or the same branch decision is copied across call sites. Convert it with the ordered options in "Replace the growing conditional." A single stable dispatch point over a closed set is not this flag.

## References

Open one of these files. Read the stack file that matches the code you are placing, and open a subject file only when that subject is the change.

- `references/examples.md` covers Python backend and React web. Start with its cases.
- `references/replace-the-conditional.md` covers the five options in order with a worked example for each, then React, React Native, and backend forms.
- `references/web.md` covers React, Solid, and Svelte, including hooks, composables, runes, server state, store slices, and headless components.
- `references/mobile.md` covers React Native, navigation state, native modules, and async storage.
- `references/backend-apis.md` covers Java/Spring, Go, and TypeScript backends. Its examples show composition versus inheritance most concretely.
- `references/databases.md` covers the repository pattern, schema as interface, ORMs, and transactions.
- `references/caching.md` covers the cache as a deep module, invalidation, and stampedes.
