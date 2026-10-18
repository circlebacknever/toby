---
name: toby-swd-modules
description: >-
  Contains Toby's checks for where code goes and when to split or merge
  modules. Use it for a new module or boundary, or a question about where code
  belongs. Skip it for a change inside one function.
---

# Toby SWD Modules

A good module is deep: it offers a simple interface to substantial functionality.

## Where new code goes

Follow "Default structure" in `toby-swd-architecture` for entry points, rules, data access, and wiring. In existing code, put new code where the surrounding code puts that knowledge, and never put a business rule in an entry point. When new code fits awkwardly, state the placement problem and make the smallest boundary fix that `toby-swd-campfire` allows, or list it as a follow-up at `file:line`.

## The checks

Run these eight checks whenever you place code or set a module boundary. Reserve multi-file restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Split by what each module hides

Give each module one design decision to hide, starting with decisions likely to change (such as a file format, wire protocol, or pricing rule). When you describe a split as steps in time order ("first read, then parse, then write"), that is temporal decomposition, so merge or re-split until one module hides the whole format or protocol. Split code when two teams edit it for different reasons. Put two pieces of code in one module when they share a design decision, are always used together, share one simple category, or can't be understood apart.

### 2. Information-leakage check

Count how many modules must change when one file format, wire protocol, storage layout, or policy changes. More than one is leakage, so move that knowledge into a single module. Two modules sharing an interface signature without sharing format internals (such as a caller and an implementer, or a dispatcher and its handlers) aren't leaking information.

### 3. Pull complexity downward

Handle unavoidable complexity inside the module when it belongs to that module's job and simplifies callers. Across a process, network, or serialization boundary, prefer one coarse call over many fine-grained calls. Prefer computing a tuning value inside the module over exposing a configuration parameter whenever callers can't pick a better value.

### 4. Give adjacent layers different abstractions

Check for pass-through methods and pass-through variables, which show that adjacent layers expose the same abstraction. Open `references/pass-through.md` for the fixes.

### 5. Prefer composition over implementation inheritance

Use interface inheritance freely, and default to helper composition over base classes. Open `toby-swd-extensibility` when adding a case, implementation, or subclass.

### 6. Separate general code from special cases

Keep caller-specific branches out of general mechanisms, and push the branch up to the caller or move it onto the data type (`toby-swd-extensibility` option 1).

### 7. Split or merge

Split a module or function only when each piece is independently understandable and has a simpler interface than the original. Open `references/split-or-merge.md` before splitting, merging, extracting, or inlining code.

### 8. Depth check

Weigh what the caller must manage (parameters, preconditions, call order, error cases) against the work the module handles inside. When the two are roughly equal, or the interface comment must describe internals to be complete, the module is shallow, so merge or re-split it. A tiny local helper may stay shallow.

## Red flags

Check the diff against the eight checks above and these red flags:

- **Classitis (too many tiny modules or components):** shallow modules whose interfaces add more mental overhead than their bodies save.
- **Accessors as the public surface:** per-field getters and setters that expose the storage layout. `toby-swd-interfaces` gives the replacement methods and the plain-data exception.
- **Pattern forced onto the problem:** a Visitor, Factory, Observer, or Strategy added when direct code or a lookup map is simpler.

## References

Open the platform file matching the repo's stack, and a topic file only when relevant:

- `references/examples.md` covers temporal decomposition, computed parameters, prop drilling, and over-componentization.
- `references/placement-note.md` covers how to write a placement note in chat or a plan.
- `references/web.md` covers React, Solid, and Svelte server state, shared behavior, store slices, and headless hooks.
- `references/mobile.md` covers React Native auth state and screen data access.
- `references/backend-apis.md` covers base controllers and middleware chains.
- `references/databases.md` covers ORM boundaries, row/domain/DTO splits, and read models.
- `references/caching.md` covers cache placement and eviction ownership.
