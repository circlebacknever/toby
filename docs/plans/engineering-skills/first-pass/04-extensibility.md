# Toby's plan for the extensibility skill

Work mode: durable implementation. The SOLID material is a mapping file inside the largest method skill, and `toby-build` opens that skill only when the design adds a module.

## Group 4: adding the next case opens its own skill

- [x] Create `skills/toby-swd-extensibility/SKILL.md` as a hidden method skill.
- [x] Move the section "Replace the growing conditional" and check 5, "Prefer composition over implementation inheritance", from `skills/toby-swd-modules/SKILL.md` into the new skill. Keep their wording, so the lost-rules gate can match them.
- [x] Move `references/replace-the-conditional.md` and `references/solid.md` from `toby-swd-modules` to the new skill with `git mv`.
- [x] Add a short opening section. It says to build an extension point only for a variation that the request, a ticket, or a second implementation shows, and points to the one-instance wrapper entry in `toby-build`'s `references/checks.md`.
- [x] Add one question per SOLID principle to `references/solid.md`, each answered by a section of the skill or by `toby-swd-interfaces`, so the body stays under 700 tokens. The file keeps the smell-table mapping for reviews.
- [x] Update every pointer to the moved text. The known ones are check 6 and the red flags in `toby-swd-modules`, the dispatch item in `toby-swd-strategy`, the SOLID question in `toby-code-review`, and `toby-swd-interfaces/references/runtime-config.md`, which cites "option 4, polymorphism, in toby-swd-modules".
- [x] Open the new skill from `toby-build` when the design adds a case to a branch on a type or tag, a new implementation of an interface, or a subclass. Open it from `toby-refactor` for a split or merge across files, and from `toby-swd-modules` check 6.
- [x] Add the skill to `build-strategic` and `refactor` in `ROUTING_GROUPS`, to the token scenarios, and to the README.

### Verification

- Run `python3 evals/run.py gates`. Every moved sentence must find its survivor. Report each co-load group that passes the 5 percent growth gate.
- Run `grep -rn "toby-swd-modules" skills` and read each hit that mentions the conditional, composition, or SOLID. A hit that still sends the reader to `toby-swd-modules` for that text fails the check.
- Trace "add a fourth customer tier", where `price()` has a three-branch `switch` on tier, through `toby-build`. The trace passes when it opens `toby-swd-extensibility` and picks a dispatch option. Trace "add an optional `limit` argument to `list_orders`", which must not open it.
- Run `python3 scripts/voice-check.py --review` on every new or changed file, and read each sentence against the READ list.

If a check fails, stop and report it before Group 5.
