---
name: toby-swd-strategy
description: >-
  Contains Toby's design pass, run before a change. Entry skills open this file
  by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Strategy

Leave the code you change easier to change than it was. Do not count working code as progress when each piece adds a special case or a hidden dependency.

## Design pass

For anything beyond a one-line change, do not implement the first idea. When the change copies the structure of similar code and makes no design choice, write `Structure: follows <path:line>` and skip the rest of this pass. Do the same for a new optional parameter passed unchanged to an existing call, and cite that call.

- State the change in one sentence. List each likely next change that the request, a ticket, or the code states, and leave out any you inferred.
- Sketch at least two approaches that differ in where the complexity is: which module handles the hard part, what the interface exposes, and what callers must manage. Make the second approach the strongest option a competent engineer would pick. Pick the one with the simplest caller-side interface, even when its implementation is harder.
- Check each likely next change against the design. When one would force callers to change or add a special case, adjust the design now.
- When those changes are new cases picked by a tag or type, design the dispatch now. Use a lookup map when the case bodies are small, and an interface with implementations when each case has its own state. `toby-swd-extensibility` lists the options.

In `toby-swd-modules`, check 3 ("Pull complexity downward") says where complexity goes, and check 7 ("Split or merge") says when to split a function.

## Existing code

Before you edit existing code, follow "Before the first edit" in `toby-swd-campfire`. After the change passes its tests, follow its "After the tests pass".

## The shortcut

Take the shortcut only when one of these holds:

- The user accepted the shortcut and its later cleanup cost, because the sound design would miss a hard external deadline.
- The sound refactor would change an interface that other teams or callers depend on, and coordinating that is out of scope.
- The sound version needs information you do not have and cannot get.

Speed alone does not qualify. When you take the shortcut, leave a comment with the sound design, the reason you skipped it, and when to do it.

## Report

After a change with a design decision, report the structure you chose and the main alternative you rejected. Also report any cleanup beyond the request and any shortcut with its sound design.

Open `references/examples.md` when comparing two approaches for a caller-facing change, or when labeling a deadline shortcut. Open `references/design-note.md` when writing a design note in chat.
