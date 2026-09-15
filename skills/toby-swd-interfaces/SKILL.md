---
name: toby-swd-interfaces
description: >-
  Design the callable surface before the implementation. Use it when a task
  adds or changes a function, method, class, component props, hook return
  type, composable, REST endpoint, gRPC service, repository, cache interface,
  or message contract. It covers the comment test, the parameter
  budget, and the general-purpose bias. Skip it when the question is where
  the code should go, which `toby-swd-modules` covers, and skip it when
  adding a field beside an identical one already in that file.
---

# Toby SWD Interfaces

The interface is everything a caller must know to use a module correctly. It includes the signature and the informal contract that only comments can state, which covers behavior, side effects, ordering constraints, and errors. The interface is a cost the module imposes on the rest of the system, because callers must learn it. The implementation provides the module's benefit. Keep that cost much smaller than that benefit, so the module offers substantial functionality through a simple interface. For a message-channel boundary, the "signature" is the message contract: the request and response types, what is preserved through serialization, and the delivery guarantees.

Design the interface first, so you find a good interface before the implementation commits you to a bad one. The interface is also the earliest signal that the design is wrong. If you cannot write a short comment that names no internals, treat that failure as a bug report. You get that report while the abstraction exists only as text.

Everything below applies identically to every interface in the stack:

- a class's public methods
- a function's signature
- a service's endpoints
- a component's props
- a hook's return type
- a repository's query methods
- a cache's get-or-load contract
- a message contract across a process boundary

## Bias toward somewhat general-purpose

Make this framing decision before the procedure, because it constrains every step after it. The functionality of a module is built for your current needs, but the interface should support more than one use. A method signature written for exactly one caller forces the next caller to widen it before they can use it.

Ask these four questions early:

- **What is the simplest interface that covers all your current needs?** Use fewer methods, each with broader semantics, so the interface stays small as needs grow.
- **In how many situations will this method be used?** A method serving one call site is a candidate for inlining or for redesign into something that serves more.
- **Is this API easy to use for the common case today?** A general-purpose interface fails when it makes the common case hard to do. A `find(query)` is better than thirty `findByXAndYAndZ` only if `find(...)` is also easy to call for the common case.
- **Will this generalize without becoming a god interface?** A general interface stays deep when it keeps one clear purpose. It becomes sprawling when it serves unrelated purposes.

The mistake in the other direction is speculative generality, which adds parameters or extension points for future needs that never come. The word "somewhat" in the heading sets the limit. Cover today's needs and one or two near-future variants you can name, and stop there.

The interface-segregation principle sets the minimum rule here: a caller should depend only on the parts of the interface it uses. A consumer that needs one method gets an interface with one method. For a backend service, `references/backend-apis.md` shows how to apply this rule.

Each parameter forces every caller to answer a question. Before adding one, check whether the module can compute or set the value itself. A default lowers the burden, but the coupling stays. The caller still reads the default to know the behavior. Prefer a computed value or a narrower operation over a configurable one.

## The procedure

### 1. Decompose by knowledge

State what this module encapsulates in one sentence, such as "how user sessions are stored and validated" or "how the cart total is computed". A description written as a sequence of steps, such as "first parse, then validate, then write", is temporal decomposition. Temporal decomposition produces shallow modules and spreads one decision across many modules. Redraw the module boundaries around the knowledge each module contains.

### 2. Triage

Most interfaces do not need a full design loop. Spend effort in proportion to the cost of getting the interface wrong, and judge that cost from what you can already see:

- **Consequential**: exported or public, has or will have several callers, crosses a module/service/process boundary, is a shipped component's props, or encodes a contract costly to change later (persisted format, published API, anything other teams build on).
- **Routine**: private, one caller, changed easily in one place, thin helper.

Use the cheap path in step 4 for routine interfaces. Reserve the full loop for consequential ones.

### 3. The comment test

For consequential or exported interfaces, write the interface comment before the body. For routine private helpers, run the same test mentally and leave no comment when the surrounding code already makes the contract obvious. A candidate passes when its complete contract meets all of these conditions:

- Four sentences or fewer for the whole entry point.
- Zero references to internal data structures, algorithms, or named internal steps.
- No words describing call order or protocol ("first", "then", "after", "you must call X before Y").
- A competent caller could use it correctly from the comment alone, including the common error cases.

You can check these conditions by reading the comment. A vague standard becomes a matter of taste, but these conditions do not depend on taste.

The comment test applies to parameter objects too. If an entry-point comment stays short only because a query or command object holds the complexity, the short comment alone does not pass. Run the same test on that object's contract. When the contract crosses a serialization boundary, what is preserved across that boundary is part of the contract. The comment states that the object contains no functions, no live references, and no cycles.

 The comment is a design tool, and it is the cheapest way to find out the abstraction is wrong. If you write the body first, you commit to the structure of whatever you wrote. Writing the comment first lets you reject a bad design while it's still text.

### 4. Cheap path first, and when to escalate

For a routine interface, write one design, run the comment test once, and ship the design if it passes. Do not write a second candidate. You use this cheap path for almost every interface, and it adds almost nothing beyond the comment you had to write anyway.

Escalate to the **design-it-twice loop** when the interface is consequential. Also escalate when a routine interface's first comment fails. That failure means the abstraction is wrong, which justifies one more try.

1. Write one candidate as signatures plus interface comments with empty bodies, and describe what each one does without describing how.
2. Run the comment test.
3. If it fails, name the exact failure ("the comment had to describe the retry buffer"). Use that named flaw to build the next candidate, which is a structurally different decomposition that removes that problem. A rename does not count.
4. Stop as soon as one candidate passes for a routine interface, two pass for a consequential one, or you reach three candidates total. Never write more than three candidates.

