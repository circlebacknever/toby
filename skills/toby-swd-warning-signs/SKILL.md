---
name: toby-swd-warning-signs
description: >-
  Contains the warning signs in code from Martin Fowler's Refactoring. Each
  sign is a question, with the case where the code is fine and the refactorings
  that remove it. Use it when deciding what to refactor or reviewing code for
  design problems. Skip it for a bug, which toby-bug-fix covers.
---

# Toby SWD Warning Signs

Ask each question below of the code in scope. A warning sign (Fowler's code smell) is structure that makes a likely change cost more than it needs to. Before acting on a match, check the sentence that states when the code is fine, and quote your search when proof requires code outside the file.

`toby-refactor` and its `references/catalog.md` give the steps for each named refactoring.

## Names and comments

**Mysterious Name.** Does a reader have to read the body to learn what a function, variable, or field does? Fine when it is a standard domain or language term, such as `i` in a short loop. Fix: Rename Variable, Rename Field, or Change Function Declaration (`toby-swd-clarity`).

**Comments.** Does a comment explain what a block does because the code is hard to follow? Fine when it states why, a unit, or an invariant the type can't express. Fix: Extract Function named for what the block does, or Introduce Assertion. Rewrite any comment the diff made false, and quote the line that falsifies a comment before reporting it.

## Duplication and size

**Duplicated Code.** Does the same business rule appear in two or more places that must change together? Fine when two blocks look similar by coincidence and change for different reasons. Fix: Slide Statements and Extract Function into a shared helper (prefer helper composition over Pull Up Method on a base class).

**Long Function.** Does a function mix calls to helpers with low-level steps, or pack nested ternaries and side effects into one expression? Fine when it is one deep abstraction whose steps share local state and would become conjoined helpers if split (`toby-swd-modules` check 7), or a top-to-bottom parser or numeric loop. Fix: Extract Variable, Decompose Conditional, or Extract Function for a self-contained subtask.

**Large Class.** Does a class have fields used by only a subset of its methods, or two method groups that never interact? Fine when most methods use most fields. Fix: Extract Class and delegate to it.

**Long Parameter List.** Does a caller have to check the declaration to get the argument order right, or pass a boolean/enum flag that switches the function between two jobs? Fine when keyword arguments keep each independent parameter clear. Fix: Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query, or Remove Flag Argument.

**Data Clumps.** Do the same two or three values (such as `start` and `end`) travel together across multiple signatures? Fine when they appear in one signature. Fix: Introduce Parameter Object or Extract Class.

## Change

**Divergent Change.** Does one module change for unrelated reasons (such as database queries and tax rules)? Fine when both reasons belong to the single design decision the module hides. Fix: Split Phase, Extract Class, or Move Function.

**Shotgun Surgery.** Does changing one rule require small edits across many files? Fine when a codegen or rename tool makes the edits automatically. Fix: Move Function and Move Field into one module, or Combine Functions into Class.

**Repeated Switches.** Does the same switch or `if` chain on a type or status appear in multiple places? Fine when there is a single switch, or when two exhaustive switches on the same field compute different domain values. Fix: apply the first matching option in `toby-swd-extensibility` (Move onto Type, Lookup Map, Exhaustive Switch, or Polymorphism).

## Data

**Global Data.** Can code anywhere mutate a module-level variable, singleton field, or class variable? Fine for constants and values initialized once at startup. Fix: Encapsulate Variable and restrict setter access, or Move Field.

**Mutable Data.** Does a function return its result by mutating an input argument, or expose mutable state that callers must track? Fine for local variables, methods whose job is mutating their receiver, caller-supplied performance buffers, or language `TryParse` out-parameters. Fix: Separate Query from Modifier, Change Reference to Value, or Remove Setting Method.

**Primitive Obsession.** Is a domain value (such as money, an email, or a date range) passed as a bare string or number whose validation repeats across call sites, or is a rule literal (`attempts > 3`) duplicated across files? Fine for a value checked once in a small scope. Fix: Replace Primitive with Object (enforcing invariants in its constructor), or define a named constant.

**Temporary Field.** Does a class hold a field that is populated only during one method call? Fix: Extract Class (method object) or Introduce Parameter Object.

## Coupling

**Feature Envy.** Does a method read another object's fields more than its own? Fine when combining multiple objects is the method's job, as in a mapper or comparator. Fix: Extract Function and Move Function onto that object.

**Message Chains.** Does a caller chain through three or more objects (`order.customer().address().city()`)? Fine in a fluent builder or pipeline where each step returns the same abstraction. Fix: Hide Delegate, or Move Function.

**Middle Man.** Does a class forward most of its methods unchanged to another object? Fine when it hides an unstable vendor SDK behind a domain contract. Fix: Remove Middle Man or Inline Class.

**Insider Trading.** Do two modules read or mutate each other's private fields? Fine inside a single module or between a unit and its test. Fix: Move Function, Move Field, or Hide Delegate.

## Code that does too little

**Lazy Element.** Does a function, class, or wrapper module add no clearer name and hide no decision beyond its one-line body? Fine when the name states why or hides an external dependency. Fix: Inline Function or Inline Class.

**Speculative Generality.** Does code define a hook, parameter, interface, or dead function with only one caller and no second case stated in the request, a ticket, or the code? Fine for exported library APIs and framework reflection hooks. Fix: Change Function Declaration, Inline Class, or Remove Dead Code.

**Loops.** Does an imperative loop filter, map, or sum values where the repo uses collection pipelines? Fine when the repo avoids pipelines or when early exits and side effects make a loop clearer. Fix: Split Loop, then Replace Loop with Pipeline.

## Classes and inheritance

**Alternative Classes with Different Interfaces.** Do two classes solve the same job behind different method names? Fine when callers never swap between them. Fix: Change Function Declaration to align the signatures and extract a shared helper.

**Data Class.** Is a class only fields and getters/setters while external callers enforce its invariants? Fine for plain data records at serialization boundaries. Fix: Encapsulate Record, Remove Setting Method, and Move Function (`toby-swd-interfaces`).

**Refused Bequest.** Does a subclass ignore its parent's contract or override a method to throw? Fine when it only omits internal parent helpers that callers never invoke. Fix: Replace Subclass with Delegate or Replace Superclass with Delegate.
