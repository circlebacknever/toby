---
name: toby-swd-strategy
description: >-
  Contains Toby's design pass, run before a change. Entry skills open this file
  by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Strategy

Leave the design at least as good after your change as before it. Do not count working code as progress when each piece adds a special case or a hidden dependency.

## Design pass

For anything beyond a one-line change, do not implement the first idea.

- State the change in one sentence. List each near-future variant, meaning a likely next change, that the request, a ticket, or the code states. Leave out a variant you inferred.
- Sketch at least two approaches that differ in where the complexity is: which module handles the hard part, what the interface exposes, and what callers must manage. Make the second approach the strongest option a competent engineer would pick. Pick the one with the simplest caller-side interface, even when its implementation is harder. This step decides which module holds the hard part. The "Cheap path first" rule in `toby-swd-interfaces`, which allows a single interface design, applies only after that decision.
- Check the near-future variants against the design. When a likely next change would force callers to change or add a special case, adjust the design now.
- When those variants are new cases picked by a tag or type, design the dispatch now. Use a lookup map when the case bodies are small, and an interface with implementations when each case has its own state. `toby-swd-modules` lists the options.

In `toby-swd-modules`, check 3 ("Pull complexity downward") says where complexity goes, and check 7 ("Split or merge") says when to split a function.

## Existing code

Before editing existing code, ask what structure it would have if it had been designed with this change in mind. When the answer is the current code plus the new part, add the part. When the current design no longer fits, refactor first with behavior unchanged, and run the tests. Then add the change on top as a separate step with no workaround. When the user asks for commits, the refactor gets its own commit. Do not default to the minimal diff, because a run of minimal diffs makes the design worse one commit at a time.

Offer the smallest local refactor that makes the change fit, with its cost and benefit, before doing it. When it would widen the task, let the user choose between the refactor and the tactical change.

After the change, find one flaw in the code you touched, such as an unclear name, a dead branch, a wrong comment, or duplicated logic. Fix it when the fix is small, local, and supports the change, and otherwise report it as a follow-up. Do not start cleanup outside the code you touched, and plan no separate cleanup phase.

## Quick fix

Take the tactical path only when one of these holds:

- The user accepted the shortcut and its later cleanup cost, because the sound design would miss a hard external deadline.
- The sound refactor would change an interface that other teams or callers depend on, and coordinating that is out of scope.
- The sound version needs information you do not have and cannot get.

Speed alone does not qualify. When you take the quick path, leave a comment with the sound design, the reason you skipped it, and when to do it.

## Report

After a change with a design decision, report the structure you chose and the main alternative you rejected. Also report any cleanup beyond the request and any quick fix with its sound design.

Open `references/examples.md` when comparing two approaches for a caller-facing change, or when labeling a deadline shortcut. Open `references/design-note.md` when writing a design note in chat.
