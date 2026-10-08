---
name: toby-swd-clarity
description: >-
  Contains Toby's rules for names, comments, and docstrings inside code. Entry
  skills open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Clarity

Names and types state part of a contract. When the language allows it, put the unit, what null means, and which states can occur into the type. Use comments for the rest, which is behavior, side effects, invariants the type cannot enforce, and reasons. Non-trivial code with no interface comment is unfinished, however good its names are.

## Naming

Picture a developer who sees only the name, with no declaration or surrounding code. Check that they would guess what the variable holds or what the function does. Make a name more specific as its scope grows. A loop index can be `i`, while a field, an argument, or anything exported needs a precise name. An over-specific name misleads too, such as an argument named `selection` on a method that works on any range. Use `data`, `value`, `result`, `status`, `flag`, or `count` only when the meaning is visible at a glance.

Give each name one purpose, so every variable with that name behaves the same. When you need several of one kind, keep the common root and add a prefix, such as `srcBlock` and `dstBlock`.

When no precise, short name fits after real effort, the thing probably has a mixed purpose, so split or rethink it. Keep a dense expression as one piece when it computes one result you can name, even if its steps have no good names.

## Consistency

Do similar things the same way, and dissimilar things differently. Before adding a convention for naming, structure, error handling, style, or test layout, read the local file and project and match what is there. Reuse the exact name already established for a concept.

Change an existing convention only with information that was not available when it was set. The new approach must also be enough of an improvement to justify changing every existing use. Convert every use in the same change, because a half-adopted convention stops a reader from trusting a familiar pattern. When one concept has several names across the codebase, offer the rename as a follow-up, because renaming it in one place adds another name.

## Proportionality

On every edit, check the names, the comments, and whether a developer new to the code would understand it on the first read. Some code is exported, called from several places, or costly to change later. Only for that code, change a convention everywhere it is used or add an AGENTS.md note. Leave already-clear code outside the change alone.

## Red flags

Before calling a clarity pass done, check the touched code for each of these:

- A name is vague, was hard to pick, or is used for two purposes.
- A comment repeats the code, or an interface comment describes internals.
- A field does not state its units, its bounds, or what null means, where those are not obvious.
- Non-trivial code has no interface or field comments.
- The touched code handles one concept in more than one way.
- A quick read gets the behavior wrong.

Open `references/comments.md` when the change adds or edits a comment, a docstring, or control flow a reader could misread.

Open `references/examples.md` when you write a return type for a hook or a comment on an effect or callback. Also open it for a comment that gives units, bounds, or what null means.
