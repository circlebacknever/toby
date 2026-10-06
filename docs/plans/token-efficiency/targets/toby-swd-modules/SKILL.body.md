# Toby SWD Modules

**A good module is deep, which means it offers a simple interface to substantial functionality.** Treat the interface as the cost the module adds to the system, and treat the implementation as its benefit. Maximize benefit per unit of interface cost. Design each boundary to serve more than one caller, and support only the variants someone has named. `toby-swd-interfaces` covers how to apply this to a callable surface.

## The checks

Apply these to any boundary decision. They are cheap, so run all of them. Reserve full restructuring proposals for modules that are exported, have multiple callers, cross a service boundary, or are costly to change later.

### 1. Decompose by knowledge

Give each module one design decision to hide, starting with those most likely to change, such as a file format or a pricing rule. A split described as a sequence, such as "first read, then parse, then write", is temporal decomposition, which spreads one decision across shallow stages. Divide the code again so each module hides one whole decision. This check is the single-responsibility principle. A reason to change is a person or team that asks for changes, so put code that two teams change in two modules.

Two pieces belong together when they share knowledge, or when using one almost always means using the other. They also belong together when they fall under one simple higher-level category, or when one cannot be understood without the other. The "using one means the other" relation must hold in both directions. A cache uses a hash table, but hash tables serve unrelated callers, so they stay apart.

### 2. Information-leakage check

Take each significant design decision or implementation detail: a file format, a wire protocol, a storage layout, a policy. Count how many modules would need to change if it changed. More than one is leakage, which means the boundary is wrong. Move that knowledge so exactly one module has it.

Shared signatures are not leakage when each participant adds distinct functionality. Don't flag an interface known to caller and implementer, a dispatcher and its handlers, several implementations of one interface, or a decorator and its object.

### 3. Pull complexity downward

Put unavoidable complexity inside the module when it relates to that module's job and simplifies both the callers and the interface. A module has more callers than authors, so the author should handle the hard part. Pulling unrelated complexity down is another form of leakage, and in the extreme case it produces a god module. Across a process or serialization boundary, prefer one coarse call over many fine-grained ones, because each call costs a round trip and serialization.

Prefer computing a value internally over exporting a configuration parameter or throwing to the caller. Before exposing a parameter, ask whether the caller can choose a better value than the module can.

### 4. Give adjacent layers different abstractions

Look for a pass-through method or a pass-through variable, which is how similar abstractions in adjacent layers usually appear.

- A **pass-through method** does almost nothing except forward arguments to another method with a near-identical signature. Fix it by exposing the lower module to callers, redistributing responsibility so the call disappears, or merging the two methods.
- A **pass-through variable** is a value passed through a chain of methods that don't use it, such as prop drilling in frontend code. Fix it with a shared object between the endpoints, or with a context that stays small and preferably immutable.

A decorator that adds little is a shallow pass-through. Before adding one, ask whether the behavior goes in the underlying module.

### 5. Prefer composition over implementation inheritance

Use interface inheritance freely when one interface has several implementations, such as a `Storage` interface with disk, S3, and memory implementations. A new case is then a new implementation, and the code that selects between cases does not change. Default to composition, and hold shared behavior in a helper object. Implementation inheritance lets a parent and its subclasses each silently break the other. Default methods on an interface or trait, and a generic module with hidden assumptions about its argument, do the same. When a framework requires inheritance, or you override a stable parent, keep the parent final or sealed with one or two override points. Do not let the parent and a subclass write the same fields.

### 6. Separate general code from special cases

Special-purpose conditions that exist for one caller don't go inside a general mechanism. Push them up to that caller, or remove them with option 1 under "Replace the growing conditional".

### 7. Split or merge

**Merge** when pieces share knowledge, when the combined interface is simpler than the separate ones (it can do something automatically that callers previously coordinated), or when it removes a copy of one rule. Keep blocks separate when they look alike and change for different reasons.

**Split** only when the resulting pieces are independently understandable and each interface is simpler than the original. Length alone is not a reason to split, so a long method that is one deep abstraction with a simple signature stays whole. One valid split extracts a general-purpose subtask, so the parent keeps its interface and the child method works on its own. The other valid split divides a method doing unrelated things into separate caller-visible methods. Take the second split only if most callers need just one of the results. If callers must invoke both halves and pass state between them, the split created shallow methods, so do not make that split.

**Inline** a shared helper back into its callers when it has gained a flag parameter or a branch for each caller. Then extract only the code that every caller still shares.

