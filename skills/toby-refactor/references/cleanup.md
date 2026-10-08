# Cleanup

This file lists what a local cleanup looks for, what is not a simplification, and how to pick between an idiom and local style. Open it when the scope is a local cleanup inside changed code.

## What to look for

**Over-built code where simpler code does the same job.**

- Repeated setup or branches that encode one rule, where defining them once removes lines.
- A long conditional where an early return or a named predicate shows intent.
- A clever one-liner, nested ternary, or dense chain that packs several branches or side effects into one expression and makes debugging worse.
- A private wrapper with a single caller that only renames another call, and adds no type, no clearer name, and no useful boundary.
- A comment that repeats what the code plainly says, or a name that describes the code's history and hides its purpose.
- A try/catch, guard, or branch for a condition the types or an earlier check already rule out, when you can quote that proof from the code. A check on input from outside the program stays.

**A design smell from the catalog in `toby-code-review`'s `references/smells.md`.**

- When code matches an entry in that catalog, fix it in this pass if the fix stays inside one module and changes no public signature, such as a dead function, a magic number, or a comment the diff made wrong. Leave any other match, and report it with its file:line. Route it to `toby-swd-interfaces` when the fix changes a signature, or to `toby-swd-modules` when it moves code between modules.

**Code that ignores a pattern this repo already uses.**

- The change re-solves something the repo solves elsewhere, such as a helper, util, base class, hook, decorator, error type, or config accessor. Search the repo for the operation before deciding that nothing in the repo already does it. Swap to the existing pattern only when two or more independent call sites already use it.

**Code that ignores the language's idioms.**

- Hand-rolled control flow the language has a construct for, such as a manual index loop or a manual close.

**Code that hand-rolls what a library already in this repo provides.**

- Use a library only when it replaces a reimplementation in an error-prone area: timezones, unicode, retry and backoff, deep clone or equality, schema validation. Outside those areas, keep a few lines of plain stdlib, because saving a line or two isn't worth an import. The library must already be a direct dependency, so confirm it in the manifest. Adding a dependency is out of scope, so note it as a follow-up.

## Not a simplification

Leave these alone, because none of them reduces a count:

- Reordering for taste.
- A rename that does not fix a misleading name.
- Swapping one construct for another of equal length and clarity.
- Splitting or merging expressions with no debugging gain.
- Splitting a function for its length alone.
- Merging blocks that share text but change for different reasons.
- Formatting that a tool handles.

## Idiom or local style

1. When the repo has a settled convention for this exact construct, visible in two or more sibling files, follow it, even over the textbook idiom.
2. With no settled convention, use the language idiom only when it already appears elsewhere in the repo. Otherwise note it as a follow-up, because adding the idiom starts a change to the repo's style, which is a separate task.
