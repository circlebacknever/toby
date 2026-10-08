---
name: toby-swd-interfaces
description: >-
  Contains Toby's procedure for designing a callable surface before its body.
  Entry skills open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Interfaces

The interface is everything a caller must know to use a module correctly. The interface includes the signature and the rules that only a comment can state. Those rules cover behavior, side effects, required call order, and errors. Keep the interface much smaller than the functionality behind it. A deep module hides a lot of work behind a small interface. A shallow module has an interface about as complex as the work behind it.

When two modules talk by sending messages, such as over a queue or between processes, the message format plays the role of the signature. That format includes the request and response types, which values survive serialization, and the delivery guarantees.

Write the interface and its comment before the body. When you cannot write a short comment that mentions no internals, redesign the interface before you write any code behind it.

## Make interfaces somewhat general-purpose

Build the functionality for current needs, and make the interface serve more than one use. When a signature fits only one caller, whoever writes the next caller has to change the signature. Ask these four questions early:

- **What is the simplest interface that covers all your current needs?** Use fewer methods that each handle more cases, so the interface stays small as needs grow.
- **In how many situations will this method be used?** A method serving one call site is a candidate for inlining or for redesign into something that serves more.
- **Is this API easy to use for the common case today?** A `find(query)` is better than thirty `findByXAndYAndZ` only if `find(...)` is also easy to call for the common case.
- **Does it keep one purpose?** An interface that serves unrelated purposes has become too general.

Do not add parameters or extension points for needs nobody has named. Cover today's needs plus one or two specific changes you expect soon and can describe.

To follow the interface segregation principle, each caller declares its own interface type that lists only the methods it calls. One class or module provides all of those methods, so that class or module satisfies every caller's type. `references/backend-apis.md` shows an example in Go under "Go consumer interface".

Each parameter is one more value that every caller has to choose. Before adding one, check whether the module can compute the value itself, and whether any caller could pick a better value. Even a parameter with a default makes the person writing the call read it to know what the call does. So prefer a value the module computes, or a separate operation that does less, over a setting the caller passes.

## The procedure

### 1. Split by what each module hides

State in one sentence what the module hides, such as "how user sessions are stored and validated". When that sentence lists steps in time order, the module is split in the wrong place. Follow check 1 in `toby-swd-modules` to fix the split.

### 2. Classify by cost

Classify the interface by how costly a bad design would be, based on the code and the request in front of you:

- **Consequential**: the interface is exported or public, has or will have several callers, or is called across a module, service, or process boundary. The interface is also consequential when it is a released component's props, or when it fixes something costly to change later. Examples are a stored data format, a published API, or anything other teams build on.
- **Routine**: the interface is a private, thin helper with one caller, and you can change it in one place.

### 3. The comment test

For consequential or exported interfaces, write the interface comment before the body. For routine private helpers, run the same test mentally and leave no comment when the surrounding code already makes the contract obvious. A proposed interface passes when its full comment meets all of these conditions:

- The comment is four sentences or fewer, plus one more sentence for each argument whose units, allowed range, or empty value the type does not already show.
- The comment mentions no internal data structure, algorithm, or internal step.
- No words describing call order or protocol ("first", "then", "after", "you must call X before Y").
- A competent caller could use it correctly from the comment alone, including the common error cases.

Also run the test on any query or command object that an entry point takes, such as a public function, an endpoint, or an RPC. A short comment on the entry point can hide a complicated parameter object. Some of these objects cross a serialization boundary, such as a network call, a worker or process boundary, a native bridge, or disk. The comment for such an object states that the object contains no functions, no references to live objects, and no circular references.

### 4. Start with one design, and when to try more

For a routine interface, write one design, run the comment test once, and ship the design if it passes. Do not write a second design.

The steps in `references/design-it-twice.md` compare two or three designs. Use them when the interface is consequential, or when a routine interface's first comment fails the test.

### 5. Keep modules deep, but expose what callers need