If you reach three candidates and none passes, give the strongest candidate to the human and name the exact blocker. Writing more than three candidates uses quota without reaching a passing candidate.

### 5. Resolve a real tie

Spend the one expensive step, a second independent call, only when the interface is consequential and two or more candidates passed. For a routine interface, or when only one passed, take the first passing candidate.

When both conditions hold and an independent review tool is available, use the tool as a critic. Send it the passing signatures and interface comments only, with no implementations and no hint of your preference. Send the comment-test predicate too, and this rubric in priority order: common-case caller burden, generality, efficiency, then depth without over-hiding (step 7). Ask for one verdict: the chosen candidate, a one-line reason per rubric item, and any over-hiding risk. Treat the verdict as evidence you weigh. Choose deliberately, and fix a real over-hiding risk before writing any body.

If the human rejects all candidates, treat their stated reason as one new named flaw. Generate exactly one more candidate that fixes that flaw, then stop.

### 6. When the comment test shows that a redesign is needed

Apply the same test whenever you later change a public interface, before touching code. Whenever you cannot write a short comment, redesign the interface. This step applies the design loop to later changes.

### 7. Keep modules deep, but expose what callers need

Hide complexity, but keep any information the caller needs in the interface. That information includes tunable performance config, errors the caller must handle, durability or visibility guarantees, and ordering the caller depends on. If you hide any of these to make the interface look smaller, you create a defect, because callers cannot use the module correctly.

Apply progressive disclosure to the signature. The common case stays in the main signature, required and simple. Move advanced or rarely needed config to a separate options object with defaults that work. A caller doing the ordinary thing reads only the first two or three parameters.

Where a special case can be removed by redesigning semantics so it does not arise, redesign it away and leave it out of the interface. An interface that accepts input from outside the program, such as a request, a message, or a deserialized payload, is a trust boundary. The module that defines the contract validates that input at the boundary.

The word "configuration" covers caller-facing parameters and deploy-varying config. A caller-facing parameter, meaning a function argument or a component prop, is the kind this skill tells you to minimize. Deploy-varying config is a separate kind, such as database URLs, credentials, log levels, pool sizes, and timeouts that differ between environments. It belongs in one module that reads the environment, validates it at startup, and hands typed values to the rest of the code.

A module that reads `process.env` for its own needs has taken a hidden dependency. It has also leaked a decision that belongs in one place. `references/runtime-config.md` has the detail.

### 8. Then implement

Only now write the bodies. If the implementation shows the abstraction was wrong, change the interface and its comment. The implementation shows it when the interface guarantees something you cannot provide or requires a parameter you did not need. Don't widen the contract in the implementation without saying so.

## Brownfield Work

Before changing an existing callable surface, list its callers in the repo and the behavior each relies on. Mark every one updated or deliberately out of scope before calling the change done. If a simpler interface would reduce caller burden, offer a migration path so call sites move over without silent breakage. Keep compatibility when the current surface is public, exported, persisted, or used across a service boundary unless the user approves the break. When the change creates or clarifies a public contract in a meaningful module, offer an AGENTS.md update if none exists nearby.

## Red flags

Run this list against the finished interface before calling it done. If the interface matches any item, redesign it now, while it is still cheap to change.

- **Shallow module**: interface nearly as complex as the implementation.
- **Overexposure**: callers must understand rarely-used features to use common ones.
- **Information leakage**: one design decision shows up in several modules, as in prop drilling or key schemas duplicated across endpoints.
- **Temporal decomposition**: structure follows execution order, when it should follow the knowledge each module contains.
- **Pass-through method**: an entry point that only forwards to another with a near-identical signature.
- **Implementation in the interface comment**: the comment describes internals.
- **Hard to describe**: a complete comment for the entry point has to be long.
- **Accessors as the public surface**: an interface that is mostly per-field get/set exposes the data layout with extra syntax. It costs a caller as much as the implementation would, which makes it shallow by definition. Replace it with operations that name intent (`reserve`, `markPaid`) and enforce invariants. Keep the representation hidden behind the module boundary where the language allows. The exception is a record that exists deliberately as plain data, with the behavior over it handled by another module. In that case the data is the contract, and the module that handles the behavior provides the depth.
- **One method per caller variation**: a finder/handler/query method per combination of conditions, growing without bound. Replace the set with a value object or query parameter that lets one method replace the whole set.
- **Pattern forced onto the problem**: a Visitor, Factory, Observer, or Strategy interface adopted on the belief that patterns are good, while the problem does not have the structure the pattern solves. A pattern is worth adding only when it removes complexity.

## References

Open one of these references. Read the stack file for the interface you are designing, and open a subject file only when that subject is the contract:

- `references/examples.md` — Foundational cases (rate limiter, UserCard, file upload).
- `references/runtime-config.md` — where deploy config enters, validation at boot, injecting typed values, the composition root.
- `references/web.md` — React, Solid, Svelte. Hook return types, component prop contracts, store slice interfaces.
- `references/mobile.md` — React Native. Native bridge interfaces, navigation prop contracts, storage module interfaces.
- `references/backend-apis.md` — Java/Spring, Go, TypeScript backends. Service interfaces, REST/gRPC contracts.
- `references/databases.md` — Repository interface, query interface, transaction interface.
- `references/caching.md` — Cache get-or-load contract, invalidation methods.
