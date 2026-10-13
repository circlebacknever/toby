---
name: toby-swd-warning-signs
description: >-
  Contains the warning signs in code from Martin Fowler's Refactoring. Each
  sign is a question, with the case where the code is fine and the refactorings
  that remove it. Use it when deciding what to refactor or reviewing code for
  design problems. Skip it for a bug, which toby-bug-fix covers.
---

# Toby SWD Warning Signs

Ask each question below of the code in scope. A warning sign is code that makes a likely change cost more than it needs to. Fowler calls these code smells. Before you act on a match, read the sentence that says when the code is fine. When the proof needs code outside the scope, quote the search you ran.

Each fix names refactorings from Fowler's catalog. The `toby-refactor` skill lists their steps.

## Names and comments

**Mysterious Name.** Does a reader have to open the body to learn what a function, variable, or field is for? The name is fine when it is a standard term in the domain or the language, such as `i` in a three-line loop. Fix: Rename Variable, Rename Field, or Change Function Declaration. `toby-swd-clarity` covers how to choose the name.

**Comments.** Does a comment explain what a block does, because the code doesn't say it? The comment is fine when it states why, a unit, or an invariant the code can't show. Fix: Extract Function with a name that says what the block does, or Introduce Assertion for an invariant. A comment that still describes code the change replaced gets rewritten in the same step. A comment you only suspect is out of date doesn't count, so quote the line that makes it false.

## Duplication and size

**Duplicated Code.** Does the same rule appear in two or more places that must change together? The copies are fine when they share text but change for different reasons. Fix: Slide Statements to bring each copy into one block, then Extract Function. Use Pull Up Method when the copies are in sibling subclasses.

**Long Function.** Does a function need comments or blank lines to separate its parts, or mix calls to helpers with low-level code? The function is fine when it is low-level all the way through, such as a parser or a numeric loop, and reads top to bottom. Fix: Extract Function for each part, named for what it does. Replace Temp with Query, Introduce Parameter Object, or Decompose Conditional come first when temporaries or conditions block the extraction. A nested ternary or a dense chain that packs several branches or side effects into one expression has the same warning sign. Fix it with Extract Variable or Decompose Conditional.

**Large Class.** Does a class have fields that only some of its methods use, or two groups of methods that don't call each other? The class is fine when most methods use most fields. Fix: Extract Class, Extract Superclass, or Replace Type Code with Subclasses.

**Long Parameter List.** Does a caller check the declaration to pass the arguments in order? A boolean or enum argument that picks which of two jobs a function does is the same warning sign. The list is fine when each argument stands alone and keyword arguments keep the call readable. Fix: Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query, or Remove Flag Argument.

**Data Clumps.** Do two or three values, such as `start` and `end`, go together through several signatures or classes? The values are fine when they appear together in one place. Fix: Extract Class, or Introduce Parameter Object.

## Change

**Divergent Change.** Does one module change for unrelated reasons, such as a new database in one change and a new tax rule in the next? The module is fine when both reasons belong to the one thing it hides. Fix: Split Phase, Extract Class, or Move Function, so each module changes for one reason.

**Shotgun Surgery.** Does one change to a rule force small edits in many files? The edits are fine when a tool makes them, as with a rename or generated code. Fix: Move Function and Move Field into one module, Combine Functions into Class, or Inline Class.

**Repeated Switches.** Does the same switch or if-chain on a type or status appear in two or more places? A single switch is fine, such as the one in a factory. Fix: Replace Conditional with Polymorphism. `toby-swd-extensibility` covers the choice of dispatch.

## Data

**Global Data.** Can code anywhere change a module-level variable, a singleton's field, or a class variable? The data is fine when it is a constant, or a value set once at startup and only read after. Fix: Encapsulate Variable, then limit who calls the setter, or Move Field.

**Mutable Data.** Does a value change after it's created in a way callers must track? A function that returns its result by changing an argument has this warning sign, such as `apply_discount(order)` that sets `order.total`. The change is fine for a local variable inside one function and for a method whose job is to change its own object. It's also fine for a buffer the caller passes for speed, and for a language's out-parameter convention, such as C#'s `TryParse`. Fix: Separate Query from Modifier, Split Variable, Replace Derived Variable with Query, Change Reference to Value, or Remove Setting Method.

**Primitive Obsession.** Is a domain value, such as money, a phone number, or a date range, a bare string or number whose parsing repeats? A literal that stands for a rule, such as `attempts > 3` in two files, is the same warning sign. The value is fine when its meaning is plain in a small scope, such as an HTTP status checked once. Fix: Replace Primitive with Object, Replace Type Code with Subclasses, or a named constant for the literal.

**Temporary Field.** Does a class have a field that holds a value only during one operation? Fix: Extract Class for the field and the code that reads it, or Introduce Special Case.

## Coupling

**Feature Envy.** Does a method mostly read another object's fields? The method is fine when combining several objects is its job, as in a comparator or a mapper. Fix: Extract Function on the part that reads the other object, then Move Function.

**Message Chains.** Does a line call through three or more objects, as in `order.customer().address().city()`? The chain is fine in a builder or a pipeline, where each call returns the same kind of value. Fix: Hide Delegate, or Extract Function and Move Function on the end of the chain.

**Middle Man.** Does a class forward most of its methods to one other object? The class is fine when it hides something callers shouldn't depend on, such as a vendor library. Fix: Remove Middle Man, or Inline Function.

**Insider Trading.** Do two modules read and write each other's internal data? The access is fine inside one module, or between a class and its tests. Fix: Move Function, Move Field, Hide Delegate, or Replace Subclass with Delegate.

## Code that does too little

**Lazy Element.** Does a function, class, or module do so little that its name adds nothing over the code inside it? The element is fine when its name explains a step the code can't, or it hides a dependency. Fix: Inline Function, Inline Class, or Collapse Hierarchy.

**Speculative Generality.** Does code have a hook, parameter, abstract class, or option with one user and no stated second case? Dead code has the same warning sign, which a search for the name as a string confirms. The code is fine when the request, a ticket, or the code states the second case. Exported code, and code reached through reflection, dependency injection, or a test harness, is also fine. Fix: Collapse Hierarchy, Inline Function, Inline Class, Change Function Declaration, or Remove Dead Code.

**Loops.** Does a loop filter, map, or sum values that a pipeline, such as `filter` and `map`, would state directly? The loop is fine when the repo doesn't use pipelines elsewhere, or when early exits and side effects make a pipeline harder to read. Fix: Split Loop, then Replace Loop with Pipeline.

## Classes and inheritance

**Alternative Classes with Different Interfaces.** Do two classes do the same job behind different method names? The classes are fine when callers never choose between them. Fix: Change Function Declaration to match the names, Move Function, then Extract Superclass for the code they share.

**Data Class.** Is a class only fields with getters and setters, while other code does its work? The class is fine when it's a record kept as plain data on purpose, such as a message at a service boundary. Fix: Encapsulate Record, Remove Setting Method, and Move Function to bring the behavior to the data. `toby-swd-interfaces` covers the methods that replace the accessors.

**Refused Bequest.** Does a subclass ignore what its parent provides, or override a parent method to throw? The subclass is fine when it skips only internal helpers that callers don't use. Fix: Push Down Method and Push Down Field, or Replace Subclass with Delegate, or Replace Superclass with Delegate.
