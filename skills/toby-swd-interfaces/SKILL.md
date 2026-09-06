---
name: toby-swd-interfaces
description: >-
  Design the callable surface before the implementation. Use it when a task
  adds or changes a function, method, class, component prop surface, hook
  return shape, composable, REST endpoint, gRPC service, repository, cache
  surface, or message contract. It owns the comment test, the parameter
  budget, and the general-purpose bias. Skip it when the question is where
  the code should live, which `toby-swd-modules` owns, and skip it when
  adding a field beside an identical one already in that file.
---

# Toby SWD Interfaces

The interface is everything a caller must know to use a module correctly. That is the signature, plus the informal contract only comments can carry: behavior, side effects, ordering constraints, errors. The interface is the cost the module imposes on the rest of the system. The implementation is the benefit. You want that cost much smaller than that benefit, meaning a simple interface over substantial functionality. For a message-channel boundary, the "signature" is the message contract: the request and response payload shapes, what survives serialization, and the delivery guarantees.

Interface-first design exists to find that interface before implementation locks in a bad one. It also uses the interface itself as the earliest possible signal that the design is wrong. Treat a comment you can't write short and internals-free as a bug report. It arrives while the abstraction is still only text.

This applies identically across the stack. A class's public methods. A function's signature. A service's endpoints. A component's props, a hook's return shape, a repository's query methods, a cache's get-or-load surface, a message contract across a process boundary. All are interfaces, and everything below applies to each.

## Bias toward somewhat general-purpose

Make this framing decision before the procedure, because it constrains every step after it. The functionality of a module reflects your current needs, but the interface should support more than one. A method signature shaped exactly to one caller produces a one-call-shaped hole the next caller cannot use without widening it.

Four questions, asked early:

- **What is the simplest interface that covers all your current needs?** Fewer methods, each carrying broader semantics, so the surface stays small as needs grow.
- **In how many situations will this method be used?** A method serving one call site is a candidate for inlining or for redesign into something that serves more.
- **Is this API easy to use for the common case today?** General-purpose interfaces fail when they make the easy thing hard. A `find(query)` is better than thirty `findByXAndYAndZ` only if `find(...)` is also easy to call for the common case.
- **Will this generalize without becoming a god interface?** Generality with a clear single purpose is depth. Generality across unrelated purposes is sprawl.

The mistake in the other direction is speculative generality: parameters or extension points for futures that never arrive. "Somewhat" is the operative word. Cover today's needs and one or two near-future variants you can name. Stop there.

The interface-segregation principle is the floor here: no caller should depend on parts of the surface it does not use. A consumer that needs one method gets an interface with one method. On a backend service, `references/backend-apis.md` works this through.

Each parameter forces every caller to answer a question. Before adding one, check whether the module can compute or decide the value itself. A default lowers the burden and keeps the coupling, because the caller still reads the default to know the behavior. Prefer a computed value or a narrower operation over a configurable one.

## The procedure

### 1. Decompose by knowledge

Before sketching, state in one sentence what this module encapsulates. "How user sessions are stored and validated." "How the cart total is computed." A description that is an order of steps is temporal decomposition. "First parse, then validate, then write." That produces shallow modules and leaks one decision across many. Re-slice around the knowledge each module owns.

### 2. Triage: decide how much this interface is worth

Most interfaces don't earn a full design loop. Spend effort in proportion to how expensive the interface is to get wrong, judged from signals already in front of you:

- **Consequential**: exported or public, has or will have several callers, crosses a module/service/process boundary, is a shipped component's prop surface, or encodes a contract costly to change later (persisted format, published API, anything other teams build on).
- **Routine**: private, one caller, changed easily in one place, thin helper.

Routine interfaces take the cheap path in step 4. Reserve the full loop for consequential ones.

### 3. The comment test

For consequential or exported interfaces, write the interface comment before the body. For routine private helpers, run the same test mentally and leave no comment when the surrounding code already makes the contract obvious. A candidate passes when its complete contract satisfies all of:

- Four sentences or fewer for the whole entry point.
- Zero references to internal data structures, algorithms, or named internal steps.
- No words describing call order or protocol ("first", "then", "after", "you must call X before Y").
- A competent caller could use it correctly from the comment alone, including the common error cases.

This bar is checkable by reading. A vague bar collapses into taste, and this one does not.

The comment test applies to parameter objects too. A short entry-point comment that stays short only because a query or command object absorbs the complexity is not a pass. Run the same test on that object's contract. When the contract crosses a serialization boundary, what survives that crossing is part of the contract. The comment carries it: no functions, no live references, no cycles.

**For consequential interfaces, write the comment before the body.** The comment is a design tool — the cheapest way to find out the abstraction is wrong. Writing the body first traps you in the structure of whatever you wrote. Writing the comment first lets you reject a bad shape while it's still text.

### 4. Default to the cheap path; escalate only when it matters

For a routine interface: write one design, run the comment test once, ship it if it passes. One design, one check, no second candidate. This is the path almost every interface takes, and it adds almost no cost beyond the comment you owed anyway.

Escalate to the **design-it-twice loop** when the interface is consequential. Escalate too when a routine interface's first comment fails, because that failure means the abstraction is wrong and earns one more try.

