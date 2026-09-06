# Smell Catalog

The main skill only credits a change with a literal countable reduction — fewer lines, branches, or duplicated blocks. Its Out of scope section rules out anything that moves code between modules or changes a signature. So a design smell that needs a boundary fix walks past silently, because fixing it isn't this skill's job and nothing tells it to say so. That is the gap.

This file closes the gap. Every entry below is either:

- **Fix here** — the fix stays local and clears the countable-win bar same as anything else in What to look for. Do it in the same pass.
- **Flag, don't fix** — the fix crosses a module boundary or changes a public signature. Name the smell, the file:line, and the routing skill in the final response. Leave the code alone.

## Fix here

- **Comment invalidated at a distance.** A change makes a comment somewhere else in the codebase wrong — a caller's documented assumption, an invariant note at a distant call site, a doc comment describing behavior that just changed. Fires when the diff changes a function's behavior, return type, error conditions, or an invariant, and a search for callers or the described behavior turns up a comment still asserting the old one. Fix here: correct the comment to match the new behavior — a one-line edit, no boundary crossed. Exception: only flag what you can name — a specific file:line and the exact clause the diff makes false. "Something elsewhere might describe this" isn't checkable. Drop it.

- **Dead function or class.** A function, method, or class that compiles and could run, but nothing calls it anymore. Fires when the diff removes its last caller, or a repo-wide grep for the symbol name turns up only its own definition. Fix here: delete it. Nothing else in the repo names it, so removing it touches no signature and no caller — pure line reduction. Exception: anything exported or public that code outside this repo might consume, and anything reached through reflection, dependency injection, dynamic dispatch, or a test-only harness. Grep the identifier as a string, confirm export status, before you delete.

- **Magic number or string.** An unexplained literal doing real work in the logic — a comparison, a multiplier, a branch condition — standing in for a concept the reader has to guess at. Fires when a changed line checks against, multiplies by, or branches on a bare literal with no obvious meaning from the surrounding lines, or the same literal shows up at two or more sites for the same concept. Fix here: name it. One constant, declared once, replaces the guesswork and the repetition. Exception: a self-evident value in a narrow scope — a loop's 0 or -1, an HTTP status checked once inline. The tell is a value nobody could explain on sight, or repetition where a change to one should change all.

- **Stale comment beside changed code.** A comment sitting right next to code the diff just changed still describes what the code used to do. Fires when a changed line or block behaves differently now, and the comment immediately above or beside it, visible in the same hunk, still asserts the old version. Fix here: rewrite the comment to match what the code does now — same hunk, roughly the same line count. Exception: a comment describing something the diff left alone — an invariant that still holds, a unit that's still correct. Flag it only when the diff visibly changes the exact thing the adjacent comment claims.

## Flag, don't fix

Each of these needs a change this skill's Out of scope note already excludes: a signature, a public return type, or which module owns what. Name the entry, the file:line, and the skill listed, then leave the code alone.

`toby-code-review`'s `references/smells.md` owns the full entry for every name below: the definition, the Fires-when criterion you quote against the code, and the exception that makes it a non-finding. Read it there before flagging. Keeping a second copy here is how the accessors entry ended up in four files with three wordings.

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
| Divergent change | `toby-swd-modules` | the diff's stated intent is one change, but the edits inside a single file or class serve visibly unrelated purposes — a pricing-rule tweak and a display-copy tweak in the same class |
| Shotgun surgery | `toby-swd-modules` | the diff touches many files with small, similar-shaped edits — a field added to N structs, a case added to N switch statements — that all encode the same underlying decision |
| Shallow module | `toby-swd-modules` | a new or changed module's public surface — parameters, methods, required setup — takes about as much explaining as its internals would |
| Information leakage | `toby-swd-modules` | the diff touches two or more modules to express what is really one decision |
| Pass-through method | `toby-swd-modules` | a new or changed method's body is a single call to another method, passing the same arguments through unchanged |

The exceptions matter as much as the criteria. An entry whose exception covers the code in front of you is not a finding, and the exceptions live only in the owning catalog.

## Not on this list, on purpose

**Refused bequest** (a subclass that uses only a slice of what it inherits) doesn't get an entry. Its diff-visible half — a subclass overriding an inherited method to throw or no-op — is already `toby-swd-modules`' "Deep implementation-inheritance hierarchy" red flag. The rest of the definition needs a full census: the parent class's public methods against everything the subclass actually calls. Running that census means opening and reading an unrelated file end to end. That's a full-file read this skill doesn't do during a cleanup pass, so flag the override half under the existing red flag and stop there.

A numeric ceiling on function length, "comments are always failures," a blanket "duplication is evil," and a TDD-mandates-test-first rule are also absent, deliberately. Each one contradicts a position `toby-swd-modules`, `toby-swd-clarity`, or `toby-swd-interfaces` already states for this repo — depth over line count, comments as the legitimate carrier of what code can't say, knowledge-gated duplication, interface-first design. Adding any of them here would put this skill at odds with the skills that wrote the code in the first place.
