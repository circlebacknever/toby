---
name: toby-simplify-code
description: >-
  Reduce complexity in recently changed code while preserving behavior and tests. Use it
  when the user asks to simplify, tidy, tighten, refactor, de-duplicate, or clarify code
  that already works. It edits the code. Skip it when the user asked for findings and no
  edit, which `toby-code-review` owns.
---

# Toby Simplify Code

Make changed code simpler to read and keep behavior identical. A lateral rewrite that only swaps one style for another is churn. Never ship a diff to look productive, which is the churn this skill exists to prevent.

## Disposition

- Precision over recall. A missed cleanup costs less than a churning diff or a silent behavior change. When unsure, leave it.
- Claim a win only when it's countable. Before you touch anything, say which number goes down: lines, branches, state variables, duplicated blocks, or named traps removed. "Clearer," "tidier," "more idiomatic" count nothing down. They're how a lateral rewrite disguises itself.
- Prove behavior is preserved, then change. The burden sits on the edit, so the default is to leave the code alone.
- Returning the diff unchanged is a valid result. "Nothing worth simplifying" is a complete answer. Say it plainly, and don't ship a rewrite to have something to show.

## What to look for

**Over-built code where simple does the same job.**

- Repeated setup or branches that can be named once — two or more real occurrences, where naming them once removes lines.
- A long conditional where an early return or a named predicate shows intent.
- A clever one-liner, nested ternary, or dense chain that packs several branches or side effects into one expression and makes debugging worse.
- A shallow wrapper with a single caller that only renames another call and adds no type, name, or boundary value.
- A parameter that leaks a lower-level mechanism into callers.
- A comment that narrates what the code plainly says; a name that records history while hiding purpose.
- A try/catch, guard, or branch defending against a condition that can't occur, the kind toby-swd-complexity's error ladder already defines out of existence — removing it is one fewer branch or catch block.

**A design smell from references/smells.md.**

- A match against the file's "Fix here" half is a countable win like any other in this section, so fix it in the same pass.

**Code that ignores a pattern this repo already uses.**

- The change re-solves something the repo solves elsewhere — a helper, util, base class, hook, decorator, error type, config accessor. Search the repo for the operation before calling the code novel. Swap to the existing pattern only when two or more independent call sites already use it. A definition plus its one use is not a pattern. If you have to squint to call two blocks the same, they aren't.

**Code that fights the language's idioms.**

- Hand-rolled control flow the language has a construct for: a manual index loop where an iterator or comprehension fits, a manual null check where there's optional chaining or null-coalescing, manual accumulation where a fold fits, concatenation where interpolation fits, a manual close where there's a context manager or defer.

**Code that hand-rolls what a library already in this repo provides.**

- Reach for a library only when it replaces a reimplementation in a hazard-prone class: timezones, unicode, retry and backoff, deep clone or equality, schema validation. Outside those, a few lines of plain stdlib stay, because saving a line or two isn't worth an import. The library must already be a direct dependency, so confirm it in the manifest. Adding a dependency is out of scope, so note it as a follow-up.

## Not a simplification

Reordering for taste, a rename that doesn't fix a misleading name, swapping one construct for another of equal length and clarity, splitting or merging expressions with no debugging gain, formatting a tool owns. None of these clear the countable-win bar, so leave them.

## Idiom or local style

1. When the repo has a settled convention for this exact construct, visible in two or more sibling files, it wins, even over the textbook idiom.
2. With no local convention, follow the language idiom.
3. An idiom that appears nowhere else in the repo stays out of a cleanup pass, because that's a style migration, noted as a follow-up.
4. Leave code that's already idiomatic or conventional. Rewriting it into another idiom is churn.

## Behavior drifts quietly

A change ships one of two ways: a test covers the touched path and passes, or the change is mechanical and you show why the edge can't fire.

Mechanical means a pure rename, a dead-code deletion, or a swap where the edge for its class is provably unreachable, and you quote why ("can't be null — typed string, no | null"). Anything where the edge could fire is edge-crossing. It needs a covering test, or you leave it and note the edge that needs one. Do not ship on assumed equivalence.

The edge per class:

- Idiom swap — null, undefined, and empty handling match; iteration order holds; short-circuit and laziness hold; the same exception type is thrown.
- Library substitution — error type and shape, ordering and stability, locale and timezone, and precision all match. A change in performance class (linear to quadratic, sync to async) is a behavior change, so leave it.
- Repo-pattern reuse — the helper's defaults match the inline code: timeouts, retries, logging, caching, what it throws. A helper that also logs is not equivalent to code that didn't.
- Early return or predicate extraction — the same side effects run before the return, and the extracted predicate has none of its own.

## Keep

- Helpful domain boundaries.
- Explicit, visible error handling for a failure that can happen. Collapsing distinct error paths or hiding a failure path is a behavior change.
- Slightly longer code that makes a state change visible.
- A test that asserts behavior through the public interface. Don't rewrite a test to make a cleanup pass.

## Out of scope

Moving code between modules, changing a signature, or altering a public return shape is behavior-changing work. If a cleanup isn't small, local, and behavior-preserving, leave it. When it matches the "Flag, don't fix" half of references/smells.md, or a red flag in toby-swd-modules, toby-swd-interfaces, or toby-swd-complexity, name the smell and the skill that owns it. Otherwise, note it as a follow-up. If you spot a real bug or a security issue while cleaning up, don't fix it here, because that's a behavior change. Flag it only when you can state the input that triggers it and why no guard catches it. A vague "this might be buggy" is noise. Then recommend a review pass.

## Process

1. Inspect the diff and the patterns nearby and across the repo.
2. Pick candidates, discard any that risk behavior drift.
3. Make one cleanup pass. Stop when the next change doesn't clear the countable-win bar.
4. Verify per the behavior-drift rules above.
5. Re-read the diff and confirm the caller now reads closer to intent.

## Final response

Lead with what got simpler, ordered by how much reading effort each change saves, and the number each one drove down. For every change, state in one clause the edge you checked and how you know it held — the covering test, or why the edge can't fire. If behavior couldn't be proven preserved, say what remains unknown. A structural smell spotted but left alone gets one line naming the smell and the skill that owns it, kept apart from what changed.
