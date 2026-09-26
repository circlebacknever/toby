# SOLID principles

This file maps each SOLID principle to the check in `toby-swd-modules` or `toby-swd-interfaces` that applies it. Use it when a plan, a review, or a user cites a principle by name.

- **Single responsibility** is check 1, decompose by knowledge. A module holds one body of knowledge, which gives it one reason to change. The principle does not ask for small classes. Check 7 rejects a split that leaves two shallow modules.
- **Open-closed** is the section on replacing the growing conditional. A new case adds an implementation or a map entry, and the code that selects the case stays unchanged.
- **Liskov substitution** is part of check 5. Every implementation accepts the input its interface accepts and returns what the interface promises. An override that throws "not supported" or narrows the input breaks each caller that holds the base type.
- **Interface segregation** is in `toby-swd-interfaces`. A caller depends only on the methods it calls, so a consumer that needs one method gets a one-method interface.
- **Dependency inversion** is in `toby-swd-interfaces` and its `references/runtime-config.md`. Domain code receives its collaborators, such as a client, a clock, or config values. The composition root constructs them.

In a review, a break of one of these principles is reported under the matching entry in `toby-code-review`'s `references/smells.md`:

| Principle | Smell entry |
|---|---|
| Single responsibility | Divergent change |
| Open-closed | Repeated type switch |
| Liskov substitution | Substitute breaks its contract |
| Interface segregation | Fat interface |
| Dependency inversion | Hardwired dependency |
