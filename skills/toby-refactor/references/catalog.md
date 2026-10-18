# Catalog

This file lists the refactorings from Martin Fowler's *Refactoring*, second edition, with the steps for the ones Toby uses most. Open it at step 3 of `toby-refactor`, when you plan the refactor as a sequence of named steps. Run the tests after each numbered step below.

## Steps

**Extract Function.**

1. Create a function named for what the code does, and copy the code into it.
2. Pass each variable the code reads as a parameter. Return each variable it changes that the caller reads later.
3. Replace the original code with a call to the new function.

Inline Function runs these steps in reverse.

**Rename.** Rename Variable, Rename Field, and the simple form of Change Function Declaration work the same way. When every use is in this repo and isn't public, exported, or stored, rename every use in one step with a rename tool or search. Otherwise, use parallel change.

**Parallel change.** Use it to change a public, exported, or stored interface, or one with callers in many files.

1. Add the new function, field, or format, and make the old one call or read the new one.
2. Move callers to the new form in small batches.
3. Delete the old form once a search shows that it doesn't have callers. For a public interface, keep the old form and mark it deprecated, unless the user approves the break.

**Move Function.**

1. Copy the function into its new module, and change the references inside it to work there.
2. Make the old function call the new one.
3. Move each caller to the new function, then delete the old one.

Move Field works the same way, after Encapsulate Variable puts every read and write behind a function.

**Encapsulate Variable.**

1. Write a function that reads the variable and one that writes it.
2. Replace each direct read and write with a call.
3. Make the variable private where the language allows it.

**Split Phase.** Use it when one function does two jobs in sequence, such as parsing input and then computing a result.

1. Extract the second job into its own function.
2. Add a data structure that the first job builds and the second job reads.
3. Move each value the second job reads into that structure, one at a time.
4. Extract the first job into a function that returns the structure.

**Replace Conditional with Polymorphism.**

1. Create a class for each case, and a factory function that returns the right class for a value.
2. Make callers get an object from the factory.
3. Move each branch of the conditional into a method on its class, one branch at a time.
4. Delete the conditional once every branch has moved.

**Replace Primitive with Object.**

1. Apply Encapsulate Variable to the field.
2. Create a small class for the value, with the parsing and checks the callers repeat.
3. Make the setter build the class, and the getter return its value.
4. Move each repeated check into the class, then change callers to use the class.

**Substitute Algorithm, or switch a library, runtime, or tool.**

1. Put the calls to the old implementation behind one function or module, when they aren't already.
2. Write the new implementation with the new tool's own API behind the same interface, and run the same tests against it.
3. Move callers to the new implementation.
4. Delete the old implementation, with its config files, its dependencies, and any folder layout only the old tool needed.

A small project can switch its runtime, test runner, or build tool in one step. Afterward, search the repo for each name of the old tool.

## The rest of the catalog

Describe each refactoring step in plain words in plans and replies (`inline the one-line wrapper`, `move the tax calculation into Order`), and use the catalog names below only when the user asks for them.

- First set: Extract Variable, Inline Variable, Introduce Parameter Object, Combine Functions into Class, Combine Functions into Transform.
- Encapsulation: Encapsulate Record, Encapsulate Collection, Replace Temp with Query, Extract Class, Inline Class, Hide Delegate, Remove Middle Man.
- Moving code: Move Statements into Function, Move Statements to Callers, Replace Inline Code with Function Call, Slide Statements, Split Loop, Replace Loop with Pipeline, Remove Dead Code.
- Data: Split Variable, Replace Derived Variable with Query, Change Reference to Value, Change Value to Reference.
- Conditionals: Decompose Conditional, Consolidate Conditional Expression, Replace Nested Conditional with Guard Clauses, Introduce Special Case, Introduce Assertion.
- APIs: Separate Query from Modifier, Parameterize Function, Remove Flag Argument, Preserve Whole Object, Replace Parameter with Query, Replace Query with Parameter, Remove Setting Method, Replace Constructor with Factory Function, Replace Function with Command, Replace Command with Function.
- Inheritance: Pull Up Method, Pull Up Field, Pull Up Constructor Body, Push Down Method, Push Down Field, Replace Type Code with Subclasses, Remove Subclass, Extract Superclass, Collapse Hierarchy, Replace Subclass with Delegate, Replace Superclass with Delegate.

## Repo conventions

- Follow the repo's convention for a construct when two or more sibling files use it, even over the textbook idiom.
- Use a language idiom the repo doesn't use yet when the target design calls for it, and list it in the plan.
- Reuse a helper, error type, or config accessor the repo already has when two or more call sites use it. Search the repo for the operation before you write a new one.
- Use a library only to replace code that reimplements an error-prone area, such as timezones, unicode, retries, deep equality, or schema validation. Outside those areas, keep a few lines of standard-library code, because saving a line or two isn't worth an import. Confirm the library is already a direct dependency in the manifest. Adding a dependency needs the user's approval.

## Checks that stay

- Remove a try/catch, a guard, or a validation only when you can quote the type, contract, or earlier check that rules out its condition.
- Keep every check on input from outside the program, such as a request body, a file, or an environment variable, because that input can hold any value.

## Not a refactoring

These change the code and don't make a later change cheaper, so leave them out:

- Reordering code for taste.
- A rename that doesn't fix a misleading name.
- A swap between two constructs of equal length and clarity.
- Splitting a function into parts that don't have their own names.
- Merging blocks that share text and change for different reasons.
- Formatting that a tool handles.
