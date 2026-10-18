---
name: toby-swd-warning-signs
description: >-
  Contains the warning signs in code from Martin Fowler's Refactoring. Each
  sign is a question, with the case where the code is fine and the refactorings
  that remove it. Use it when deciding what to refactor or reviewing code for
  design problems. Skip it for a bug, which toby-bug-fix covers.
---

# Toby SWD Warning Signs

Ask each question below of the code in scope. A warning sign is structure that makes a likely change cost more than it needs to. Before acting on a match, check when the code is fine, and quote your search when proof requires code outside the file.

`toby-refactor` and its `references/catalog.md` give the steps for each fix. In user-facing replies and reviews, describe the concrete fix in plain words without naming the catalog labels below.

## Names and comments

- **Mysterious Name:** does a reader have to read the body to learn what a function, variable, or field does? Keep standard domain terms and short loop counters (`i`), and rename anything vague (`toby-swd-clarity`).
- **Comments:** does a comment explain what a block does because the code is hard to follow? Keep comments that state why, a unit, or an invariant, and extract or rename hard-to-follow code so it explains itself. Rewrite any comment the diff made false, quoting the line that contradicts it.

## Duplication and size

- **Duplicated Code:** do two or more places repeat the same business rule that must change together? Leave blocks alone when they look similar by coincidence, and extract a shared helper function when they must change together.
- **Long Function:** does a function mix helper calls with low-level steps, or pack nested ternaries and side effects into one line? Keep a long function whole when its steps share local state behind one simple signature (`toby-swd-modules` check 7), and extract self-contained subtasks when they simplify the parent.
- **Large Class:** does a class have fields used by only a subset of its methods, or two method groups that never interact? Keep the class whole when most methods use most fields, or extract the separate group into a delegated helper class.
- **Long Parameter List:** does a caller have to check the declaration to get the argument order right, or pass a flag that switches the function between two jobs? Split flag-switched functions in two, or group related parameters into a parameter object.
- **Data Clumps:** do the same two or three values (such as `start` and `end`) travel together across multiple signatures? Group them into one parameter object or value type (`DateRange`).

## Change

- **Divergent Change:** does one module change for unrelated reasons (such as database queries and tax rules)? Split the phases or move the unrelated functions into separate modules unless both belong to the single decision the module hides.
- **Shotgun Surgery:** does changing one rule require small edits across many files? Move the scattered functions and fields into one module unless a codegen tool updates them automatically.
- **Repeated Switches:** does the same switch or `if` chain on a type or status appear in multiple places? Keep two exhaustive switches when they compute different domain values, or replace the repeated switch using `toby-swd-extensibility`.

## Data

- **Global Data:** can code anywhere mutate a module-level variable, singleton field, or class variable? Keep constants and startup-initialized config, and wrap mutable globals behind functions or move the state into an instance.
- **Mutable Data:** does a function return its result by mutating an input argument, or expose mutable state that callers must track? Keep local variables, mutator methods, and caller-supplied performance buffers, and otherwise return a new value or read-only view.
- **Primitive Obsession:** does code pass a domain value (money, email, date range) as a bare string or number whose validation repeats across call sites, or repeat a magic literal (`attempts > 3`) across files? Wrap the value in a type that validates in its constructor, or define a named constant.
- **Temporary Field:** does a class have a field that only one method sets? Pass that value as a parameter or extract those methods into a small helper object.

## Coupling

- **Feature Envy:** does a method read another object's fields more than its own? Keep mappers and comparators as they are, and move other calculations onto the object that has the data.
- **Message Chains:** does a caller chain through three or more objects (`order.customer().address().city()`)? Keep fluent builders and pipelines, and otherwise add a method on the target object that answers the question directly.
- **Middle Man:** does a class forward most of its methods unchanged to another object? Keep a wrapper that hides a vendor SDK behind a domain contract, and inline wrappers that add nothing.
- **Insider Trading:** do two modules read or mutate each other's private fields? Move the coupled function or field so one module manages the state.

## Code that does too little

- **Lazy Element:** does a one-line function or wrapper class add no clearer name and hide no decision? Keep it when the name states why or hides an external dependency, and inline it otherwise.
- **Speculative Generality:** does code define a hook, parameter, interface, or dead function with only one caller and no second case stated in the request, a ticket, or the code? Keep exported library APIs and framework hooks, and delete unused hooks and parameters.
- **Loops:** does an imperative loop filter, map, or sum values where the repo uses collection pipelines? Keep a loop when early exits or side effects make it clearer, or rewrite it as a pipeline to match the repo.

## Classes and inheritance

- **Alternative Classes with Different Interfaces:** do two classes solve the same job behind different method names? When callers swap between them, align their signatures and extract a shared helper.
- **Data Class:** is a class only fields and getters/setters while external callers enforce its invariants? Keep plain data records at serialization boundaries, and move invariant checks and behavior methods onto domain classes (`toby-swd-interfaces`).
- **Refused Bequest:** does a subclass ignore its parent's contract or override a method to throw? Replace the inheritance with a passed-in helper object.
