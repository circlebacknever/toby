---
name: toby-swd-modules
description: >-
  Contains Toby's checks for where code goes and when to split or merge modules.
  Entry skills open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Modules

**A good module is deep, which means it offers a simple interface to substantial functionality.** A shallow module has an interface about as complex as the work behind it. Treat the interface as the cost the module adds to the system, and treat the implementation as its benefit. Put as much functionality as you can behind as small an interface as you can. Design each module's interface to serve more than one caller, and support only the uses someone has asked for or described. The `toby-swd-interfaces` skill covers how to apply this to the interface of a function, class, or endpoint.

## The checks

Run these checks whenever you decide where code goes or where one module ends and another begins. They are cheap, so run all of them. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Split by what each module hides

Give each module one design decision to hide, starting with those most likely to change, such as a file format or a pricing rule. When you describe a split as steps in time order, such as "first read, then parse, then write", the split is temporal decomposition. Temporal decomposition spreads one decision across several shallow modules. Divide the code again so each module hides one whole decision.

This check is the single-responsibility principle. In that principle, a "reason to change" means a person or team that asks for changes. So when two teams change the same code, split that code into two modules, one for each team.

Put two pieces of code in one module when both depend on one design decision, or when using one almost always means using the other. Two pieces also belong together when they fall under one simple higher-level category, or when one cannot be understood without the other. The "using one means the other" relation must hold in both directions. A cache uses a hash table, but hash tables serve unrelated callers, so they stay apart.

### 2. Information-leakage check

Take each significant design decision or implementation detail: a file format, a wire protocol, a storage layout, a policy. Count how many modules would need to change if it changed. More than one is leakage, which means the boundary is wrong. Move that knowledge so exactly one module has it.

Two modules may use the same signature without leakage, as long as each module adds its own functionality. Do not report leakage for an interface that both the caller and the implementer know, or for a dispatcher and its handlers. Also do not report leakage for several implementations of one interface, or for a decorator and the object it wraps.

### 3. Pull complexity downward

Put unavoidable complexity inside the module when it relates to that module's job and simplifies both the callers and the interface. Pulling complexity down means handling a hard part inside the module so callers do not have to. A module has more callers than authors, so the author should handle the hard part. Pulling unrelated complexity down is another form of leakage. At the extreme, that produces one module that does everything.

When calls cross a process, network, or serialization boundary, prefer one call that does a lot over many small calls. Each call costs a round trip and serialization.

Prefer computing a value inside the module over adding a configuration parameter or throwing an error that leaves the caller to handle the problem. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

### 4. Give adjacent layers different abstractions

Look for a pass-through method or a pass-through variable. Either one usually means that two adjacent layers offer nearly the same abstraction.

- A **pass-through method** does almost nothing except forward arguments to another method with a near-identical signature. Fix it by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two methods.
- A **pass-through variable** is a value passed through a chain of methods that don't use it, such as prop drilling in frontend code. Fix it with an object that the first and last methods in the chain both reach directly. A context object also works if it stays small and preferably immutable.

A decorator that adds little is a shallow pass-through. Before adding one, ask whether the behavior goes in the underlying module.

### 5. Prefer composition over implementation inheritance

Use interface inheritance freely when one interface has several implementations, such as a `Storage` interface with disk, S3, and memory implementations. A new case is then a new implementation, and the code that selects between cases does not change. Default to composition, and hold shared behavior in a helper object. Implementation inheritance lets a parent and its subclasses each silently break the other. Default methods on an interface or trait, and a generic module with hidden assumptions about its argument, do the same. When a framework requires inheritance or you subclass a stable parent, mark the parent final or sealed, apart from one or two overridable methods. Do not let the parent and a subclass write the same fields.

### 6. Separate general code from special cases

Special-purpose conditions that exist for one caller don't go inside a general mechanism. Push them up to that caller, or remove them with option 1 under "Replace the growing conditional".

### 7. Split or merge

**Merge** two pieces when they depend on the same design decision, or when merging removes a duplicated rule. Also merge when the merged interface is simpler because it does automatically what callers used to coordinate. Keep blocks separate when they look alike and change for different reasons.

**Split** only when the resulting pieces are independently understandable and each interface is simpler than the original. Length alone is not a reason to split, so a long method that is one deep abstraction with a simple signature stays whole. One valid split extracts a general-purpose subtask, so the parent keeps its interface and the child method works on its own. The other valid split divides a method doing unrelated things into separate caller-visible methods. Take the second split only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods, so do not make that split.

**Inline** a shared helper back into its callers when it has gained a flag parameter or a branch for each caller. Then extract only the code that every caller still shares.

