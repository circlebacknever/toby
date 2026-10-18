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

Change the structure of code so the next change costs less, while keeping observable behavior identical. Work in small steps and run the tests after each step.

## Defaults

- Name the concrete change the refactor makes cheaper, such as a planned feature, a recurring bug area, or a tangle a reader misreads.
- Decide the target design before the first edit, then move the code all the way to it.
- Keep each step small enough that a failing test points to that step. When a step fails, revert it and take a smaller step.
- Keep refactoring and behavior changes separate. When the work needs a behavior change, state it and run that change under `toby-build` or `toby-bug-fix`.
- Measure the gain by a count that dropped: lines, branches, tools, or files edited per rule change. "Clearer" and "more idiomatic" don't count on their own, and "Nothing worth refactoring" is a complete answer.

## Tactical or strategic

State `Mode: cleanup (tactical)` or `Mode: cleanup (strategic)` in one line. The refactor is strategic when any of these apply:

- It switches the code to a new runtime, framework, build tool, or test runner.
- It moves code between modules or changes the folder layout.
- It changes a signature or exported type used across multiple files.
- The user states a target state for the whole codebase and doesn't list single edits.

When a strategic condition appears mid-refactor, say so and treat the rest of the work as strategic.

For a tool switch, design the target so the new tool handles every job the old tool did using its own standard API and layout, remove the old tool with its configs and dependencies, and port test assertions when switching test runners. When the request doesn't name the new tool or end state, ask one question in the first sentence and recommend the option that removes the old tool.

## Steps

1. **Target.** State the target design in one or two sentences with the change it makes cheaper. Open `toby-swd-warning-signs` to check the touched code, and for strategic work open `toby-swd-strategy`.
2. **Tests.** Run the covering tests and confirm they pass. When a behavior the refactor touches lacks a test, write a characterization test first (`toby-swd-testing`), or list each unchecked behavior if the user declines tests.
3. **Sequence.** Open `references/catalog.md` and list the sequence of named refactorings. Tactical work lists the sequence in chat, and strategic work offers to write a plan file using `toby-swd-plan` before the first edit. Use parallel change from `references/catalog.md` for public, exported, or multi-caller interfaces.
4. **Apply.** Apply one refactoring step (or one caller batch in a parallel change) and run the tests before starting the next step. Commit after each passing step when the user asked for commits.
5. **Finish.** Search the repo for every removed or replaced identifier, and list any remaining match with the reason it stays.

## Other skills

Open each skill at `../<skill>/SKILL.md` that the target design needs:

- Names, comments, or docstrings: `toby-swd-clarity`.
- A split, merge, or move across files: `toby-swd-architecture`, then `toby-swd-modules`.
- A growing conditional or inheritance tree: `toby-swd-extensibility`.
- A changed signature: `toby-swd-interfaces`. A changed module structure: `toby-swd-docs`.
- An error check for a condition that can't occur: `toby-swd-errors`.

## Behavior drift

Ship a step only when a passing test asserts the behavior it touches, or when the step is mechanical (a pure rename, dead-code deletion, or proven-equivalent swap) and you quote why its edge case can't occur (such as `"non-null string typed by schema"`). Check these edge cases before shipping a swap or extraction:

- **Idiom swap:** null, undefined, and empty handling, iteration order, short-circuiting, laziness, and thrown exception types all match.
- **Library substitution:** error type and message, ordering, stability, locale, timezone, precision, and complexity class (linear vs. quadratic, sync vs. async) all match.
- **Extracted or moved statements:** statements stay inside the same database transaction and lock acquisition order, and sequential `await` calls aren't turned into concurrent calls (or the reverse).
- **Implicit contracts:** serialized field names in queues or databases, exception types caught higher up the stack, and log or metric keys stay unchanged unless every reader updates with them.
- **Helper reuse or early return:** the helper's defaults (timeouts, retries, logging, caching, errors) match the inline code, and extracted predicates have no side effects.

## Keep

- Explicit error handling for failures that can occur. Collapsing distinct error paths is a behavior change.
- Slightly longer code that keeps a state change visible.
- Every test assertion that checks behavior through the public interface.

## Bugs on the way

Don't fix a bug or security issue inside a refactoring step, because that changes behavior. Report it at `file:line` with the triggering input and why current guards miss it, and list warning signs outside the target design as follow-ups.

## Final response

Lead with the target design, whether the code matches it, and the change it makes cheaper. List the applied refactorings in order, any characterization tests added, any edge cases or steps left out for lack of tests, and any bugs or follow-ups at `file:line`.
