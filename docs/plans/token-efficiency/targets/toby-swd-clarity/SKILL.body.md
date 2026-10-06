# Toby SWD Clarity

Names and types state part of a contract. Put a unit, a null meaning, or a rule about which states can occur in a type when the language allows it. Comments state the rest, which is behavior, side effects, invariants the type cannot hold, and reasons. Non-trivial code with no interface comment is unfinished, however good its names are.

## Naming

Show a name alone, with no declaration or surrounding code, and check that a developer would guess what it holds or does. Make a name more specific as its scope grows. A loop index can be `i`, while a field, an argument, or anything exported needs a precise name. An over-specific name misleads too, such as an argument named `selection` on a method that works on any range. Use `data`, `value`, `result`, `status`, `flag`, or `count` only when the meaning is visible at a glance.

Give each name one purpose, so every variable with that name behaves the same. When you need several of one kind, keep the common root and add a prefix, such as `srcBlock` and `dstBlock`.

When no precise, short name fits after real effort, the thing probably has a mixed purpose, so split or rethink it. A dense expression that computes one nameable result is one abstraction, even when its steps have no good names.

## Comments

Write an interface comment at the entry point that states behavior, arguments, return value, side effects, exceptions, and caller preconditions, with no internals. When it needs internals to be complete, the fix is in the design, which `toby-swd-interfaces` covers.

Write every other comment at a different level from the code:

- **Precision**, on fields, arguments, and return values, adds what the name and type cannot say, such as units, inclusive or exclusive bounds, what null or empty means, ownership, and invariants. A field whose name and type state the whole contract gets no comment.
- **Intuition**, inside code, says why the code exists, what a block does as a whole, or why a non-obvious approach was chosen. For a bug fix whose purpose is not obvious, say why and cite the tracker.

A field comment is a whole sentence too, such as `// This is null while the request is loading or after it fails.`

Delete a comment that restates the adjacent code or the name. Delete commented-out code, and leave change history to git. Document each decision once, in the place a reader looks first. At a call site, point to the called method's comment and do not explain it again. A decision that spans modules goes in the module's AGENTS.md, as `toby-swd-docs` describes, with a pointer at each affected site.

Keep secrets, credentials, tokens, and personal data out of logs, diagnostics, and source.

## Consistency

Do similar things the same way, and dissimilar things differently. Before adding a convention for naming, structure, error handling, style, or test layout, read the local file and project and match what is there. Reuse the exact name already established for a concept.

Change an existing convention only with information that was not available when it was set. The new approach must also be better enough to convert every existing use. Convert every use in the same change, because a half-adopted convention stops a reader from trusting a familiar pattern. When one concept has several names across the codebase, offer the rename as a follow-up, because renaming it in one place adds another name.

## Obviousness

After writing, reread the code as a developer new to it, and check that their first guess about each behavior is right. A reviewer's report of confusion outranks your own read. Fix these four cases:

- **Generic container.** A tuple, pair, or untyped object that the caller reads by position gets a type with named fields.
- **Declared type differs from the real one.** A value typed as a broad supertype that behaves as a different subtype breaks every user of that type, so make the types match. A component that takes another component's props and drops or reinterprets one is this case.
- **Behavior that breaks convention.** A constructor that starts threads, a method that changes unrelated state, or an effect with a non-obvious trigger gets a comment where a linear reader meets it, and again where a reader would act on the wrong assumption.
- **Hidden control flow.** An event handler, callback, or effect states in its own comment when and why it runs.

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

Open `references/examples.md` when writing a precision comment, a comment on an effect or callback, or a return type for a hook.
