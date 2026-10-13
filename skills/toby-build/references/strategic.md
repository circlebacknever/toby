# Strategic work

Open this file when step 1 of `toby-build` marks the work strategic. Each section below adds to a step in the skill body.

## Reading the code

Strategic work also reads the call sites the change would affect, and the sibling feature. The sibling is the shipped feature most like this one, on the same layer and using the same data. Read it end to end: route, handler, model, test, and doc.

Before copying the sibling, check it against the "Design check" in `toby-swd-architecture` and the red flags in `toby-swd-modules`. Follow its structure when it passes, and design the new code without each flaw you found. Don't copy a shallow module, one whose interface is nearly as complex as the work behind it.

Greenfield means the repo doesn't have a similar feature. Before you create a second new file, state the two closest patterns the repo uses elsewhere, even in another layer. Say which one you extend, as the greenfield example in `references/examples.md` does.

## Slices and the plan

`references/examples.md` shows four features cut into slices, with their criteria and wiring.

## Stops

Stop 3 comes at the end of each plan group, as the Plan Format section of the operating guide requires. At each stop 3:

1. Open with what the user can now do, using the slice's name.
2. List what proved it and what the next slice does.
3. For each decision the next slice depends on, take its usual answer and list it as an assumption the user can change at this stop.
4. Wait for the user's yes.

Put a question before step 1 only when the Decisions section of the operating guide allows one. Do the same when a criterion turned out wrong, or when reading the code missed an item from step 1's strategic list.

## The design lines

The plan's design block has each of these lines that has content:

- The structure chosen, and the main reason for it.
- The alternative rejected, and why.
- The sibling feature and each flaw in it at file:line.
- Each rule the feature adds, such as a count, a limit, or a table of values, with the one function that computes it and every caller of that function.
- Each new or changed module, with the details it hides from its callers.
- Each new or changed signature, with its interface comment.
- The checks from `toby-swd-hardening`, `toby-swd-twelve-factor`, and `toby-swd-observability` that apply to this code.
- Any refactor that runs before the feature code.

## Resuming half-built work

Before touching code, recover the mode, the criteria, the plan, the steps already checked off, and the last stop's decision. When you can't find one of these, rebuild it from the code and the original request. List which ones you rebuilt, and confirm them before continuing, because criteria rebuilt from a diff repeat the diff's mistakes.

Half-built experiment code stays experiment code until the user says otherwise.
