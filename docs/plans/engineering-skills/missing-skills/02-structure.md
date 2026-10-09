# Group 2: a build places each part of a feature, improves what it touches, and checks the diff

This group meets criteria 3 and 4 in the overview. Its owner edits `skills/toby-swd-architecture/**`, `skills/toby-swd-campfire/**`, `skills/toby-swd-strategy/**`, `skills/toby-swd-extensibility/**`, and `skills/toby-bug-fix/**`.

## Steps

- [x] Create `skills/toby-swd-architecture/SKILL.md` as a hidden method skill of about 700 words, with `agents/openai.yaml` laid out like `toby-swd-campfire`'s. It has two sections, "Default structure" and "Design check", which other skills cite by those names.
- [x] Open "Default structure" with the rule to follow the repo's own split when the sibling feature has one. The default applies when the repo has none, or when the sibling keeps its rules in the handler. Describe each part as a job, then say where it goes in common frameworks:
  - The entry point, such as a route, view, CLI command, consumer, or job, authenticates the caller, parses input into a typed value, calls one operation, and maps the result to a response. It may load the record it acts on by id, scoped to the caller, in the framework's usual form. It writes the outcome log when it changes state or calls another service, unless middleware already does.
  - The operation is named for the business action. It holds each rule that decides an outcome, such as a price, a limit, a permission on this record, or a status change. In Django or Rails that is a model method or a function in a `services` module that calls the ORM directly.
  - The module that owns a table or a third-party API is the only code that writes it. Code outside that module calls an operation such as `order.mark_paid()`. The module that calls a provider turns the provider's types into the repo's own.
  - The composition root builds the clients from config. In Django it is settings, in Flask the app factory, and in a Lambda the module scope. Pass a client in only when it crosses the network and the tests cannot patch it. Freeze time with the test tool the repo uses, such as freezegun or fake timers, and add no clock parameter.
- [x] Add the rule that each price, limit, status change, or format is computed in one function that every caller calls. Before writing one, search for where the repo computes that kind of value and cite it. When the repo computes it in an entry point, the new rule goes in an operation, and the old code moves there within campfire's limits.
- [x] Add one paragraph that keeps the default small. A three-line rule goes in a function beside the repo's other rules. It needs no new service class, repository, or interface. A library takes its clients from the caller. UI code follows `toby-swd-modules`' `references/web.md`.
- [x] Give two short examples in domains that the verification requests do not use, one for an Active Record framework and one for an Express webhook. Put them in `references/examples.md`, opened when a part's place is unclear, so the build-service group stays under its token ceiling. The Rails example wraps its guarded update in `with_lock`. The webhook example verifies the signature on the raw body before it parses.
- [x] Write "Design check" as a short list of plain questions for a finished diff, each with a fix. Cover these flaws:
  - a rule in an entry point
  - code that writes another module's data
  - a branch for one caller in shared code
  - a boolean parameter that switches between two jobs
  - a rule written twice
  - a switch on a type that a second switch repeats
  - a network client or environment read built inside an operation
  - a provider type passed past its module
  - a read, a check, and a write on a row that two requests can change at once
- [x] Rework `skills/toby-swd-campfire/SKILL.md` into "Before the first edit" and "After the tests pass".
  - Before the first edit, look for the refactor that makes the change easy. Do it first, as its own step, when it stays in the files the feature would edit anyway plus at most one new module for a moved rule. State it in `toby-build`'s design lines or the plan before the first edit. When no test covers that code, write a characterization test first. When that test would take longer than the feature, list the refactor as a follow-up.
  - After the tests pass, run the design check in `toby-swd-architecture`, fix what it finds, and run the tests again. When the touched lines have an unclear name, dead branch, or wrong comment, fix one, or list it as a follow-up. When the user asked for the smallest diff, list each fix as a follow-up and leave the code as asked. In a planned build, add each fix to the plan file as a step before making it.
