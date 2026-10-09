---
name: toby-swd-interfaces
description: >-
  Contains Toby's procedure for designing a callable surface before its body.
  Entry skills open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Interfaces

The interface is everything a caller must know to use a module correctly. The interface includes the signature and the rules that only a comment can state about behavior, side effects, required call order, and errors. Keep the interface much smaller than the functionality behind it.

Write the interface and its comment before the body. Open `references/serialization.md` when a message or a parameter object crosses a process, network, native-bridge, or disk boundary.

## The procedure

### Classify by cost

Classify the interface by how costly a bad design would be:

- **Consequential**: two or more modules call the interface, or a separately deployed client uses a format this code chooses. A second caller counts when the request, a ticket, or the code states one. Released component props also count, as does anything costly to change later, such as a stored data format, a published API, or code other teams build on.
- **Routine**: any other interface whose callers are all in this repo, such as a private helper, when you can update every caller in the same change. A view, job, or webhook handler whose signature the framework or provider sets is routine when only this app or that provider calls it.

### The comment test

An interface passes when its full comment meets all of these conditions:

- The comment is four sentences or fewer, plus one more sentence for each argument whose units, allowed range, or empty value the type does not already show.
- The comment mentions no internal data structure, algorithm, or internal step.
- The comment has no words that describe call order or protocol, such as "first", "then", "after", or "you must call X before Y".
- A competent caller could use it correctly from the comment alone, including the common error cases.

For a routine private helper, run the test mentally, and leave no comment when the surrounding code already makes the contract obvious.

Also run the test on any query or command object that an entry point takes, such as a public function, an endpoint, or an RPC.

### Start with one design, and when to try more

For a routine interface or an optional parameter or field added to an existing one, write one design and run the comment test once.

Open `references/design-it-twice.md` to compare two or three designs when a first comment fails the test. Also open it for a consequential interface that is new or changes what callers must pass, handle, or rely on. Answer the four questions in `references/general-purpose.md` for each design.

### Keep modules deep, but expose what callers need

Hide complexity, but keep in the interface what the caller needs, such as these items:

- performance settings the caller may tune
- errors the caller must handle
- when data is saved or becomes visible to other readers
- any order of results or events that the caller depends on

Keep the common case in the main signature, required and simple. Move rarely needed config to keyword arguments with defaults, or to an options object in a language without them. A caller doing the ordinary thing reads only the first two or three parameters.

The module that defines the contract for external input, such as a request, a message, or a deserialized payload, parses it into a typed value. Later code takes that type and repeats no check.

Open `toby-swd-twelve-factor`'s `references/config.md` when a change reads an environment variable or adds deploy config.

### Then implement

Update the interface and its comment when the code does less or more than they state, such as ignoring a required parameter.

## Brownfield Work

Before changing an existing interface, run the comment test on the new version. Then list its callers in the repo and the behavior each relies on. Mark every one updated or deliberately out of scope before calling the change done. When a simpler interface would save callers work, list it as a follow-up at file:line. Keep compatibility when the surface is public, exported, persisted, or used across a service boundary unless the user approves the break.

## Red flags

Fix the finished interface now when a part this change adds or changes matches an item below. List a match in an unchanged part as a follow-up at file:line. When the interface is new or changes what callers must pass, handle, or rely on, open `toby-swd-modules`. Run that skill's checks 1, 2, 4, and 8 and its "Pattern forced onto the problem" red flag on the module behind the interface.

- **Overexposure**: callers must understand rarely-used features to use common ones.
- **Accessors as the public surface**: an interface that is mostly per-field get/set exposes the data layout. Replace the getters and setters with methods named for what the caller wants done, such as `reserve` or `markPaid`, that check the rules the data must always satisfy. Keep the representation private where the language allows. The exception is a record kept as plain data on purpose, whose behavior another module handles.
- **Fields valid only in some combinations**: a comment has to list which combinations of optional fields, such as `data`, `error`, and `loading`, can occur. Where the language has union or sealed types, replace the fields with one variant per state.

## References

Open the platform file that matches the repo's framework, and a topic file, such as caching, only when the interface is about that topic.

- `references/examples.md` has a rate limiter, a `UserCard`, and a file upload redesigned through the comment test. Open it when a first comment fails.
- `references/web.md` covers React, Solid, and Svelte hook return types, component props, and headless hooks.
- `references/mobile.md` covers React Native native bridges, route params, storage modules, and screen data hooks.
- `references/backend-apis.md` covers REST search endpoints, service commands and results, Go consumer interfaces, and gRPC update messages.
- `references/databases.md` covers repository, query object, transaction, and migration interfaces.
- `references/caching.md` covers the cache get-or-load contract, typed keys, and outage behavior.