Hide complexity, but keep any information the caller needs in the interface. That information includes performance settings the caller may tune and errors the caller must handle. The information also includes promises about when data is saved or becomes visible to other readers. Any order of results or events that the caller depends on belongs in the interface too. Hiding any of these is a defect, because callers then cannot use the module correctly.

Keep the common case in the main signature, required and simple. Move advanced or rarely needed config to an options object with defaults that work. A caller doing the ordinary thing reads only the first two or three parameters.

Some input comes from outside the program, such as a request, a message, or a deserialized payload. The module that defines the contract for that input parses it into a typed value. Later code takes that type and repeats no check.

Settings that change between deployments, such as database URLs, credentials, and connection pool sizes, are handled differently from function parameters. One module reads these settings from the environment, validates them at startup, and passes typed values to the rest of the code. Open `references/runtime-config.md` when a change reads an environment variable or adds deploy config.

### 6. Then implement

When the implementation cannot provide a guarantee the interface states, or never uses a parameter the interface requires, change the interface and its comment. Do not let the code accept or promise more than the interface comment states unless you update the comment to match.

## Brownfield Work

Before changing an existing interface, run the comment test on the new version. Then list its callers in the repo and the behavior each relies on. Mark every one updated or deliberately out of scope before calling the change done. If a simpler interface would mean less work for callers, propose a migration path. The path moves each call site over without breaking any of them unnoticed. Keep compatibility when the current surface is public, exported, persisted, or used across a service boundary unless the user approves the break.

## Red flags

Run this list against the finished interface before calling it done. If the interface matches any item, redesign it now, while it is still cheap to change.

- **Overexposure**: callers must understand rarely-used features to use common ones.
- **Comment fails the test**: a complete comment for the entry point is long or describes internals.
- **Accessors as the public surface**: an interface that is mostly per-field get/set exposes the data layout with extra syntax. Replace the getters and setters with methods named for what the caller wants done, such as `reserve` or `markPaid`, that check the rules the data must always satisfy. Keep the representation hidden behind the module boundary where the language allows. The exception is a record that exists deliberately as plain data, with the behavior over it handled by another module. In that case the fields are the interface, and the module that works on the data holds the logic.
- **One method per caller variation**: each combination of conditions gets its own find, handler, or query method. The number of methods keeps growing. Replace them with one method that takes a query object or parameter describing the conditions.
- **Fields valid only in some combinations**: a comment has to list which combinations of optional fields, such as `data`, `error`, and `loading`, can occur. Where the language has union or sealed types, replace the fields with one variant per state.

Some problems come from how code is split into modules. These are a shallow module, information leakage, temporal decomposition, a pass-through method or variable, and a design pattern used where it does not fit. Information leakage means one detail that several modules depend on. Temporal decomposition means modules split by the order their steps run. Check each problem against the matching red flag in `toby-swd-modules`.

## References

Read the reference file for the platform you are working in, such as web, mobile, or backend. Open a topic file, such as caching or runtime config, only when the interface you are designing is about that topic.

- `references/examples.md` has a rate limiter, a `UserCard`, and a file upload redesigned through the comment test. Open it when a first comment fails.
- `references/design-it-twice.md` has the steps for comparing designs, how to choose between two designs that both pass, and how to ask a separate reviewer for a verdict. Open it for a consequential interface or a failed first comment.
- `references/runtime-config.md` covers where deploy config enters, validation at startup, injecting typed values, and the composition root.
- `references/web.md` covers React, Solid, and Svelte hook return types, component prop contracts, and headless hooks.
- `references/mobile.md` covers React Native native bridges, route params, storage modules, and screen data hooks.
- `references/backend-apis.md` covers REST search endpoints, service commands and results, Go consumer interfaces, and gRPC update messages.
- `references/databases.md` covers repository, query object, transaction, and migration interfaces.
- `references/caching.md` covers the cache get-or-load contract, typed keys, and outage behavior.