Apply the **conjoined-methods test**. If you can't understand one method's implementation without reading another's, the two methods are conjoined. That pair is a red flag even when the methods share a file.

### 8. Depth check

Weigh what the caller must manage to use the module (parameters, preconditions, ordering, error cases) against what it handles internally and invisibly. When the two are roughly equal, the module is shallow.

Write the module's interface comment, and when it must be long or describe internals to be complete, decompose the module again. A trivial helper may stay shallow.

## Replace the growing conditional

Treat a conditional as a design smell when it gains a branch every time the domain gains a case. Copying the same branch decision across call sites is the same smell. In both forms the module is not closed to modification, so adding the next case means editing shared code or several files at once. A `switch` over a set that has been stable for a year is fine, so leave it alone.

Work through these options in order and stop at the first one that fits.

1. **Remove the branch** when the type can hold the answer, or when the common path can handle the edge input. This option is often the whole fix.
2. **Data-driven dispatch** uses a lookup map when the branch selects a small behavior by a tag value.
3. **Discriminated union with an exhaustive switch** fits when branches read different fields. Guard it with `assertNever`.
4. **Polymorphism** fits when each case has its own behavior, private state, or dependencies.
5. **Registry** fits when new cases must be addable without editing a central file. It is the most complex option.

Move to the next option only when the case bodies are substantial. Options 4 and 5 need both a case set that visibly grows and case bodies that hold state or dependencies. Open `references/replace-the-conditional.md` when two adjacent options both seem to fit, or for the React, React Native, and backend forms.

In greenfield code, build the dispatch from the start. In brownfield code, fixing a scattered conditional is a scoped refactor. Offer it with its cost and benefit, and keep it out of an unrelated change.

## Writing a placement note

- Put the file and the place inside it in the first sentence, such as "The retry helper goes in `http/client.ts`, inside `request()`."
- Give each reason as a fact from the code or the request, such as the files that call the code, a limit, a count, or how often a value changes.
- Give a rejected placement its own sentence with its cost, such as "A helper in `billing/sync.ts` would leave `orders/sync.ts` without retries."
- Say what the code or the request shows about each caller.
- Do not write that a module owns, knows, or decides, or that code lives, sits, or belongs somewhere.
- Terms in this skill, such as deep module, leakage, and pulling complexity down, are for your reasoning. The note states the fact behind the term.

## Brownfield Work

In existing code, put new code where the surrounding code already puts that kind of knowledge. When it fits awkwardly, describe the placement problem and offer the smallest local boundary cleanup. Do not turn a local placement issue into a module-tree redesign.

## Red flags

Run this list against the diff before calling a boundary decision done. Each entry points to the check that defines it, so re-read that check when the flag might fire.

- **Information leakage** — check 2.
- **Temporal decomposition** — check 1.
- **Special-general mixture** — check 6.
- **Shallow module** — check 8.
- **Pass-through method** — check 4.
- **Pass-through variable** — check 4.
- **Conjoined methods** — check 7.
- **Repeated rule**: one rule is written in two places, so a change to one must change both.
- **Classitis / over-subdivision**: many shallow modules have interfaces that sum to more complexity than they remove (frontend: over-componentization).
- **Deep implementation-inheritance hierarchy** — check 5.
- **Accessors as the public surface**: a module whose surface is mostly per-field get/set is definitionally shallow. The `toby-swd-interfaces` red flags give the replacement and the plain-data exception.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy is applied for its own sake, when the problem does not have the structure the pattern solves. A pattern is worth adding only when it removes complexity.
- **Conditional that grows per domain change** — "Replace the growing conditional" lists the options. A single stable dispatch point over a closed set is not this flag.

## References

Read the stack file that matches the code you are placing, and open a subject file only when that subject is the change.

- `references/examples.md` covers Python backend and React web cases, including a merge that fixes temporal decomposition, a computed parameter, prop drilling, and over-componentization. Open it when a check fires and the fix is unclear.
- `references/replace-the-conditional.md` covers the five options in order with a worked example for each, then React, React Native, and backend forms.
- `references/web.md` covers React, Solid, and Svelte server state, shared behavior, store slices, and headless components.
- `references/mobile.md` covers React Native auth state and data access in screens.
- `references/backend-apis.md` covers base controllers and middleware chains in Spring and Nest, the clearest composition-over-inheritance cases.
- `references/databases.md` covers ORM placement, one type per audience, and read models.
- `references/caching.md` covers which layer contains the cache and where eviction runs.
- `references/solid.md` maps SOLID to these checks. Open it when a plan, a review, or the user cites a SOLID principle by name.
