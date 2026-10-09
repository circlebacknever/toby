---
name: toby-swd-extensibility
description: >-
  Contains Toby's rules for code that branches on a type, kind, status, or
  provider. Entry skills open this file by path. Do not trigger it from a user
  request alone.
disable-model-invocation: true
---

# Toby SWD Extensibility

Use this file for code that branches on a type, kind, status, or provider, whether the branch is new or gains a case.

Build an extension point only for a next case that someone has shown you. A request, a ticket, a TODO, or a second implementation can show that case. So can a `git log` where the switch gained cases. An extension point with one implementation adds code that every reader has to trace, for a case that may never come.

## Replace the growing conditional

Treat an `if` or `switch` as a design smell when it gains a branch each time the product adds a new kind of thing. Copying the same branch decision across call sites is the same smell. In both cases, adding the next kind means editing shared code or several files at once. A `switch` over a set that has been stable for a year is fine, so leave it alone.

Work through these options in order and stop at the first one that fits.

1. **Move the branch onto the type** when the data type can compute the answer itself. Delete the branch when the normal code path already handles the unusual input. This option is often the whole fix.
2. **Data-driven dispatch** fits when each branch picks a small behavior based on the value of one field, such as `kind`. A lookup map from each value to its behavior replaces the branches.
3. **Discriminated union with an exhaustive switch** fits when branches read different fields. Guard it with `assertNever`.
4. **Polymorphism** fits when the list of cases keeps growing and each case has its own behavior, private state, or dependencies.
5. **Registry** fits when new cases must be addable without editing a central file. It is the most complex option.

Open `references/replace-the-conditional.md` when two adjacent options both seem to fit, or for examples in React, React Native, and backend code.

When two switches on the same field compute different values, such as a label and a fee, make each one exhaustive. Use `assert_never`, a sealed type, or a map whose test checks that every value has an entry. The next value then fails the type check or that test in both places. Merge the two switches only when both compute the same value.

In new code, use the chosen option from the start. When you add a case to a conditional copied across files you already edit, replace those copies first, within the limits in `toby-swd-campfire`. List a copy in any other file as a follow-up at file:line.

## Inheritance

- Implement an interface freely, as disk, S3, and memory classes implement one `Storage` interface. A new case is then a new class, and the code that picks a class stays the same.
- Share behavior through a helper object passed in, and avoid a base class. A parent and a subclass can break each other with no change at any call site. Default methods on an interface or trait can break implementations the same way.
- When you write a parent class that other code subclasses, make every method final except the one or two that subclasses override. Never let the parent and a subclass write the same field.

## Red flags

- An extension point, hook, or option with one implementation and no shown second case.
- A subclass that overrides a method to throw or to accept less input.

## References

Open `references/solid.md` when the design adds an interface or a parent class, or when a plan, a review, or the user cites a SOLID principle. That file lists one question per principle, with its answer.
