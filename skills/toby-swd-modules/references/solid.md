# SOLID principles

This file maps each SOLID principle to the check in `toby-swd-modules` or `toby-swd-interfaces` that applies it.

- **Single responsibility** is check 1, split by what each module hides. Each module should get change requests from only one person or team. The principle does not ask for small classes. Check 7 rejects a split that leaves two shallow modules. A shallow module has an interface about as complex as the work behind it.
- **Open-closed** is the section on replacing the growing conditional. A new case adds an implementation or a map entry, and the code that selects the case stays unchanged.
- **Liskov substitution** applies to every class that implements an interface, which check 5 allows freely. Every implementation accepts the input its interface accepts and returns what the interface promises. An override that throws "not supported" or accepts less input breaks every caller that uses the class through its interface type.
- **Interface segregation** is in `toby-swd-interfaces`. Each caller declares an interface type with only the methods it calls, and one class or module implements all of those methods.
- **Dependency inversion** is in `toby-swd-interfaces` and its `references/runtime-config.md`. Domain code receives its collaborators, such as a client, a clock, or config values. The composition root constructs them.

In a review, a break of one of these principles is reported under the matching entry in `toby-code-review`'s `references/smells.md`:

| Principle | Smell entry |
|---|---|
| Single responsibility | Divergent change |
| Open-closed | Repeated type switch |
| Liskov substitution | Substitute breaks its contract |
| Interface segregation | Fat interface |
| Dependency inversion | Hardwired dependency |
