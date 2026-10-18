---
name: toby-swd-interfaces
description: >-
  Contains Toby's procedure for designing a function or API signature before its
  body. Use it for a new or changed function signature, API, or exported type.
  Skip it for a field added beside fields of the same kind.
---

# Toby SWD Interfaces

An interface is everything a caller must know to use a module: its signature plus the behavior, side effects, invariants, and errors in its comment. Keep the interface much smaller than the work behind it, and write the signature and comment before the body.

Open `references/serialization.md` when a message or parameter object crosses a process, network, native-bridge, or disk boundary.

## The procedure

### Classify by cost

- **Cross-module or public**: two or more modules call it, a separately deployed client reads its format, or changing it later is costly.
- **Local**: all callers are in this repo and you can update them in the same diff, or a framework sets the signature.

### The comment test

An interface passes when its comment meets all four conditions:

- It runs four sentences or fewer, plus at most one sentence per argument whose units, bounds, or null meaning the type doesn't show.
- It mentions no internal data structure, algorithm, or implementation step.
- It uses no call-order words (`first`, `then`, `after`, `must call X before Y`).
- A caller can use the interface and handle its errors from the comment alone.

For a local private helper whose surrounding code makes the contract obvious, run the test mentally and omit the comment. Run the test on every public function, endpoint, RPC, and command or query object.

### Start with one design, and when to try more

For a local interface or a new optional parameter, write one design that passes the comment test. Open `references/design-it-twice.md` and `references/general-purpose.md` when the first comment fails the test, or when a cross-module or public interface is new or changes what callers pass or handle.

### Keep modules deep, and enforce invariants in types

Hide implementation details while exposing what callers need:

- performance settings callers tune, and errors callers handle differently (translate lower-level storage or transport errors at the boundary)
- durability and visibility guarantees, and any ordering of results or events callers rely on
- the common case in the first two or three parameters, with rare options in keyword arguments or an options object
- immutable domain types (such as `Money`, `Email`, or `DateRange`) that check bounds in their constructor, and external inputs parsed into typed values at the boundary
- automatic scope cleanup (`with`, `using`, `defer`, or a callback) whenever a module opens a file, stream, connection, lock, or timer

Open `toby-swd-twelve-factor`'s `references/config.md` when reading an environment variable or adding deploy config. Update the signature and comment whenever the body does more or less than they state.

## Brownfield Work

Before changing an existing interface, run the comment test on the new signature. List every caller in the repo with what it relies on, and update every caller (or mark it out of scope with approval). Keep backwards compatibility on public, exported, persisted, or cross-service contracts unless the user approves the break.

## Red flags

Fix any match in code this change adds or edits, and list matches in unchanged code as follow-ups at `file:line`. When a new or changed interface alters what callers pass, handle, or rely on, also check `toby-swd-modules`.

- **Overexposure**: callers must configure rarely used options just to run the common case.
- **Getters and setters for every field**: per-field accessors or returned mutable collections let callers bypass invariants. Replace them with behavior methods (`reserve`, `markPaid`) and read-only views or copies, except on plain data records at boundaries.
- **Fields valid only in some combinations**: optional fields such as `data`, `error`, and `loading` require a comment to explain which combinations are valid. Replace them with a tagged union that has one variant per valid state.

## References

Open the platform file matching the repo's stack, and a topic file only when relevant:

- `references/examples.md` shows a rate limiter, a `UserCard`, and a file upload redesigned with the comment test.
- `references/web.md` covers React, Solid, and Svelte hook return types, component props, and headless hooks.
- `references/mobile.md` covers React Native bridges, route params, storage modules, and screen hooks.
- `references/backend-apis.md` covers REST search endpoints, command/result objects, Go consumer interfaces, and gRPC messages.
- `references/databases.md` covers repository, query object, transaction, and migration interfaces.
- `references/caching.md` covers the cache `getOrLoad` contract, typed keys, and outage behavior.
