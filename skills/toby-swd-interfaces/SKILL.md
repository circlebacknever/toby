---
name: toby-swd-interfaces
description: >-
  Design the public contract before the implementation. Use this skill when a
  task adds or changes a function, method, class, component, hook, composable,
  REST endpoint, gRPC service, repository, cache, or any other callable surface.
  The interface is the cost the module imposes on the system, and a bad one
  compounds across every caller forever.
---

# Toby SWD Interfaces

The interface is everything a caller must know to use a module correctly: the signature plus the informal contract (behavior, side effects, ordering constraints, errors) that only comments can carry. The interface is the cost the module imposes on the rest of the system; the implementation is the benefit. You want that cost much smaller than that benefit — a simple interface over substantial functionality.

Interface-first design exists to find that interface before implementation locks in a bad one, and to use the interface itself as the earliest possible signal that the design is wrong. A comment you can't write short and internals-free is the cheapest bug report you will ever get. It shows the abstraction is broken while it's still only text.

This applies identically across the stack: a class's public methods, a function's signature, a service's endpoints, a React component's props, a hook's return shape, a repository's query methods, a cache's get-or-load surface — all are interfaces, and everything below applies to each.

## Bias toward somewhat general-purpose

Before the procedure, one framing decision that shapes everything downstream. The functionality of a module reflects your current needs, but the interface should support more than one. A method signature shaped exactly to one caller produces a one-call-shaped hole the next caller cannot use without widening it.

Four questions, asked early:

- **What is the simplest interface that covers all your current needs?** Fewer methods with broader semantics, not more methods with narrower ones.
- **In how many situations will this method be used?** A method serving one call site is a candidate for inlining or for redesign into something that serves more.
- **Is this API easy to use for the common case today?** General-purpose interfaces fail when they make the easy thing hard. A `find(query)` is better than thirty `findByXAndYAndZ` only if `find(...)` is also easy to call for the common case.
- **Will this generalize without becoming a god interface?** Generality with a clear single purpose is depth. Generality across unrelated purposes is sprawl.

The mistake in the other direction is speculative generality — parameters or extension points for futures that never arrive. "Somewhat" is the operative word. Cover today's needs and one or two near-future variants you can name, not every imaginable one.

## The procedure

### 1. Decompose by knowledge, not sequence

Before sketching anything, state in one sentence what design decision or piece of knowledge this module exists to encapsulate ("how user sessions are stored and validated", "how the cart total is computed"). If the natural description is an order of steps ("first parse, then validate, then write"), you're doing temporal decomposition. That produces shallow modules and leaks one decision across many. Re-slice around knowledge each module owns.

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

This bar is checkable by reading. A vague bar collapses into taste; this one doesn't.

**For consequential interfaces, write the comment before the body.** The comment is not decoration. It is a design tool — the cheapest way to find out the abstraction is wrong. Writing the body first traps you in the structure of whatever you wrote; writing the comment first lets you reject a bad shape while it's still text.

### 4. Default to the cheap path; escalate only when it matters

For a routine interface: write one design, run the comment test once, ship it if it passes. One design, one check, no second candidate. This is the path almost every interface takes, and it adds almost no cost beyond the comment you owed anyway.

Escalate to the **design-it-twice loop** only when the interface is consequential, or when a routine interface's first comment fails (the failure means the abstraction is wrong and earns one more try):

1. Write one candidate: signatures plus interface comments, bodies empty, describing what and not how.
2. Run the comment test.
3. If it fails, name the exact failure ("the comment had to describe the retry buffer"). That named flaw seeds the next candidate — a structurally different decomposition that removes that specific problem, not a rename.
4. Stop as soon as one candidate passes for a routine interface, two pass for a consequential one, or you reach three candidates total. Three is a hard ceiling.

If the ceiling is hit with nothing passing, hand the strongest candidate to the human with the precise blocker named. Spinning past the ceiling burns quota without converging.

### 5. Resolve a real tie

A second independent call is the one expensive move here; gate it hard. Make it only when the interface is consequential and two or more candidates passed. For a routine interface, or when only one passed, take the first passing candidate.

When the gate is met and an independent review tool is available, use it as a critique surface. Send it: surviving signatures and interface comments only (no implementations, no hint of your preference), the comment-test predicate, and this rubric in priority order — common-case caller burden first, then generality, then efficiency, then depth without over-hiding (step 7). Ask for one verdict: the chosen candidate, a one-line reason per rubric item, and any over-hiding risk. Treat the verdict as evidence, not authority. Choose deliberately, and fix a real over-hiding risk before writing any body.

If the human rejects all candidates, treat their stated reason as one new flaw-seed and generate exactly one more directed candidate, then stop. A rejection is a redirect, not a reason to restart the loop.

### 6. The comment test is also the redesign trigger

Apply the same test whenever you later change a public interface, before touching code. A comment you can't write short is always the signal to redesign. This is the loop's maintenance mode.

### 7. Guardrail: deep, but expose what callers actually need

Hiding complexity is the goal, with a hard limit: information the caller truly needs must stay in the interface. Tunable performance config, errors the caller must handle, durability or visibility guarantees, ordering the caller depends on — hiding these to make the interface look smaller is its own defect and produces modules that can't be used correctly. Where a special case can be removed by redesigning semantics so it does not arise, do that instead of exposing it.

### 8. Then implement

Only now write the bodies. If implementation reveals the abstraction was wrong — a promise you can't keep cleanly, a parameter you didn't need — change the interface and its comment. Don't let the implementation quietly widen the contract.

## Brownfield Work

Before changing an existing callable surface, inspect current callers and the behavior they rely on. If a cleaner interface would reduce caller burden, offer a migration path instead of silently breaking call sites. Keep compatibility when the current surface is public, exported, persisted, or used across a service boundary unless the user approves the break. When the change creates or clarifies a public contract in a meaningful module, offer an AGENTS.md update if none exists nearby.

## Red flags

- **Shallow module**: interface nearly as complex as the implementation.
- **Overexposure**: callers must understand rarely-used features to use common ones.
- **Information leakage**: one design decision shows up in several modules; prop drilling; key schemas duplicated across endpoints.
- **Temporal decomposition**: structure follows execution order, not knowledge.
- **Pass-through method**: an entry point that only forwards to another with a near-identical signature.
- **Implementation in the interface comment**: the comment describes internals.
- **Hard to describe**: a complete comment for the entry point has to be long.
- **Getters and setters as the public surface**: a class whose interface is mostly `getFoo`/`setFoo` has an interface the same shape as its implementation — definitionally shallow. Replace with methods that name intent (`reserve()`, `markPaid()`) and enforce invariants; keep fields private.
- **One method per caller-shape**: a finder/handler/query method per combination of conditions, growing without bound. Compress with a value object or query parameter that lets one method cover the cluster.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy interface adopted because patterns are good, not because the problem has the shape the pattern solves.

## References

Worked examples organized by domain. Read the file matching the code you are in:

- `references/examples.md` — Foundational cases (rate limiter, UserCard, file upload).
- `references/web.md` — React, Solid, Svelte. Hook return shapes, component prop contracts, store slice interfaces.
- `references/mobile.md` — React Native. Native bridge interfaces, navigation prop contracts, storage module shapes.
- `references/backend-apis.md` — Java/Spring, Go, TypeScript backends. Service interfaces, REST/gRPC contracts.
- `references/databases.md` — Repository interface, query interface, transaction interface.
- `references/caching.md` — Cache get-or-load contract, invalidation surface.
