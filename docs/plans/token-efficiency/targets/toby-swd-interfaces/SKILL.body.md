# Toby SWD Interfaces

The interface is everything a caller must know to use a module correctly. It includes the signature and the informal contract that only comments can state, which covers behavior, side effects, ordering constraints, and errors. Keep the interface much smaller than the functionality behind it. For a message-channel boundary, the "signature" is the message contract: the request and response types, what is preserved through serialization, and the delivery guarantees.

Write the interface and its comment before the body. When you cannot write a short comment that mentions no internals, redesign the interface while it is still text.

## Bias toward somewhat general-purpose

Build the functionality for current needs, and make the interface serve more than one use. A signature written for one caller forces the next caller to widen it. Ask these four questions early:

- **What is the simplest interface that covers all your current needs?** Use fewer methods, each with broader semantics, so the interface stays small as needs grow.
- **In how many situations will this method be used?** A method serving one call site is a candidate for inlining or for redesign into something that serves more.
- **Is this API easy to use for the common case today?** A `find(query)` is better than thirty `findByXAndYAndZ` only if `find(...)` is also easy to call for the common case.
- **Does it keep one purpose?** An interface that serves unrelated purposes has become too general.

Do not add parameters or extension points for needs nobody has named. Cover today's needs and one or two near-future variants you can name.

Under interface segregation, each caller declares a type with only the methods it calls, and one deep provider implements every such type. `references/backend-apis.md` shows it in Go under "Go consumer interface".

Each parameter forces every caller to answer a question. Before adding one, check whether the module can compute the value itself, and whether any caller could pick a better value. A default still makes the caller read it to know the behavior, so prefer a computed value or a narrower operation over a configurable one.

## The procedure

### 1. Decompose by knowledge

State in one sentence what the module hides, such as "how user sessions are stored and validated". When that sentence is a sequence of steps, the boundary is wrong, and `toby-swd-modules` check 1 applies.

### 2. Triage

Classify the interface by what getting it wrong would cost, judged from what you can already see:

- **Consequential**: exported or public, has or will have several callers, crosses a module/service/process boundary, is a shipped component's props, or encodes a contract costly to change later (persisted format, published API, anything other teams build on).
- **Routine**: private, one caller, changed easily in one place, thin helper.

### 3. The comment test

For consequential or exported interfaces, write the interface comment before the body. For routine private helpers, run the same test mentally and leave no comment when the surrounding code already makes the contract obvious. A candidate passes when its complete contract meets all of these conditions:

- Four sentences or fewer, plus one per argument whose units, bounds, or empty case the type cannot state.
- Zero references to internal data structures, algorithms, or named internal steps.
- No words describing call order or protocol ("first", "then", "after", "you must call X before Y").
- A competent caller could use it correctly from the comment alone, including the common error cases.

Run the test on any query or command object the entry point takes, because a short entry-point comment can hide a complex parameter object. When that object crosses a serialization boundary, its comment states that it contains no functions, live references, or cycles.

### 4. Cheap path first, and when to escalate

For a routine interface, write one design, run the comment test once, and ship the design if it passes. Do not write a second candidate.

Escalate to the **design-it-twice loop** when the interface is consequential or a routine interface's first comment fails.

1. Write one candidate as signatures plus interface comments with empty bodies, and describe what each one does without describing how.
2. Run the comment test.
3. If it fails, state what failed ("the comment had to describe the retry buffer"). Use that flaw to build the next candidate, which is a structurally different decomposition that removes that problem. A rename does not count.
4. Stop as soon as one candidate passes for a routine interface, two pass for a consequential one, or you reach three candidates total. Never write more than three candidates.

If you reach three candidates and none passes, give the strongest candidate to the user and say what blocks it.

### 5. Resolve a real tie

For a routine interface, take the first passing candidate. Rank two or more passing consequential candidates by common-case caller burden, then generality, then efficiency, then depth that hides nothing callers need. When an independent review tool is available, ask it first, the way `references/examples.md` describes under "Asking a critic".

If the user rejects all candidates, treat their stated reason as one new flaw. Generate exactly one more candidate that fixes that flaw, then stop.

### 6. Keep modules deep, but expose what callers need

Hide complexity, but keep any information the caller needs in the interface. That information includes tunable performance config, errors the caller must handle, durability or visibility guarantees, and ordering the caller depends on. Hiding any of these is a defect, because callers then cannot use the module correctly.

Keep the common case in the main signature, required and simple. Move advanced or rarely needed config to an options object with defaults that work. A caller doing the ordinary thing reads only the first two or three parameters.

The module that defines a contract for outside input, such as a request, a message, or a deserialized payload, parses it into a typed value. Later code takes that type and repeats no check.

Deploy-varying config, such as database URLs, credentials, and pool sizes, is a different kind from caller-facing parameters. One module reads it from the environment, validates it at startup, and passes typed values to the rest of the code. Open `references/runtime-config.md` when a change reads an environment variable or adds deploy config.

### 7. Then implement

When the implementation cannot provide a guarantee the interface states, or never uses a parameter the interface requires, change the interface and its comment. Don't widen the contract in the implementation without saying so.

## Brownfield Work

Before changing an existing callable surface, run the comment test on the changed contract. Then list its callers in the repo and the behavior each relies on. Mark every one updated or deliberately out of scope before calling the change done. If a simpler interface would reduce caller burden, offer a migration path so call sites move over without silent breakage. Keep compatibility when the current surface is public, exported, persisted, or used across a service boundary unless the user approves the break.

## Red flags

Run this list against the finished interface before calling it done. If the interface matches any item, redesign it now, while it is still cheap to change.

- **Overexposure**: callers must understand rarely-used features to use common ones.
- **Comment fails the test**: a complete comment for the entry point is long or describes internals.
- **Accessors as the public surface**: an interface that is mostly per-field get/set exposes the data layout with extra syntax. Replace it with operations that name intent (`reserve`, `markPaid`) and enforce invariants. Keep the representation hidden behind the module boundary where the language allows. The exception is a record that exists deliberately as plain data, with the behavior over it handled by another module. In that case the data is the contract, and the module that handles the behavior provides the depth.
- **One method per caller variation**: a finder/handler/query method per combination of conditions, growing without bound. Replace the set with a value object or query parameter that lets one method replace the whole set.
- **Fields valid only in some combinations**: a comment has to list which combinations of optional fields, such as `data`, `error`, and `loading`, can occur. Where the language has union or sealed types, replace the fields with one variant per state.

A shallow module, information leakage, temporal decomposition, a pass-through method or variable, or a design pattern forced onto the problem is a module-structure problem. Run the matching red flag in `toby-swd-modules`.

## References

Read the stack file for the interface you are designing, and open a subject file only when that subject is the contract.

- `references/examples.md` has a rate limiter, a `UserCard`, and a file upload redesigned through the comment test, and how to ask a critic. Open it when a first comment fails or two candidates tie.
- `references/runtime-config.md` covers where deploy config enters, validation at startup, injecting typed values, and the composition root.
- `references/web.md` covers React, Solid, and Svelte hook return types, component prop contracts, and headless hooks.
- `references/mobile.md` covers React Native native bridges, route params, storage modules, and screen data hooks.
- `references/backend-apis.md` covers REST search endpoints, service commands and results, Go consumer interfaces, and gRPC update messages.
- `references/databases.md` covers repository, query object, transaction, and migration interfaces.
- `references/caching.md` covers the cache get-or-load contract, typed keys, and outage behavior.