Apply the **conjoined-methods test**. If you can't understand one method's implementation without reading another's, the two methods are conjoined. That pair is a red flag even when the methods share a file.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally and invisibly. When the two are roughly equal, the module is shallow.

Write the module's interface comment, and when it must be long or describe internals to be complete, split the module a different way. A trivial helper may stay shallow.

## Replace the growing conditional

Treat an `if` or `switch` as a design smell when it gains a branch each time the product adds a new kind of thing. Copying the same branch decision across call sites is the same smell. In both cases, adding the next kind means editing shared code or several files at once. A `switch` over a set that has been stable for a year is fine, so leave it alone.

Work through these options in order and stop at the first one that fits.

1. **Remove the branch** when the data type can compute the answer itself, or when the normal code path already handles the unusual input correctly. This option is often the whole fix.
2. **Data-driven dispatch** fits when each branch picks a small behavior based on the value of one field, such as `kind`. A lookup map from each value to its behavior replaces the branches.
3. **Discriminated union with an exhaustive switch** fits when branches read different fields. Guard it with `assertNever`.
4. **Polymorphism** fits when each case has its own behavior, private state, or dependencies.
5. **Registry** fits when new cases must be addable without editing a central file. It is the most complex option.

Move to the next option only when the case bodies are substantial. Use option 4 or 5 only when the list of cases keeps growing and each case has its own state or dependencies. Open `references/replace-the-conditional.md` when two adjacent options both seem to fit, or for examples in React, React Native, and backend code.

In new code, use the chosen option from the start. In existing code, fixing a conditional that is repeated in several places is a separate refactor. Offer it with its cost and benefit, and keep it out of an unrelated change.

## Writing a placement note

- Put the file and the place inside it in the first sentence, such as "The retry helper goes in `http/client.ts`, inside `request()`."
- Give each reason as a fact from the code or the request, such as the files that call the code, a limit, a count, or how often a value changes.
- Give a rejected placement its own sentence with its cost, such as "A helper in `billing/sync.ts` would leave `orders/sync.ts` without retries."
- Say what the code or the request shows about each caller.
- Do not write that a module owns, knows, or decides, or that code lives, sits, or belongs somewhere.
- Terms in this skill, such as deep module, leakage, and pulling complexity down, are for your reasoning. The note states the fact behind the term.

## Brownfield Work

In existing code, put new code where the surrounding code already puts that kind of knowledge. When the new code fits awkwardly there, describe the placement problem and offer the smallest change to nearby module boundaries that fixes it. Do not turn a local placement issue into a module-tree redesign.

## Red flags

Run this list against the diff before calling a boundary decision done. Each entry points to the check that defines it, so re-read that check when you suspect the problem.

- **Information leakage** — check 2.
- **Temporal decomposition** — check 1.
- **Special case inside general code** — check 6.
- **Shallow module** — check 8.
- **Pass-through method** — check 4.
- **Pass-through variable** — check 4.
- **Conjoined methods** — check 7.
- **Repeated rule**: one rule is written in two places, so a change to one must change both.
- **Classitis, or too many small modules**: many shallow modules have interfaces that add more complexity than the modules remove. In frontend code, the same problem appears as too many components.
- **Deep implementation-inheritance hierarchy** — check 5.
- **Accessors as the public surface**: a module whose surface is mostly per-field get/set is shallow by definition. The `toby-swd-interfaces` red flags give the replacement and the plain-data exception.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy is applied for its own sake, when the problem does not have the structure the pattern solves. A pattern is worth adding only when it removes complexity.
- **Conditional that grows per domain change** — "Replace the growing conditional" lists the options. One `switch` that handles a fixed set of cases and rarely changes does not count.

## References

Read the reference file for the platform of the code you are placing, such as web, mobile, or backend. Open a topic file, such as caching or databases, only when the change is about that topic.

- `references/examples.md` covers Python backend and React web cases, including a merge that fixes temporal decomposition, a computed parameter, prop drilling, and over-componentization. Open it when a check fires and the fix is unclear.
- `references/replace-the-conditional.md` covers the five options in order with a worked example for each, then React, React Native, and backend examples.
- `references/web.md` covers React, Solid, and Svelte server state, shared behavior, store slices, and headless components.
- `references/mobile.md` covers React Native auth state and data access in screens.
- `references/backend-apis.md` covers base controllers and middleware chains in Spring and Nest, the clearest composition-over-inheritance cases.
- `references/databases.md` covers ORM placement, one type per audience, and read models.
- `references/caching.md` covers which layer contains the cache and where eviction runs.
- `references/solid.md` maps SOLID to these checks. Open it when a plan, a review, or the user cites a SOLID principle by name.