- [x] Move the "Existing code" section of `skills/toby-swd-strategy/SKILL.md` into campfire's first part, and leave a one-line pointer. Replace "tactical path" and "tactical version" with "shortcut" in strategy's SKILL.md and `references/examples.md`, including the "Tactical vs Strategic" heading. The shortcut needs its own word because `toby-build` uses "tactical" for most work. Change strategy's opening line so the bar is code left easier to change. Fix the "Cheap path first" pointer to name the interfaces step by its heading.
- [x] In `skills/toby-swd-extensibility/SKILL.md`, say the skill applies to new code that branches on a type, kind, status, or provider. When two switches on the same field compute different values, make each one exhaustive, with `assert_never`, a sealed type, or a map whose test checks every value. Merge them only when both compute the same value. Rename option 1 to "Move the branch onto the type". Apply the human-voice fixes from the audit to the opening and the inheritance section.
- [x] Rewrite `skills/toby-swd-extensibility/references/solid.md` as five short entries. Give each entry one question, answered in the file, and drop the table that points at review entries.
- [x] In `skills/toby-bug-fix/SKILL.md`, open `toby-swd-architecture` when the fix moves a rule. Add a log line only when finding the cause needed production state that the logs did not record. Keep campfire's improvements as follow-ups, so the fix stays small. Keep the body within 10 percent of its 650-token baseline.

- [x] Narrow the triggers in campfire, architecture, strategy, refactor, and bug-fix so a small change gets no refactor, design comparison, or log line it does not need. A refactor first now needs a problem from campfire's list and a test that already covers the code. A read-only entry point with no rule follows the code around it.

## Removed on purpose

- Campfire's eight-row table, because the design check in `toby-swd-architecture` replaces it and a second copy would drift.
- "Report each improvement with the number it reduced", because the user asked for a qualitative judgment. The report says what the next change no longer has to touch.
- Campfire's rows for one detail used in two modules, a function that mixes a business step with low-level detail, and a name that describes how the code works. `toby-swd-modules` check 2, `toby-refactor`'s `references/smells.md`, and `toby-swd-clarity` cover them.
- The clock in campfire's dependency row and in the dependency-inversion entry of `solid.md`, because `toby-swd-architecture` freezes time with the repo's test tool and adds no clock parameter.
- Campfire's pointer to `toby-code-review`'s `references/architecture.md` for an unclear fix, because group 1 deletes that file and each design-check question now states its fix.
- Campfire's opening sentence "Code drifts from its plan while it is written", because the audit read it as a slogan and the opening now states the rule.
- Extensibility's sentence "Move to the next option only when the case bodies are substantial", because it overlapped "stop at the first one that fits" and the fit line of option 4.
- Extensibility's pointer to the wrapper entry in `toby-build`'s `references/checks.md`, because it cited a label from another file. The paragraph now states what an unused extension point costs a reader.
- Extensibility's rule that a repeated conditional in existing code is always a separate refactor, because it contradicted campfire. Campfire's limits now decide when that refactor runs first.
- "Keep it to one map" in `references/replace-the-conditional.md`, because two maps that compute different values stay apart. The reference now types each map so the compiler reports a missing kind.
- Strategy's rule to "offer the smallest local refactor that makes the change fit, with its cost and benefit, before doing it". Criterion 4 in the overview has the build run a refactor inside campfire's limits with no wait for the user, once the design lines state it. A larger refactor still goes to the user as a follow-up with its cost.
- The second and third sentences of `toby-bug-fix`'s opening, which explained why a symptom fix is wrong. The red flag about a branch for one input keeps the rule. The cut keeps the body within its 715-token limit.

## Verification

Each check gives an Opus subagent the skills `toby-build` would open, and asks it to quote the sentences that would lead to the bad result. A quoted sentence that holds up when Toby reads it fails this group.

- The request is "add a refund limit so support agents cannot refund more than $500 without a manager" in a FastAPI app whose refund route computes the refund inline. The check fails when no sentence moves the limit out of the route, or nothing requires one function for the limit.
- The request is "add a Rails job that cancels subscriptions whose card failed three times". The check fails when no sentence keeps the status change in the model, or when a sentence would add a repository or a clock parameter.
- The request is "return `created_at` in the order detail JSON" in a small Django app. The check fails when a sentence would add a module, a class, a repository, an interface, or a parameter.
- Give `evals/fixtures/review-clean.diff` to the design check. The check fails when any question in it matches that diff.
- Run `python3 scripts/validate-skills.py`. An error in an owned file fails this group.
