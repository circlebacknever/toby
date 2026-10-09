# Toby's plan for the design check after tests pass

Work mode: durable implementation. New code ships with design flaws that a reviewer would catch, and edited code is left no better than it was.

`toby-build` checks the design before coding and checks process at handoff. Nothing reads the design of the finished diff, so flaws added during coding reach the user. Tactical work, which is most work, never opens the `toby-swd-modules` red flags.

## Group 3: a passing change gets a design check and leaves its files better

- [x] Create `skills/toby-swd-campfire/SKILL.md` as a hidden method skill, with a body under 600 tokens so `build-tactical` stays inside its 5 percent gate. The name comes from the user's "campfire rule", which is better known as the Boy Scout rule.
- [x] Write the design check, which runs once the change's tests pass. It is a short table of flaws a reader can see in a diff, each with one line on the fix. The skill opens a definition in `toby-code-review`'s `references/architecture.md` only when an entry seems to fire and the fix is unclear, because that file costs more than the skill. Each flaw found gets fixed before the handoff, and the tests run again.
- [x] Write the improvement step. In each file the change edited, find what made this change harder than it needed to be. Fix it when the fix stays in the files the change already edits, the existing tests cover it, and it runs as its own step before or after the feature code. List a larger fix as a follow-up with file:line.
- [x] Say when to skip the improvement step: on the quick-fix path in `toby-swd-strategy`, which includes a user who asked for the smallest diff, and in generated or vendored code. The design check never gets skipped.
- [x] Move the paragraph that starts "After the change, find one flaw" from `skills/toby-swd-strategy/SKILL.md` into the new skill, and leave a one-line pointer.
- [x] In `skills/toby-build/references/checks.md`, change the exception in the adjacent-feature entry and the uninvited-migration entry so both allow an improvement that `toby-swd-campfire` allows.
- [x] In `skills/toby-build/SKILL.md`, open `toby-swd-campfire` after each slice's proof, at both sizes. In `skills/toby-bug-fix/SKILL.md`, open it after the fix is proved, for the design check, and list its improvements as follow-ups so the fix stays small.
- [x] Add `toby-swd-campfire` to `build-tactical`, `build-strategic`, and `bug-fix` in `ROUTING_GROUPS`, to the matching scenarios in `scripts/token-budget.py`, and to the README.

### Verification

- Run `python3 evals/run.py gates`. The lost-rules gate fails if the moved paragraph has no survivor. Report each co-load group that passes the 5 percent growth gate, with its numbers.
- Trace a tactical change whose diff adds `if customer.tier == "gold"` inside a shared `price()` function through `toby-build`. The trace passes when the design check flags the special case and fixes it before the handoff. It fails when the handoff reports only the eight process red flags.
- Trace a bug fix in `parse_date` where the same date format string appears in three files. The trace passes when the fix stays in `parse_date` and the three copies get listed as one follow-up.
- Run `python3 scripts/voice-check.py --review` on every new or changed file, and read each sentence against the READ list.

If a check fails, stop and report it before Group 4.
