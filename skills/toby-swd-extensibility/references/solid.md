# SOLID principles

Ask these five questions when a design adds an interface, a subclass, or a new case. Each answer says what to change.

- **Single responsibility.** Does one person or team ask for every change to this module? A class that contains the pricing rule and the invoice wording gets edits from finance and from support. Split it so each module changes for one group. Keep a long class whole when its parts always change together, because two halves that must change together are harder to follow than one class.
- **Open-closed.** Does adding the next case edit one place? A new file kind adds one map entry or one class, and the code that picks between kinds stays the same. When the next case edits a switch in three files, use an option from "Replace the growing conditional" in SKILL.md.
- **Liskov substitution.** Can every class that implements an interface stand in for it? Each one accepts every input the interface accepts and returns what the interface promises. An override that throws "not supported" or accepts less input breaks every caller that uses the class through its interface type.
- **Interface segregation.** Does each caller depend on only the methods it calls? Let a caller declare a small interface with those methods, as Go code does, and let one class satisfy every caller's interface. A report job that only reads files then needs no `delete` method in its type.
- **Dependency inversion.** Does business code build the network clients it calls? Build each client once from config in the composition root, as `toby-swd-architecture` describes. Pass a client into business code only when a test cannot patch it. In tests, freeze time with the repo's tool, such as freezegun, so business code needs no clock parameter.
