# SOLID principles

Ask these five questions when a design adds an interface, a subclass, or a new case:

- **Single responsibility:** does one team or domain rule drive every change to this module? Split a class that mixes pricing math and invoice formatting, and keep a class whole when its parts always change together.
- **Open-closed:** does adding the next case edit one place? When a new case edits switches across multiple files, replace the switches using `SKILL.md`.
- **Liskov substitution:** does every implementation accept every input the interface allows and fulfill its return contract? Never override a method to throw `NotImplementedError` or reject valid interface inputs.
- **Interface segregation:** does each caller depend only on the methods it calls? Let callers declare narrow interfaces so a read-only report job never depends on `delete()`.
- **Dependency inversion:** do business rules depend on the behavior they need while startup selects concrete providers (`toby-swd-architecture`)? Choose dependency injection or the repo's composition mechanism from responsibility, lifetime, and caller needs. A narrow consumer interface can justify one implementation. Test patching doesn't determine the production boundary.
