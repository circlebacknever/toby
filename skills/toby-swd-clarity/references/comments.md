# Comments and obviousness

This file has the rules for interface, precision, and intuition comments, and the four cases a first-time reader gets wrong. Open it when the change adds or edits a comment, a docstring, or control flow a reader could misread.

## Comments

Write an interface comment at the entry point that states behavior, arguments, return value, side effects, exceptions, and caller preconditions, with no internals. If the interface comment cannot be complete without describing how the code works inside, change the design, as `toby-swd-interfaces` describes.

Every other comment must add something the code does not show, either more precise detail or the reason behind the code. There are two kinds:

- **Precision**, on fields, arguments, and return values, adds what the name and type cannot say, such as units, inclusive or exclusive bounds, what null or empty means, ownership, and invariants. A field whose name and type state the whole contract gets no comment.
- **Intuition**, inside code, says why the code exists, what a block does as a whole, or why a non-obvious approach was chosen. For a bug fix whose purpose is not obvious, say why and cite the tracker.

A field comment is a whole sentence too, such as `// This is null while the request is loading or after it fails.`

Delete a comment that restates the adjacent code or the name. Delete commented-out code, and leave change history to git. Document each decision once, in the place a reader looks first. At a call site, point to the called method's comment and do not explain it again. Write a decision that affects several modules in the AGENTS.md of the module that contains them, as `toby-swd-docs` describes. At each affected place in the code, add a comment that points to that AGENTS.md section.

Keep secrets, credentials, tokens, and personal data out of logs, diagnostics, and source.

## Obviousness

After writing, reread the code as a developer new to it, and check that their first guess about each behavior is right. When a reviewer says the code confused them, trust that over your own impression. Fix these four cases:

- **Generic container.** A tuple, pair, or untyped object that the caller reads by position gets a type with named fields.
- **Declared type differs from the real one.** When a value is declared as a broad type but behaves like a narrower subtype, the mismatch breaks every user of the declared type. Change the declared type to match the real behavior. A component that takes another component's props and drops or reinterprets one is this case.
- **Behavior that breaks convention.** A constructor that starts threads, a method that changes unrelated state, or an effect with a non-obvious trigger gets a comment where someone reading the file from top to bottom first sees it. The same code gets a second comment where a reader would act on the wrong assumption.
- **Hidden control flow.** An event handler, callback, or effect states in its own comment when and why it runs.