1. Write one candidate: signatures plus interface comments, bodies empty, describing what and not how.
2. Run the comment test.
3. If it fails, name the exact failure ("the comment had to describe the retry buffer"). That named flaw seeds the next candidate — a structurally different decomposition that removes that specific problem. A rename does not count.
4. Stop as soon as one candidate passes for a routine interface, two pass for a consequential one, or you reach three candidates total. Three is a hard ceiling.

If the ceiling is hit with nothing passing, hand the strongest candidate to the human with the precise blocker named. Spinning past the ceiling burns quota without converging.

### 5. Resolve a real tie

A second independent call is the one expensive move here, so gate it hard. Make it only when the interface is consequential and two or more candidates passed. For a routine interface, or when only one passed, take the first passing candidate.

When the gate is met and an independent review tool is available, use it as a critique surface. Send it the surviving signatures and interface comments only, with no implementations and no hint of your preference. Send the comment-test predicate too, and this rubric in priority order: common-case caller burden, generality, efficiency, then depth without over-hiding (step 7). Ask for one verdict: the chosen candidate, a one-line reason per rubric item, and any over-hiding risk. Treat the verdict as evidence you weigh. Choose deliberately, and fix a real over-hiding risk before writing any body.

If the human rejects all candidates, treat their stated reason as one new flaw-seed and generate exactly one more directed candidate, then stop. A rejection is a redirect that costs you one directed candidate.

### 6. The comment test is also the redesign trigger

Apply the same test whenever you later change a public interface, before touching code. Whenever you can't write the comment short, redesign. This is the loop's maintenance mode.

### 7. Guardrail: deep, but expose what callers need

Hiding complexity is the goal, with one hard limit. Information the caller needs must stay in the interface. Tunable performance config, errors the caller must handle, durability or visibility guarantees, ordering the caller depends on. Hiding any of these to make the interface look smaller is its own defect, and it produces modules nobody can use correctly.

Apply progressive disclosure to the signature. The common case stays on the primary surface, required and simple. Advanced or rarely needed config moves to a separate optional surface, an options object with defaults that work. A caller doing the ordinary thing reads only the first two or three parameters.

Where a special case can be removed by redesigning semantics so it does not arise, redesign it away and leave it out of the interface. An interface that accepts input from outside the program is a trust boundary: a request, a message, a deserialized payload. The module that owns the contract validates that input. The boundary owns the check.

The word "configuration" covers two things. A caller-facing parameter is the kind this skill tells you to minimize, meaning a function argument or a component prop. Deploy-varying config is separate: database URLs, credentials, log levels, pool sizes, timeouts that differ between environments. It belongs in one module that reads the environment, validates it at startup, and hands typed values to the rest of the code. A module that reads `process.env` for its own needs has taken a hidden dependency and leaked a decision that should live in one place. `references/runtime-config.md` has the detail.

### 8. Then implement

Only now write the bodies. If implementation reveals the abstraction was wrong, change the interface and its comment. That means a promise you cannot keep, or a parameter you did not need. Don't let the implementation quietly widen the contract.

## Brownfield Work

Before changing an existing callable surface, list its callers in the repo and the behavior each relies on. Mark every one updated or deliberately out of scope before calling the change done. If a cleaner interface would reduce caller burden, offer a migration path so call sites move over without silent breakage. Keep compatibility when the current surface is public, exported, persisted, or used across a service boundary unless the user approves the break. When the change creates or clarifies a public contract in a meaningful module, offer an AGENTS.md update if none exists nearby.

## Red flags

Run this list against the finished interface before calling it done. A match against any item calls for a redesign now, while it is still cheap to change.

- **Shallow module**: interface nearly as complex as the implementation.
- **Overexposure**: callers must understand rarely-used features to use common ones.
- **Information leakage**: one design decision shows up in several modules; prop drilling; key schemas duplicated across endpoints.
- **Temporal decomposition**: structure follows execution order, when it should follow the knowledge each module owns.
- **Pass-through method**: an entry point that only forwards to another with a near-identical signature.
- **Implementation in the interface comment**: the comment describes internals.
- **Hard to describe**: a complete comment for the entry point has to be long.
- **Accessors as the public surface**: an interface that is mostly per-field get/set exposes the data layout with extra syntax — the same shape as the implementation, definitionally shallow. Replace with operations that name intent (`reserve`, `markPaid`) and enforce invariants. Keep the representation hidden behind the module boundary where the language allows. The exception is a record that exists deliberately as plain data, with the behavior over it owned by another module. There the data is the contract, and depth lives in the module that owns the behavior.
- **One method per caller-shape**: a finder/handler/query method per combination of conditions, growing without bound. Compress with a value object or query parameter that lets one method cover the cluster.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy interface adopted on the belief that patterns are good, while the problem does not have the structure the pattern solves. Patterns earn their place by removing complexity.

## References

Open one. Read the stack file for the surface you are designing, and open a subject file only when that subject is the contract:

- `references/examples.md` — Foundational cases (rate limiter, UserCard, file upload).
- `references/runtime-config.md` — where deploy config enters, validation at boot, injecting typed values, the composition root.
- `references/web.md` — React, Solid, Svelte. Hook return shapes, component prop contracts, store slice interfaces.
- `references/mobile.md` — React Native. Native bridge interfaces, navigation prop contracts, storage module shapes.
- `references/backend-apis.md` — Java/Spring, Go, TypeScript backends. Service interfaces, REST/gRPC contracts.
- `references/databases.md` — Repository interface, query interface, transaction interface.
- `references/caching.md` — Cache get-or-load contract, invalidation surface.
