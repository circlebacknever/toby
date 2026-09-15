---
name: toby-simplify-code
description: >-
  Reduce complexity in recently changed code while preserving behavior and tests. Use it
  when the user asks to simplify, tidy, tighten, refactor, de-duplicate, or clarify code
  that already works. It edits the code. Skip it when the user asked for findings and no
  edit, which `toby-code-review` handles.
---

# Toby Simplify Code

Make changed code simpler to read and keep behavior identical. A rewrite that only swaps one style for another is churn, because it changes lines and makes nothing simpler. Never ship a diff to look productive, because this skill is meant to prevent that churn.

## Disposition

- Prefer precision over recall, because a missed cleanup costs less than a churning diff or a silent behavior change. When you are unsure, leave the code as it is.
- Claim a win only when it's countable. Before you touch anything, say which number goes down: lines, branches, state variables, duplicated blocks, or named traps removed. "Clearer," "tidier," and "more idiomatic" name no number that went down, so a rewrite that only swaps style can claim them without simplifying anything.
- Prove that behavior is preserved before you change the code. You must prove the edit is safe, so the default is to leave the code alone.
- Returning the diff unchanged is a valid result, so "Nothing worth simplifying" is a complete answer. Say it plainly, and don't ship a rewrite to have something to show.

## What to look for

**Over-built code where simpler code does the same job.**

- Repeated setup or branches with two or more real occurrences, where naming them once removes lines.
- A long conditional where an early return or a named predicate shows intent.
- A clever one-liner, nested ternary, or dense chain that packs several branches or side effects into one expression and makes debugging worse.
- A shallow wrapper with a single caller that only renames another call and adds no type, name, or boundary value.
- A parameter that leaks a lower-level mechanism into callers.
- A comment that repeats what the code plainly says, or a name that describes the code's history and hides its purpose.
- A try/catch, guard, or branch that defends against a condition that can't occur. toby-swd-complexity's error ladder already defines that condition out of existence. Removing the check leaves one fewer branch or catch block.

**A design smell from `references/smells.md`.**

- A match against the file's "Fix here" half is a countable win like any other in this section, so fix it in the same pass.

**Code that ignores a pattern this repo already uses.**

- The change re-solves something the repo solves elsewhere, such as a helper, util, base class, hook, decorator, error type, or config accessor. Search the repo for the operation before calling the code novel. Swap to the existing pattern only when two or more independent call sites already use it. A definition plus its one use is not a pattern. Treat two blocks as different when they look the same only after you ignore their differences.

**Code that ignores the language's idioms.**

- Hand-rolled control flow the language has a construct for: a manual index loop where an iterator or comprehension fits, a manual null check where there's optional chaining or null-coalescing, manual accumulation where a fold fits, concatenation where interpolation fits, a manual close where there's a context manager or defer.

**Code that hand-rolls what a library already in this repo provides.**

- Use a library only when it replaces a reimplementation in an error-prone area: timezones, unicode, retry and backoff, deep clone or equality, schema validation. Outside those areas, keep a few lines of plain stdlib, because saving a line or two isn't worth an import. The library must already be a direct dependency, so confirm it in the manifest. Adding a dependency is out of scope, so note it as a follow-up.

## Not a simplification

None of these is a countable win, so count none of them as a simplification and leave them alone:

- Reordering for taste.
- A rename that does not fix a misleading name.
- Swapping one construct for another of equal length and clarity.
- Splitting or merging expressions with no debugging gain.
- Formatting that a tool handles.

## Idiom or local style

1. When the repo has a settled convention for this exact construct, visible in two or more sibling files, follow it, even over the textbook idiom.
2. With no local convention, follow the language idiom.
3. Keep an idiom that appears nowhere else in the repo out of a cleanup pass, because adding it is a style migration. Note it as a follow-up.
4. Leave code that's already idiomatic or conventional, because rewriting it into another idiom is churn.

## Behavior drift

Ship a change only when a test covers the touched path and passes. A mechanical change can also ship when you show why its edge case can't occur.

Mechanical means a pure rename, a dead-code deletion, or a swap where the edge for its class is provably unreachable. Quote why ("can't be null, typed string, no | null"). Any change where the edge case could occur needs a covering test. Without that test, leave the change and note the edge that needs one. Do not ship on assumed equivalence.

Check this edge for each class of change:

- For an idiom swap, null, undefined, and empty handling match. Iteration order, short-circuiting, and laziness stay the same. The code throws the same exception type.
- For a library substitution, error type and message, ordering and stability, locale and timezone, and precision all match. A change in performance class (linear to quadratic, sync to async) is a behavior change, so leave it.
- For reuse of a repo pattern, the helper's defaults match the inline code: timeouts, retries, logging, caching, and what it throws. A helper that also logs is not equivalent to code that didn't.
- For an early return or predicate extraction, the same side effects run before the return, and the extracted predicate has none of its own.

## Keep

- Helpful domain boundaries.
- Explicit, visible error handling for a failure that can happen. Collapsing distinct error paths or hiding a failure path is a behavior change.
- Slightly longer code that makes a state change visible.
- A test that asserts behavior through the public interface. Don't rewrite a test to make a cleanup pass.

## Out of scope

Leave anything that moves code between modules, changes a signature, or alters a public return type. All of that is behavior-changing work.

Leave any cleanup that is not small, local, and behavior-preserving. When the cleanup matches the "Flag, don't fix" half of `references/smells.md`, name the smell and the skill that handles it. Do the same for a red flag in toby-swd-modules, toby-swd-interfaces, or toby-swd-complexity. Otherwise, note it as a follow-up.

If you spot a real bug or a security issue while cleaning up, don't fix it here, because the fix is a behavior change. Flag it only when you can state the input that triggers it and why the existing guards do not catch it. Do not report a vague "this might be buggy." Then recommend a review pass.

## Process

1. Inspect the diff and the patterns nearby and across the repo.
2. Pick candidates, and discard any that risk behavior drift.
3. Make one cleanup pass. Stop when the next change would not be a countable win.
4. Verify per the behavior-drift rules above.
5. Re-read the diff and confirm the calling code now states its intent more directly.

## Final response

Lead with what got simpler, ordered by how much reading effort each change saves. Give the number each change reduced. For every change, state in one clause the edge you checked and how you know it held. Name the covering test, or say why the edge case can't occur. If behavior couldn't be proven preserved, say what remains unknown. For a structural smell you spotted and left alone, write one line naming the smell and the skill that handles it, separate from the changes.
