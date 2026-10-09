# Toby's plan for slice-based plan rules

Work mode: durable implementation. Plans cut work by layer, verify things that cannot fail, and put a multi-session plan in one long file that is hard to review.

## Group 1: every plan cuts groups by slice and checks what can fail

- [x] In the Plan Format section of `base/toby.md`, replace "one coherent unit of work each" with a rule that each group is one vertical slice. A slice ends in something a person can run or see that they could not before. A group named for a layer, such as "database changes", gets cut again. A refactor that keeps behavior may be its own group, proved by the tests that already exist.
- [x] Replace the verification-block rule. Each check is a command or an action with the result that means it failed. A check that passes whether or not the work is right gets left out, such as "the file exists", "grep finds the new line", or "the code compiles".
- [x] Add a rule for long plans. A plan with more than three groups, or one that will take more than one session, is an `overview.md` plus one file per group. The overview has the mode, the problem, the criteria, and the design, and finishing a group file finishes a slice.
- [x] In the Skill Routing section, replace the sentence that lists six hidden skills with one sentence that covers every hidden method skill, so a new method skill needs no guide edit.
- [x] Run `bash scripts/sync.sh`, `bash scripts/sync.sh --check`, and `python3 tests/test-voice-hook.py`, because the hooks read `base/toby.md` on every run.
- [x] In `skills/toby-build/references/strategic.md`, cut each sentence of "The plan document" that the guide now states, and keep the step-detail rules that are specific to a build.

### Verification

- Run `python3 evals/run.py gates`. The lost-rules gate fails when a sentence cut from `strategic.md` has no survivor in the guide.
- Run `python3 scripts/token-budget.py` and compare the resident total with the run before this group. The guide may grow by at most 150 tokens.
- Trace "make a plan to add CSV export to the reports page, across a few sessions" through the guide's Plan Format. The trace passes when it gives an overview file plus one file per slice, and fails when it allows one file or a group named "backend".
- Read this plan's own seven group files against the new rules. A group whose verification has a check that cannot fail gets rewritten before Group 2 starts.
- Run `python3 scripts/voice-check.py --review` on `base/toby.md`, and read each changed sentence against the READ list.

If a check fails, stop and report it before Group 2.
