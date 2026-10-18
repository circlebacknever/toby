---
name: toby-swd-extensibility
description: >-
  Contains Toby's rules for code that branches on a type, kind, status, or
  provider. Use it when adding a case, an implementation, or a subclass, or
  when a conditional keeps growing. Skip it for a branch with two cases that
  the request doesn't extend.
---

# Toby SWD Extensibility

Use this file when code branches on a type, kind, status, or provider, or adds an implementation or subclass.

Build an extension point only when the request, a ticket, a TODO, a second implementation, or `git log` shows another case coming. An extension point with one implementation adds indirection for a case that may never arrive.

## Replace the growing conditional

When a `switch` or `if` chain gains a branch on each new product case, or repeats across files, work through these five options in order and stop at the first one that fits (leave a switch alone when its cases have stayed fixed for a year):

1. **Move the branch onto the type** when the data object or a null-object stand-in can compute the answer itself.
2. **Data-driven dispatch** (a lookup map from `kind` to a function or value) when each branch runs a small stateless behavior.
3. **Discriminated union with an exhaustive switch** guarded by `assertNever` / `assert_never` when branches read different fields per variant.
4. **Polymorphism** (an interface with one class per case) when cases keep growing and each case holds its own private state or dependencies.
5. **Registry** (`registerHandler`) only when external or plugin code must add cases without editing a central file.

Open `references/replace-the-conditional.md` when choosing between adjacent options or for frontend and backend examples.

When two switches on the same field compute different values (such as a fee and a label), keep them separate and make both exhaustive with `assert_never`, a typed `Record<Kind, ...>`, or a test over all enum values. When adding a case to a conditional duplicated across files you already touch, consolidate the copies within the limits of `toby-swd-campfire`, and list copies in other files as follow-ups at `file:line`.

## Inheritance

- Implement interfaces freely (`Storage` implemented by disk, S3, and memory classes), so adding a provider adds one class without changing callers.
- Share code through a passed-in helper object, and avoid an implementation base class or default interface methods, because base and derived classes can break each other through shared state and self-calls.
- When a framework requires a base class, mark every method `final` except the one or two methods subclasses are meant to override, and never write the same field from both parent and subclass.

## Red flags

- An interface, hook, or option with one implementation and no stated second case.
- A subclass that overrides a parent method to throw `NotImplementedError` or accept narrower inputs.

## References

Open `references/solid.md` when adding an interface or parent class, or when a plan, review, or user cites SOLID.
