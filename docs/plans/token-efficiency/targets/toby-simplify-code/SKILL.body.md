# Toby Simplify Code

Make changed code simpler to read and keep behavior identical.

## Disposition

- Prefer precision over recall, because a missed cleanup costs less than a churning diff or a silent behavior change. When you are unsure, leave the code as it is.
- Claim a win only when it's countable. Before you touch anything, say which number goes down: lines, branches, state variables, duplicated blocks, or misleading names. "Clearer," "tidier," and "more idiomatic" state no number, so they do not count.
- "Nothing worth simplifying" is a complete answer. Do not ship a rewrite to have something to show.

## What to look for

**Over-built code where simpler code does the same job.**

- Repeated setup or branches that encode one rule, where defining them once removes lines.
- A long conditional where an early return or a named predicate shows intent.
- A clever one-liner, nested ternary, or dense chain that packs several branches or side effects into one expression and makes debugging worse.
- A private wrapper with a single caller that only renames another call and adds no type, name, or boundary value.
- A comment that repeats what the code plainly says, or a name that describes the code's history and hides its purpose.
- A try/catch, guard, or branch for a condition the types or an earlier check already rule out, when you can quote that proof from the code. A check on input from outside the program stays.

**A design smell from the catalog in `toby-code-review`'s `references/smells.md`.**

- Fix a match in this pass when the fix stays inside one module and changes no public signature, such as a dead function, a magic number, or a comment the diff made wrong. Leave any other match, and report it with its file:line. Route it to `toby-swd-interfaces` when the fix changes a signature, or to `toby-swd-modules` when it moves code between modules.

**Code that ignores a pattern this repo already uses.**

- The change re-solves something the repo solves elsewhere, such as a helper, util, base class, hook, decorator, error type, or config accessor. Search the repo for the operation before calling the code novel. Swap to the existing pattern only when two or more independent call sites already use it.

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
2. With no settled convention, use the language idiom only when it already appears elsewhere in the repo. Otherwise note it as a follow-up, because adding it is a style migration.

## Behavior drift

Ship a change only when a passing test asserts the touched behavior. A mechanical change can also ship when you show why its edge case can't occur.

Mechanical means a pure rename, a dead-code deletion, or a swap where the edge for its class is provably unreachable. Quote why ("can't be null, typed string, no | null"). Without a covering test, leave the change and note the edge that needs one.

Check this edge for each class of change:

- For an idiom swap, null, undefined, and empty handling match. Iteration order, short-circuiting, and laziness stay the same. The code throws the same exception type.
- For a library substitution, error type and message, ordering and stability, locale and timezone, and precision all match. A change in performance class (linear to quadratic, sync to async) is a behavior change, so leave it.
- For reuse of a repo pattern, the helper's defaults match the inline code: timeouts, retries, logging, caching, and what it throws.
- For an early return or predicate extraction, the same side effects run before the return, and the extracted predicate has none of its own.

## Keep

- Explicit, visible error handling for a failure that can happen. Collapsing distinct error paths or hiding a failure path is a behavior change.
- Slightly longer code that makes a state change visible.
- A test that asserts behavior through the public interface. Don't rewrite a test to make a cleanup pass.

## Out of scope

Leave anything that moves code between modules, changes a signature, or alters a public return type, because callers see each of those changes. Report a red flag from `toby-swd-modules`, `toby-swd-interfaces`, or `toby-swd-complexity` with the skill that handles it, and note any other larger cleanup as a follow-up.

If you spot a real bug or a security issue while cleaning up, don't fix it here, because the fix is a behavior change. Flag it only when you can state the input that triggers it and why the existing guards do not catch it. Then recommend a review pass.

## Process

Make one cleanup pass, and stop when the next change would not reduce a count. Then verify each change as Behavior drift describes.

## Final response

Lead with what got simpler and the number each change reduced. For every change, state in one clause the edge you checked, and the test that covers it or why the edge cannot occur. List each change you left out for lack of a covering test, with the edge that needs one. List each smell or red flag you left alone with the skill that handles it, and each follow-up, one per line.
