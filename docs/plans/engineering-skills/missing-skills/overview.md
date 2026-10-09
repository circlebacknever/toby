# Toby's plan for finishing the missing engineering skills

Work mode: durable implementation. An earlier pass added six method skills and a new review skill, and it left the user's main complaints in place.

## What done means

1. A review of a correct diff says "No issues found." Each real issue is one plain-English line at file:line, numbered steps that end in the wrong result, and one fix. The review loads no file with "Fires when", "Exception", "diff-visible", or a smell name used as a heading.
2. The review checks the four areas the user picked in the earlier session: module boundaries, extensibility, special cases and duplication, and production readiness. It also checks for a break of a written repo rule and for a new entry point that no test drives. It keeps only the questions whose steps can end in a wrong result.
3. A build that adds or moves a business rule, a write, or an outbound call reads a default structure before it writes code. A read-only entry point with no rule follows the code around it. The structure says where parsing, rules, data access, and wiring go. It maps each part to the repo's framework. The build checks the finished diff against a design check kept in the same skill.
4. A build that edits existing code looks for the refactor that makes the change easy before the first edit. It does that refactor when the refactor stays in the files the feature would edit anyway, plus at most one new module. Anything larger becomes a follow-up.
5. Logging, flags, hardening, twelve-factor, extensibility, end-to-end tests, and plan writing each have one short method skill. An entry skill opens each one at the step where the model writes that kind of code or plan. Every rule in them holds up as engineering advice for a small app and a large one.
6. A multi-session plan is a folder with an overview and one file per slice. Each group's verification starts with a check that can fail, and a plan for a feature ends with one test through the whole feature.
7. `toby-build` and `toby-code-review` stay under 1,300 words, and every other engineering skill body stays under about 1,100.
8. Every new or changed sentence reads as if an engineer wrote it, and passes `voice-check.py --review`.
9. A small change in a one-instance app with one developer gets the smallest code that meets its criteria. Each layer, flag, retry, harness, metric, and plan step applies only under a condition that the change meets, and the safeguards a larger app needs stay in place.

## Why new code comes out poorly structured

The earlier plan said flaws creep in while the code is written. Reading the skill text shows the structure gets chosen before any code exists. These causes are listed in the order I judge their effect, from reading the text:

1. No skill says where a feature's parts go. The design pass compares two approaches by "where the complexity is", and a discount rule in the checkout view ties with a discount rule in a pricing module. The model writes its first idea.
2. `toby-swd-modules`, the placement skill, opens only when the design "adds a module". The model decides that after it has already picked the placement, so a model whose first idea is inline code never opens the skill.
3. Small work has no path for a refactor before the feature. `checks.md` lets a reorganization through only when an approved plan lists it, and tactical work has no plan.
4. `toby-build` calls most work "tactical", and `toby-swd-strategy` uses "tactical path" for a deadline shortcut. A model told its work is tactical can read the second meaning as permission.
5. Discovery tells the model to copy the sibling feature. The check on that sibling looks for abstract smells, so a sibling with its rules in the route handler passes and gets copied.
6. The "Don't build" list forbids "a new module in front of a single implementation", which reads as forbidding a pricing module pulled out of a fat view.
7. Of the 2,624 words in `toby-build`, 61 are about design. `evals/suites/feature-dev.md`, the suite that tuned it, scores sizing and process.

`toby-swd-campfire`, the check the earlier plan added after the tests pass, stays because it catches what gets through. Restructuring costs the most at that point, so the default structure has to come before the code.

## Design

| Skill | Change | Opened by |
| --- | --- | --- |
| `toby-swd-architecture` | New. The default structure for feature code, mapped to the repo's framework, and the design check for a finished diff. | `toby-build` when the change adds or moves a rule, entry point, write, or outbound call; `toby-bug-fix` when the fix moves a rule; `toby-refactor` for a split or move; `toby-swd-campfire` after the tests pass |
| `toby-swd-campfire` | Reworked. Takes "Existing code" from `toby-swd-strategy` as its refactor-first step, and runs the design check after the tests pass. | `toby-build`, `toby-bug-fix` |
| `toby-code-review` | Rewritten. Its questions live in the skill as plain questions, each with the steps that prove it. `references/architecture.md` goes. | a review request |
| `toby-swd-hardening` | Renamed from `toby-swd-production`. Adds outbound calls, poison messages, dual writes, and deploys where two releases run at once. | `toby-build`, `toby-optimize` |
| `toby-swd-twelve-factor` | New. Each factor with the way a diff breaks it. Takes shutdown and two-instance safety from hardening, and `runtime-config.md` from `toby-swd-interfaces`. | `toby-build` for a new process, worker, scheduler, config value, secret, or backing service |
| `toby-swd-plan` | New. Slices, the plan folder, steps, and checks that can fail, with the example plan. | `toby-build` at the plan step, `toby-bug-fix` and `toby-refactor` when they write a plan |
| `toby-swd-observability`, `toby-swd-flags`, `toby-swd-e2e`, `toby-swd-extensibility` | Engineering fixes from the audit, such as the flag data steps and loop logging. | as today, with wider triggers |
| `toby-build` | Cut to about 1,200 words. Each method skill opens inside the step that uses it. | a build request |
| `toby-swd-interfaces`, `toby-swd-modules`, `toby-swd-testing` | Cut to about 1,000 words each. Repeats go, and rarely used sections move to references. | as today |

