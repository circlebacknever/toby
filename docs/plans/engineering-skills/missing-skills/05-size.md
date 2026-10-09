# Group 5: the large method skills are cut to about 1,000 words

This group meets criterion 7 in the overview. Its owner edits `skills/toby-swd-interfaces/**` other than `references/runtime-config.md`, `skills/toby-swd-modules/**`, `skills/toby-swd-testing/**`, and `skills/toby-explain/**`.

## Steps

- [x] Cut `skills/toby-swd-interfaces/SKILL.md` from 1,759 words to about 1,000. Delete the restated deep-module definition, the step that only points to `toby-swd-modules`, and the closing paragraph that repeats the modules red flags. Move "Make interfaces somewhat general-purpose" to `references/general-purpose.md`, and open it from the step that compares designs. Point the config sentence at `toby-swd-twelve-factor`'s `references/config.md`, and drop runtime-config from the reference list. Cite each step by its heading, because the numbers change.
- [x] Cut `skills/toby-swd-modules/SKILL.md` from 1,720 words to about 1,100. Move "Writing a placement note" to `references/placement-note.md`, and name that file in the body. Keep the check numbers, so pointers in other files stay right. Shorten the red-flag list to the entries that are not already checks. Point the placement default at `toby-swd-architecture`.
- [x] Cut `skills/toby-swd-testing/SKILL.md` from 1,197 words to about 950. Move "Failing tests" and the flaky-test advice to `references/failing-tests.md`, and open it from the body for a failing or flaky test. Delete the red flags that repeat the body.
- [x] Add one Coverage line to `toby-swd-testing` for a behavior whose entry point no test drives, such as a route or a job. The line says to add a test through that entry point and open `toby-swd-e2e`. Keep the sentence "Cover the success path, each documented failure mode, and the boundary conditions, then stop." word for word, because `tests/test-gates.py` deletes it as a test case.
- [x] In `skills/toby-explain/SKILL.md`, open `toby-swd-modules`' `references/placement-note.md` for where code goes. Add routing lines for structure, extensibility, flags, logs and metrics, hardening, and twelve-factor. Keep the body under 866 tokens.

## Audit fixes

- [x] The Red flags section of `toby-swd-interfaces` again sends the reader to checks 1, 2, 4, and 8 in `toby-swd-modules`. The first cut deleted that pointer, so a changed signature skipped those checks.
- [x] In `toby-swd-testing`, a mock replaces the function in the one module that calls the provider, as `toby-swd-architecture` says. The rule that put each mock on an adapter class went, because `toby-build`'s `references/checks.md` forbids a one-implementation wrapper.
- [x] In `toby-swd-testing`, "an in-memory database" became the production engine, run locally or in a container. The sentence that allowed a fake of the application's database went too, because `toby-swd-twelve-factor` asks for the production kind of database in tests.
- [x] In `toby-swd-modules`' `references/databases.md`, the repository sentence applies only when the repo already has repositories. The file opens with the Django and Rails rule from `toby-swd-architecture`.
- [x] The reference lists in `toby-swd-interfaces` and `toby-swd-modules` say to skip the platform file when none matches the repo's framework, as for Django.

- [x] Treat a view or webhook whose request and response the framework or provider sets as a routine interface, so it gets one design and one comment test. Open `toby-swd-e2e` from testing only for a new entry point, and propose a new harness only in strategic work or when the user asks.

## Removed on purpose

- Duplicate text only. Each cut sentence either repeats a sentence in the same skill or in the skill its pointer names.
- In `toby-swd-interfaces`, the red flag "Comment fails the test" went, because the opening paragraph already says to redesign an interface whose comment cannot stay short.
- In `toby-swd-interfaces`, the config paragraph went, because `toby-swd-twelve-factor`'s `references/config.md` states the same rules and the body names that file.
- In `toby-swd-interfaces`, "Hiding any of these is a defect" and "In that case the fields are the interface" went, because the sentence before each one says the same thing.
- In `toby-swd-modules`, the cost-and-benefit framing of a deep module went, because the first paragraph of `toby-swd-interfaces` says to keep the interface much smaller than the functionality behind it.
- In `toby-swd-modules`, the two sentences that name the single-responsibility principle went, because check 1 keeps the rule they explain.
- In `toby-swd-modules`, "A module has more callers than authors" went, because it only gave the reason for check 3.
- In `toby-swd-modules`, the "Repeated rule" red flag went, because check 7 merges a duplicated rule. The growing-conditional red flag went, because checks 5 and 6 name `toby-swd-extensibility`, which has the same rule.
- In `toby-swd-testing`, the red flags for a test named for a call, an unread snapshot update, and a bug fix with no regression test went, because the Names, Assertions, and Test-first sections state each rule.

## Verification

- Run `wc -w` on every engineering `SKILL.md`. A body over 1,150 words, other than `toby-build` and `toby-code-review`, fails this group.
- Run `grep -rn "Cheap path first\|references/runtime-config.md" skills/toby-swd-interfaces skills/toby-swd-modules skills/toby-swd-testing skills/toby-explain`. A hit fails this group.
- Give an Opus subagent the HEAD and new versions of the three cut skills and ask it to quote any rule that is in neither the new body nor a reference the body opens. A rule it quotes that the group file does not list as removed fails this group.
- Run `python3 tests/test-gates.py` and `python3 scripts/validate-skills.py`. A failure in either, or an error in an owned file, fails this group.
