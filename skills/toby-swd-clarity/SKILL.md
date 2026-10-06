---
name: toby-swd-clarity
description: >-
  Contains Toby's rules for names, comments, and docstrings inside code. Entry
  skills open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Clarity

Names and types state part of a contract. Put a unit, a null meaning, or a rule about which states can occur in a type when the language allows it. Comments state the rest, which is behavior, side effects, invariants the type cannot hold, and reasons. Non-trivial code with no interface comment is unfinished, however good its names are.

## Naming

Show a name alone, with no declaration or surrounding code, and check that a developer would guess what it holds or does. Make a name more specific as its scope grows. A loop index can be `i`, while a field, an argument, or anything exported needs a precise name. An over-specific name misleads too, such as an argument named `selection` on a method that works on any range. Use `data`, `value`, `result`, `status`, `flag`, or `count` only when the meaning is visible at a glance.

Give each name one purpose, so every variable with that name behaves the same. When you need several of one kind, keep the common root and add a prefix, such as `srcBlock` and `dstBlock`.

When no precise, short name fits after real effort, the thing probably has a mixed purpose, so split or rethink it. A dense expression that computes one nameable result is one abstraction, even when its steps have no good names.

## Consistency

Do similar things the same way, and dissimilar things differently. Before adding a convention for naming, structure, error handling, style, or test layout, read the local file and project and match what is there. Reuse the exact name already established for a concept.

Change an existing convention only with information that was not available when it was set. The new approach must also be better enough to convert every existing use. Convert every use in the same change, because a half-adopted convention stops a reader from trusting a familiar pattern. When one concept has several names across the codebase, offer the rename as a follow-up, because renaming it in one place adds another name.

## Proportionality

Check naming, comments, and obvious-on-read on every edit. Convert a whole convention or add an AGENTS.md note only for code that is exported, called from several places, or costly to change later. Leave already-clear code outside the change alone.

## Red flags

Before calling a clarity pass done, check the touched code for each of these:

- A name is vague, was hard to pick, or is used for two purposes.
- A comment repeats the code, or an interface comment describes internals.
- A field has no units, bounds, or null meaning where those are not obvious.
- Non-trivial code has no interface or field comments.
- The touched code handles one concept in more than one way.
- A quick read gets the behavior wrong.

Open `references/comments.md` when the change adds or edits a comment, a docstring, or control flow a reader could misread.

Open `references/examples.md` when writing a precision comment, a comment on an effect or callback, or a return type for a hook.
