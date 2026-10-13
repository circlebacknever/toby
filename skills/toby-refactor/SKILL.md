---
name: toby-refactor
description: >-
  Changes how code is arranged or reads and keeps its behavior the same. Use it
  when the user asks to simplify, tidy, refactor, de-duplicate, extract, split,
  merge, move, or rename code. Use it to switch code to a new runtime,
  framework, or tool chain that keeps behavior the same. Use it to add, fix, or
  delete comments and docstrings. Skip it when behavior should change, which
  toby-build, toby-bug-fix, or toby-optimize covers. Skip it when the user wants
  findings with no edit, which toby-code-review covers.
---

# Toby Refactor

Change the structure of code so the next change costs less, and keep its observable behavior the same. Work in small steps, and run the tests after each one. The steps can add up to a change as large as the target design needs.

## Defaults

- Name the change the refactor makes cheaper, such as the feature the user plans next, a bug that keeps coming back, or code the user can't follow.
- Decide the target design before the first edit, then move the code all the way to it.
- Keep each step small enough that a failing test points at that step. When a step fails, revert it and take a smaller step.
- Keep refactoring and behavior changes in separate steps. When the work needs a behavior change, say so, and make that change under `toby-build` or `toby-bug-fix`.
- Judge the result by the change it makes cheaper. Fewer lines, branches, tools, or edit sites for one rule count as evidence. "Clearer" and "more idiomatic" don't count on their own.
- "Nothing worth refactoring" is a complete answer. Don't ship a rewrite to have something to show.

## Tactical or strategic

Say in one line whether the refactor is tactical or strategic. It's strategic when any of these apply:

- It switches the code to a new runtime, framework, build tool, or test runner.
- It moves code between modules or changes the folder layout.
- It changes a signature or an exported type that more than one caller uses.
- The user names an end state, such as "as Bun-native as possible", and doesn't list single edits.

When a condition from this list appears partway through the work, say so, and treat the rest of the refactor as strategic.

Strategic work adds these to the steps below:

- At step 1, open `toby-swd-strategy`. For a tool switch, list each old tool, config file, and dependency that leaves the repo.
- When the request doesn't state the end state, ask one question about it before the first edit. Recommend the option that removes the old tool from the repo.

## Steps

1. Target. Write the target design in one or two sentences, with the change it makes cheaper. Open `toby-swd-warning-signs`, and ask its questions of the code the target touches.
2. Tests. Run the tests that cover the code you'll change, and confirm they pass. When the tests miss a behavior the refactor touches, write a characterization test first, as `toby-swd-testing` describes. When the user declines tests, list each unchecked behavior before the first edit.
3. Plan. Open `references/catalog.md`, and write the refactor as a sequence of named refactorings. Change a public, exported, or stored interface with the parallel change steps in that file.
4. Apply. Make one step, then run the tests. When the user asked for commits, commit after each passing step.
5. Finish. Search for each name the refactor removed or replaced. List each match that stays, with the reason it stays.

## Method skills

Each skill below is at `../<skill>/SKILL.md` relative to this skill's folder. Open the ones the target design needs.

- Names, comments, or docstrings: `toby-swd-clarity`.
- A split, merge, or move across files: `toby-swd-architecture` for where each part goes, then `toby-swd-modules`.
- A growing conditional or an inheritance tree: `toby-swd-extensibility`.
- A changed signature: `toby-swd-interfaces`. A changed module structure: `toby-swd-docs`.
- An error check for a condition that can't occur: `toby-swd-errors`.

## Behavior drift

Ship a step only when a passing test asserts the behavior it touches. A mechanical step can also ship without that test when you show why the edge case for that step can't occur.

Mechanical means a pure rename, a dead-code deletion, or a swap. For a swap, prove that the edge case listed below for its kind of change can't happen. Quote why ("can't be null, typed string, no | null"). When the tests miss a step and you can't prove its edge case away, write a characterization test first. When you can't write one, leave the step out and note the edge case.

Check this edge for each class of change:

- For an idiom swap, null, undefined, and empty handling match. Iteration order, short-circuiting, and laziness stay the same. The code throws the same exception type.
- For a library substitution, error type and message, ordering and stability, locale and timezone, and precision all match. A change in performance class (linear to quadratic, sync to async) is a behavior change, so don't make that substitution.
- For reuse of a repo pattern, the helper's defaults match the inline code: timeouts, retries, logging, caching, and what it throws.
- For an early return or predicate extraction, the same side effects run before the return, and the extracted predicate has none of its own.

## Keep

- Explicit, visible error handling for a failure that can happen. Collapsing distinct error paths or hiding a failure path is a behavior change.
- Slightly longer code that makes a state change visible.
- Each assertion in a test that checks behavior through the public interface. A step may change a test's imports, setup, or the names it calls.

## Bugs on the way

When you spot a bug or a security issue, don't fix it in a refactoring step, because the fix is a behavior change. Flag it only when you can state the input that triggers it and why the existing guards don't catch it. Then recommend a review pass. Report each warning sign outside the target design as a follow-up at file:line.

## Final response

Lead with the target design, whether the code now matches it, and the change it makes cheaper. List the refactorings you applied, in order. List each characterization test you added, and each edge case the tests don't cover. List each step you left out for lack of a test. List each problem you left alone and each follow-up at file:line, one per line.
