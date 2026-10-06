# Comments and obviousness

This file has the rules for interface, precision, and intuition comments, and the four cases a first-time reader gets wrong. Open it when the change adds or edits a comment, a docstring, or control flow a reader could misread.

## Comments

Write an interface comment at the entry point that states behavior, arguments, return value, side effects, exceptions, and caller preconditions, with no internals. When it needs internals to be complete, the fix is in the design, which `toby-swd-interfaces` covers.

Write every other comment at a different level from the code:

- **Precision**, on fields, arguments, and return values, adds what the name and type cannot say, such as units, inclusive or exclusive bounds, what null or empty means, ownership, and invariants. A field whose name and type state the whole contract gets no comment.
- **Intuition**, inside code, says why the code exists, what a block does as a whole, or why a non-obvious approach was chosen. For a bug fix whose purpose is not obvious, say why and cite the tracker.

A field comment is a whole sentence too, such as `// This is null while the request is loading or after it fails.`

Delete a comment that restates the adjacent code or the name. Delete commented-out code, and leave change history to git. Document each decision once, in the place a reader looks first. At a call site, point to the called method's comment and do not explain it again. A decision that spans modules goes in the module's AGENTS.md, as `toby-swd-docs` describes, with a pointer at each affected site.

Keep secrets, credentials, tokens, and personal data out of logs, diagnostics, and source.

## Obviousness

After writing, reread the code as a developer new to it, and check that their first guess about each behavior is right. A reviewer's report of confusion outranks your own read. Fix these four cases:

- **Generic container.** A tuple, pair, or untyped object that the caller reads by position gets a type with named fields.
- **Declared type differs from the real one.** A value typed as a broad supertype that behaves as a different subtype breaks every user of that type, so make the types match. A component that takes another component's props and drops or reinterprets one is this case.
- **Behavior that breaks convention.** A constructor that starts threads, a method that changes unrelated state, or an effect with a non-obvious trigger gets a comment where a linear reader meets it, and again where a reader would act on the wrong assumption.
- **Hidden control flow.** An event handler, callback, or effect states in its own comment when and why it runs.
