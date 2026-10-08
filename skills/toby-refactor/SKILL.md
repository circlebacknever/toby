---
name: toby-refactor
description: >-
  Changes how code is arranged or reads and keeps its behavior and tests the
  same. Use it when the user asks to simplify, tidy, refactor, de-duplicate,
  extract, split, merge, move, or rename code. Use it to add, fix, or delete
  comments and docstrings. Skip it when behavior should change, which
  toby-build, toby-bug-fix, or toby-optimize covers. Skip it when the user wants
  findings with no edit, which toby-code-review covers.
---

# Toby Refactor

Make changed code simpler to read and keep behavior identical.

## Defaults

- Make only the cleanups you are sure of, because a missed cleanup costs less than a large, noisy diff or a behavior change nobody notices. When you are unsure, leave the code as it is.
- Call a change an improvement only when you can count what it reduced. Before you touch anything, say which number goes down: lines, branches, state variables, duplicated blocks, or misleading names. "Clearer," "tidier," and "more idiomatic" state no number, so they do not count.
- "Nothing worth simplifying" is a complete answer. Do not ship a rewrite to have something to show.

## Pick the scope
Pick one scope from the request, say it in one line, and open only the files it lists. Each skill in the list is at `../<skill>/SKILL.md` relative to this skill's folder.
- Names, comments, or docstrings only: open `toby-swd-clarity`.
- A local cleanup inside changed code: open `references/cleanup.md` and `toby-code-review`'s `references/smells.md`.
- A split, merge, move, or extraction across files: open `toby-swd-strategy`, then `toby-swd-modules`. Open `toby-swd-interfaces` when a signature changes, and `toby-swd-docs` when module structure changes.
- An error check for a condition that cannot occur: open `toby-swd-errors`.
The Behavior drift rules below, which keep behavior the same, apply to every scope.

## Behavior drift

Ship a change only when a passing test asserts the touched behavior. A mechanical change can also ship without that test when you show why the edge case for that change can't occur.

Mechanical means a pure rename, a dead-code deletion, or a swap. For a swap, you must prove that the edge case listed below for its kind of change can't happen. Quote why ("can't be null, typed string, no | null"). When no test covers a change and you cannot prove its edge case away, do not make the change. Note the edge case that needs a test.

Check this edge for each class of change:

- For an idiom swap, null, undefined, and empty handling match. Iteration order, short-circuiting, and laziness stay the same. The code throws the same exception type.
- For a library substitution, error type and message, ordering and stability, locale and timezone, and precision all match. A change in performance class (linear to quadratic, sync to async) is a behavior change, so do not make that substitution.
- For reuse of a repo pattern, the helper's defaults match the inline code: timeouts, retries, logging, caching, and what it throws.
- For an early return or predicate extraction, the same side effects run before the return, and the extracted predicate has none of its own.

## Keep

- Explicit, visible error handling for a failure that can happen. Collapsing distinct error paths or hiding a failure path is a behavior change.
- Slightly longer code that makes a state change visible.
- A test that asserts behavior through the public interface. Don't rewrite a test to make a cleanup pass.

## Out of scope

In a local cleanup, do not move code between modules, change a signature, or change a public return type, because callers see each of those. Report a red flag from `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-errors`, or `toby-optimize` with the skill that handles it, and note any other larger cleanup as a follow-up.

If you spot a real bug or a security issue while cleaning up, don't fix it here, because the fix is a behavior change. Flag it only when you can state the input that triggers it and why the existing guards do not catch it. Then recommend a review pass.

## Process

Make one cleanup pass, and stop when the next change would not reduce a count. Then verify each change as Behavior drift describes.

## Final response

Lead with what got simpler and the number each change reduced. For every change, state in a short phrase the edge case you checked, and the test that covers it or why the edge cannot occur. List each change you left out for lack of a covering test, with the edge that needs one. List each smell or red flag you left alone with the skill that handles it, and each follow-up, one per line.
