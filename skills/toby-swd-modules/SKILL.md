---
name: toby-swd-modules
description: >-
  Contains Toby's checks for where code goes and when to split or merge modules.
  Entry skills open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Modules

A good module is deep, which means it offers a simple interface to substantial functionality.

## Where new code goes

Follow "Default structure" in `toby-swd-architecture` for where a feature's entry point, rules, data access, and wiring go. In existing code, put new code where the surrounding code puts that kind of knowledge, but never put a rule in an entry point. When the new code fits awkwardly there, describe the placement problem. Make the smallest boundary change that "Before the first edit" in `toby-swd-campfire` allows, or list it as a follow-up at file:line.

## The checks

Run all of these checks whenever you decide where code goes or where one module ends and another begins. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Split by what each module hides

Give each module one design decision to hide, starting with those most likely to change, such as a file format or a pricing rule. When you describe a split as steps in time order, such as "first read, then parse, then write", the split is temporal decomposition. Divide the code again so each module hides one whole decision.

When two teams change the same code, split that code into two modules, one for each team.

Put two pieces of code in one module when any of these hold:

- both depend on one design decision
- each is almost always used with the other
- they fall under one simple higher-level category
- one cannot be understood without the other

### 2. Information-leakage check

Take each significant design decision or implementation detail: a file format, a wire protocol, a storage layout, a policy. Count how many modules would need to change if it changed. More than one is leakage. Move that knowledge so exactly one module has it.

Two modules may share a signature without leakage when each adds its own functionality. Do not report leakage for a caller and an implementer of one interface, or for a dispatcher and its handlers. Also do not report it for several implementations of one interface, or for a decorator and the object it wraps.

### 3. Pull complexity downward

Put unavoidable complexity inside the module when it relates to that module's job and simplifies both the callers and the interface.

When calls cross a process, network, or serialization boundary, prefer one call that does a lot over many small calls.

Prefer computing a value inside the module over adding a configuration parameter or throwing an error that leaves the caller to handle the problem. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

### 4. Give adjacent layers different abstractions

Look for a pass-through method or a pass-through variable. A pass-through usually means that the adjacent layers offer nearly the same abstraction. Open `references/pass-through.md` for the fixes.

### 5. Prefer composition over implementation inheritance

Use interface inheritance freely, and default to composition. Open `toby-swd-extensibility` by path when a change adds a case, an implementation, or a subclass.

### 6. Separate general code from special cases

Special-purpose conditions that exist for one caller don't go inside a general mechanism. Push them up to that caller, or move the branch onto the type, as option 1 in `toby-swd-extensibility` describes.

### 7. Split or merge

Split only when the resulting pieces are independently understandable and each interface is simpler than the original. Before you split, merge, extract, or inline code, open `references/split-or-merge.md`.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally. When the two are roughly equal, the module is shallow.

Write the module's interface comment, and when it must be long or describe internals to be complete, split the module a different way. A trivial helper may stay shallow.

## Red flags

Before calling a boundary decision done, check the diff against the checks above and this list.

- **Classitis, or too many small modules**: many shallow modules have interfaces that add more complexity than the modules remove. Too many frontend components is the same flag.
- **Accessors as the public surface**: a module whose surface is mostly per-field get/set is shallow by definition. The `toby-swd-interfaces` red flags give the replacement and the plain-data exception.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy is applied for its own sake, when the problem does not have the structure the pattern solves. A pattern is worth adding only when it removes complexity.

## References

Open the platform file below that matches the repo's framework, and a topic file only when the change is about that topic.

- `references/examples.md` has worked cases for temporal decomposition, a computed parameter, prop drilling, and too many components. Open it when a check matches and the fix is unclear.
- `references/placement-note.md` has the rules for a note that tells a reader where code goes. Open it when you explain a placement to the user or state one in a plan.
- `references/web.md` covers React, Solid, and Svelte server state, shared behavior, store slices, and headless components.
- `references/mobile.md` covers React Native auth state and data access in screens.
- `references/backend-apis.md` covers base controllers and middleware chains in Spring and Nest.
- `references/databases.md` covers ORM placement, one type per audience, and read models.
- `references/caching.md` covers which layer contains the cache and where eviction runs.
