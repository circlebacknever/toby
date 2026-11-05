# Comments and obviousness

Open this file when adding or editing a comment, a docstring, or control flow that a reader could misread.

## Comments

Write an interface comment at the entry point that states behavior, arguments, return value, side effects, exceptions, and caller preconditions (`toby-swd-interfaces`). Describe guarantees callers rely on, including required ordering or durability. Hide implementation steps callers don't need to coordinate. Trace one call to check that the declaration explains its observable result.

Every other comment must add information the code and types can't express:

- **Field, argument, and return comments** state units, inclusive or exclusive bounds, what `null` or empty means, and invariants (`// Null while the request is loading or after it fails.`). Omit the comment when the name and type state the whole contract.
- **Why comments** inside a function explain why a block exists or why you chose a non-obvious approach, citing the issue tracker when a bug fix looks unusual.

Delete commented-out code and comments that only restate the code. Document each decision once where a reader looks first: point call sites to the called function's docstring, and record cross-module constraints in the module's `AGENTS.md` (`toby-swd-docs`). Never put secrets, tokens, or personal data in comments or logs.

## Obviousness

Reread touched code as a developer new to the file, and fix these four traps:

- **Unlabeled tuple or array:** replace a positional tuple or array return (`[data, err, loading]`) with an object or tagged union that has named fields.
- **Declared type broader than allowed values:** narrow the declared type to match the values the code actually accepts.
- **Surprising side effects:** when a constructor starts threads or a method mutates unrelated state, document that side effect at the declaration and at the call site.
- **Event handlers and effects:** explain when and why a handler, callback, or `useEffect` runs when its name, dependency list, and surrounding code leave that behavior unclear.
