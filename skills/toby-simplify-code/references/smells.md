# Smell Catalog

The main skill credits a change only with a literal countable reduction, such as fewer lines, branches, or duplicated blocks. Its Out of scope section rules out anything that moves code between modules or changes a signature. So the skill says nothing about a design smell that needs a fix at a module boundary. Fixing that smell isn't the skill's job, and no rule tells the skill to report it.

This file lists those smells, and each entry below is marked Fix here or Flag, don't fix.

- **Fix here** means the fix stays local and is a countable win, like anything else in What to look for. Do it in the same pass.
- **Flag, don't fix** means the fix crosses a module boundary or changes a public signature. Name the smell, the file:line, and the routing skill in the final response. Leave the code alone.

## Fix here

- **Comment invalidated at a distance.** A change makes a comment somewhere else in the codebase wrong. The comment can be a caller's documented assumption, an invariant note at a distant call site, or a doc comment describing changed behavior. Fires when the diff changes a function's behavior, return type, error conditions, or an invariant, and a search for callers or the described behavior turns up a comment still asserting the old one. Fix here: correct the comment to match the new behavior. The edit is one line and crosses no boundary. Exception: only flag a comment when you can name its file:line and the exact clause the diff makes false. "Something elsewhere might describe this" isn't checkable. Drop it.

- **Dead function or class.** A function, method, or class compiles and could run, but nothing calls it anymore. Fires when the diff removes its last caller, or a repo-wide grep for the symbol name turns up only its own definition. Fix here: delete it. Nothing else in the repo names it, so removing it touches no signature and no caller, and the only change is fewer lines. Exception: anything exported or public that code outside this repo might consume, and anything reached through reflection, dependency injection, dynamic dispatch, or a test-only harness. Before you delete it, grep the identifier as a string and confirm its export status.

- **Magic number or string.** An unexplained literal does work in the logic, such as in a comparison, a multiplier, or a branch condition. It stands in for a concept the reader has to guess at. Fires when a changed line checks against, multiplies by, or branches on a bare literal with no obvious meaning from the surrounding lines, or the same literal shows up at two or more sites for the same concept. Fix here: name it. One constant, declared once, replaces the guesswork and the repetition. Exception: a self-evident value in a narrow scope, such as a loop's 0 or -1 or an HTTP status checked once inline. A literal is a finding when nobody could explain it on sight, or when it repeats where a change to one should change all.

- **Stale comment beside changed code.** A comment sitting right next to code the diff just changed still describes what the code used to do. Fires when a changed line or block behaves differently now, and the comment immediately above or beside it, visible in the same hunk, still asserts the old version. Fix here: rewrite the comment in the same hunk to match what the code does now, at roughly the same line count. Exception: a comment describing something the diff left alone, such as an invariant that still holds or a unit that's still correct. Flag it only when the diff visibly changes the exact thing the adjacent comment claims.

## Flag, don't fix

Each of these needs a change this skill's Out of scope note already excludes: a signature, a public return type, or which module owns what. Name the entry, the file:line, and the skill listed, then leave the code alone.

`toby-code-review`'s `references/smells.md` has the full entry for every name below. Each entry there gives the definition, the Fires-when criterion you quote against the code, and the exception that makes it a non-finding. Read it there before flagging. Keeping a second copy here is how the accessors entry ended up in four files with three wordings.

| Entry | Route to | Fires when |
|---|---|---|
| Long parameter list / data clump | `toby-swd-interfaces` | a changed or new signature has enough parameters that a caller has to check the declaration to get the order right, or the same two or three parameters appear together more than once in the diff |
| Output argument | `toby-swd-interfaces` | the diff adds or changes a function that writes into a parameter it received as its way of producing a result, where a return value would say the same thing |
| Flag / selector argument | `toby-swd-interfaces` | a changed or new function branches on a bool or enum parameter near the top of its body into substantially different code paths, and the parameter's only job is choosing which path runs |
| Message chain | `toby-swd-interfaces` | a changed line chains three or more navigations through different objects' accessors to reach a final value or call |
| Primitive obsession | `toby-swd-interfaces` | a new field or parameter representing a recognizable domain concept is typed as a raw primitive, and the same parsing or validation for that concept already appears at two or more sites |
| Accessors as the public surface | `toby-swd-interfaces` | a new or changed class's public methods are mostly getters and setters for its own fields, with no operation that names intent |
| Speculative generality | `toby-swd-interfaces` | a new parameter or option has no current caller using anything but its default, and grepping for callers turns up no concretely named near-future use either |
| Artificial coupling | `toby-swd-modules` | the diff adds a general-purpose constant or helper inside a specific, unrelated class, and nothing about that class's own job explains why it owns this |
| Feature envy | `toby-swd-modules` | a changed method's body is mostly a chain of getters and fields pulled from one other object, with little use of its own class's state, and that other object could own the work |
| Divergent change | `toby-swd-modules` | the diff states one intent, but the edits inside one file or class serve visibly unrelated purposes, like a pricing-rule tweak and a display-copy tweak |
| Shotgun surgery | `toby-swd-modules` | the diff makes small, similar edits across many files that all encode one underlying decision. Examples are a field added to N structs or a case added to N switch statements |
| Shallow module | `toby-swd-modules` | explaining a new or changed module's parameters, methods, and required setup takes about as long as explaining its internals |
| Information leakage | `toby-swd-modules` | the diff touches two or more modules to express what is really one decision |
| Pass-through method | `toby-swd-modules` | a new or changed method's body is a single call to another method, passing the same arguments through unchanged |

Check the exceptions as closely as the criteria. An entry whose exception covers the code in front of you is not a finding, and the exceptions are only in the owning catalog.

## Not on this list, on purpose

**Refused bequest** (a subclass that uses only a slice of what it inherits) doesn't get an entry. The half a diff shows is a subclass overriding an inherited method to throw or no-op. `toby-swd-modules`' "Deep implementation-inheritance hierarchy" red flag already covers that half. Checking the rest of the definition means comparing the parent class's public methods against everything the subclass calls. That comparison means opening and reading an unrelated file end to end. This skill doesn't read a full file during a cleanup pass, so flag the override half under the existing red flag and stop there.

A numeric ceiling on function length, "comments are always failures," a blanket "duplication is evil," and a TDD-mandates-test-first rule are also absent, deliberately. Each one contradicts a position that `toby-swd-modules`, `toby-swd-clarity`, or `toby-swd-interfaces` already states for this repo. Those positions are depth over line count, comments as the place for what code can't say, duplication gated on shared knowledge, and interface-first design. Adding any of them here would make this skill contradict the skills that guided the code when it was written.