## One home for each rule

| Rule | Home | Others point to it |
| --- | --- | --- |
| Where parsing, rules, data access, and wiring go | `toby-swd-architecture` | `toby-swd-modules`, `toby-build` |
| The design check on a finished diff | `toby-swd-architecture` | `toby-swd-campfire` |
| Refactor before the change, and improving touched code | `toby-swd-campfire` | `toby-swd-strategy`, `toby-build`, `references/checks.md` |
| Search for where the repo computes a rule before writing one | `toby-swd-architecture` | `toby-build` |
| The growing conditional and its options | `toby-swd-extensibility` | `toby-swd-modules`, `toby-swd-architecture` |
| Schema changes across releases | `toby-swd-hardening` | `toby-swd-flags` |
| Shutdown, two instances, and state kept in the process | `toby-swd-twelve-factor` | `toby-swd-hardening` |
| The outcome log, and what never to log | `toby-swd-observability` | `toby-swd-hardening`, `toby-swd-architecture` |
| Plan layout and verification checks | `toby-swd-plan`, with a short version in the operating guide | `toby-build` |

The review keeps its own questions, because each one is written as the steps that prove an issue. The design check tells a builder what to fix, so the two lists have different wording.

## Other gaps considered

- API versioning is covered by the Brownfield Work section of `toby-swd-interfaces`, which keeps a public surface compatible.
- Data migrations across releases go into the Deploys section of `toby-swd-hardening` in this pass.
- Dependency upgrades, accessibility, and performance budgets stay out of this pass because the user did not list them. `toby-optimize` covers measured performance work.

## Constraints

- Text that moves keeps its meaning. Each group file lists the text it cut, with the reason, in plain sentences.
- `python3 scripts/validate-skills.py` runs at the end of each group, and an error fails the group. `python3 evals/run.py gates` runs once at the end. Its report goes to the user. `record` waits for the user's approval.
- Nothing gets committed, and `scripts/install.sh` does not run.
- No writer runs, because the user agrees each eval design first. Every check here is a read-only audit by a subagent that quotes the sentence it objects to. The final report proposes the writer runs.
- Files from the earlier pass move to `docs/plans/engineering-skills/first-pass/` or the session scratchpad, so nothing is lost.
- The user asked for this plan to run through without stopping. Each group's verification still runs, and a failed check sends the work back to that group.

## Order and owners

Groups 1 to 5 edit different files, so they run in parallel. The skill names, file names, and section names in this plan are fixed, so each owner can point at another group's files before they exist. Group 6 runs last.

| File | Slice | Owner's files | Status |
| --- | --- | --- | --- |
| [01-review.md](01-review.md) | A review reports plain issues or "No issues found." | `toby-code-review`, `toby-refactor`, review fixtures | done |
| [02-structure.md](02-structure.md) | A build places each part of a feature, improves what it touches, and checks the diff | `toby-swd-architecture`, `toby-swd-campfire`, `toby-swd-strategy`, `toby-swd-extensibility`, `toby-bug-fix` | done |
| [03-build.md](03-build.md) | `toby-build` is short and writes plans as folders of slices | `toby-build`, `toby-swd-plan`, the operating guide | done |
| [04-production.md](04-production.md) | Production code gets hardening, twelve-factor, logging, and flag rules that hold up | hardening, twelve-factor, observability, flags, e2e, errors, optimize | done |
| [05-size.md](05-size.md) | The large method skills are cut to about 1,000 words | `toby-swd-interfaces`, `toby-swd-modules`, `toby-swd-testing`, `toby-explain` | done |
| [06-whole.md](06-whole.md) | One held-out feature request reads correctly through every skill it opens | routing tables, README, plan files | done |
