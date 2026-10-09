# Toby's plan for adding the missing engineering skills

Work mode: durable implementation.

Toby's engineering skills cover design, unit tests, and error paths. They leave out the topics in the table below. The code review skill also reports issues that are not there, in wording the user has to ask for again.

## Gaps in the current skills

Each row says what the skills say today, so a later reader can see why each change exists.

| Gap | What the skills say today |
| --- | --- |
| Logging and observability | No skill covers structured logs, metrics, or traces. `toby-swd-errors` says to "log the detail" at the top-level handler and stops there. |
| Feature flags | `toby-build` puts a slice behind a flag that is off by default when the slice depends on a later one. Nothing covers where the flag check goes, testing both paths, or removing the flag. |
| Production hardening and twelve-factor | No skill asks for input bounds, idempotent writes, graceful shutdown, health checks, or stateless processes. `toby-swd-errors` covers timeouts and retries, and `toby-swd-interfaces/references/runtime-config.md` covers config. |
| Extensibility | `toby-swd-modules/references/solid.md` maps each SOLID name to a check. The growing-conditional section sits inside `toby-swd-modules`, and `toby-build` opens that skill only when the design adds a module. |
| End-to-end tests | `toby-swd-testing` covers unit tests and test doubles. `toby-build` requires each slice to be observable at an entry point, and no skill says how to test through that entry point. |
| Plan structure | The guide's Plan Format asks for "one coherent unit of work" per group and a verification block of checks. It does not ask for slices, rule out checks that cannot fail, or say when a plan splits into files. |
| Design of new and changed code | All eight red flags in `toby-build/references/checks.md` check process. Tactical work opens `toby-swd-modules` only for a new module, and `toby-swd-strategy` limits cleanup to "one flaw" in the touched code. |
| Code review | `toby-code-review` runs four passes "each to completion", adds up to two cleanup pointers, and writes findings as labelled evidence lines. The user wants each issue in plain English with reproduction steps and one fix, and "No issues found" when there are none. |

## Changes

Each new skill is a hidden method skill with a short body. An entry skill opens it by path at the step that needs it.

| Change | Opened by | Covers |
| --- | --- | --- |
| Plan Format in `base/toby.md` | every plan | one slice per group, checks that can fail, one file per group for long plans |
| `toby-swd-e2e`, new | `toby-build` for strategic slices, `toby-swd-testing` | one test per slice through the real entry point, and one test that walks through the whole feature |
| `toby-swd-campfire`, new | `toby-build` at both sizes, `toby-bug-fix` | a design check on the diff after its tests pass, and improvements to the code the change touched |
| `toby-swd-extensibility`, split from `toby-swd-modules` | `toby-build`, `toby-swd-strategy`, `toby-swd-modules`, `toby-refactor`, `toby-code-review` | the growing conditional, composition, and the SOLID checks |
| `toby-swd-observability`, new | `toby-build`, `toby-bug-fix`, `toby-code-review` | structured logs, metrics, and traces |
| `toby-swd-production`, new | `toby-build`, `toby-code-review` | hardening by kind of code, and the twelve-factor process rules that the other skills leave out |
| `toby-swd-flags`, new | `toby-build`, `toby-code-review` | flag kinds, one check site, tests for both paths, and removal |
| `toby-code-review`, rewritten | a review request | the user's issue format, a report with no issues as the expected result, and the four architecture areas the user picked |

Hardening and twelve-factor share one skill because both apply to the same code, a process that runs in production. Config, logs, and disposability already have homes in `runtime-config.md`, `toby-swd-observability`, and the shutdown section of `toby-swd-production`.

## Size

- `toby-build` moves its Ambiguity section to `references/ambiguity.md` and its flag sentences to `toby-swd-flags`, so its body grows by less than 10 percent with the new method lines.
- `toby-swd-modules` loses about 630 tokens to `toby-swd-extensibility`.
- `toby-code-review` drops from 2,706 body tokens to under 1,600.
- `toby-code-review`'s `references/smells.md`, at about 4,679 tokens, splits into `references/architecture.md` for the four areas the review checks and `smells.md` for the local-cleanup entries `toby-refactor` reads.
- `toby-swd-interfaces` at 2,652 tokens stays as it is in this pass. Splitting it is a follow-up.

Measured co-load totals on 2026-10-08, after the implementation. The new skill bodies measure 642 to 758 tokens, and `toby-swd-extensibility` measures 832, of which about 630 moved from `toby-swd-modules`.

| Group | Before | After | 5 percent gate |
| --- | --- | --- | --- |
| `build-tactical` | 6,211 | 6,692 | 6,522, fails |
| `build-strategic` | 17,202 | 18,573 | 18,062, fails |
| `build-service`, new | none | 18,872 | none, ceiling 19,000 |
| `bug-fix` | 5,210 | 6,645 | 5,470, fails |
| `review` | 6,676 | 4,902 | holds |

`build-strategic` grows by `toby-swd-e2e` and `toby-swd-campfire`. The text that moves to `toby-swd-extensibility` was already counted inside `toby-swd-modules`. `bug-fix` grows by the design check and the observability skill.

## Constraints

- Every new skill reads like a person wrote it, with short sections and concrete examples. Each rule exists in one skill, and other skills point to it.
- Every new or changed file passes `scripts/voice-check.py --review` and its READ list.
- `toby-swd-errors` keeps timeouts and retries, and `runtime-config.md` keeps the config module design. The new skills point to them.
- Rules that `toby-build` requires the design to cover count as part of a criterion. `checks.md` says so, so the Don't-build list does not drop them as adjacent features.
- Each group updates `ROUTING_GROUPS`, the token scenarios, and the README for its own skill. The co-load ceiling of 19,000 stays. A co-load group that grows past the 5 percent gate gets reported, and `python3 evals/run.py record` runs only after the user approves the numbers and the lost-rules list.
- Nothing gets committed, and `scripts/install.sh` does not run, because both need the user's approval.
- No eval run starts without the user's agreement. The Evals section proposes one.
- The user asked for the plan to be reviewed and then implemented in one pass. Each verification block still runs, and a block that fails stops the work.

## Groups

1. [`01-plan-rules.md`](01-plan-rules.md) puts slices and checks that can fail into the guide's Plan Format.
2. [`02-end-to-end-tests.md`](02-end-to-end-tests.md) adds `toby-swd-e2e`.
3. [`03-design-after-green.md`](03-design-after-green.md) adds `toby-swd-campfire`.
4. [`04-extensibility.md`](04-extensibility.md) splits `toby-swd-extensibility` out of `toby-swd-modules`.
5. [`05-production-code.md`](05-production-code.md) adds `toby-swd-observability` and `toby-swd-production`.
6. [`06-feature-flags.md`](06-feature-flags.md) adds `toby-swd-flags`.
7. [`07-code-review.md`](07-code-review.md) rewrites `toby-code-review`.

## Checks in this plan

Each group ends with the repo gates and with traced requests. A trace is a request that the author reads through the skill text. It catches a missing step or a wrong pointer, and it cannot show what a model does with the text. The eval below measures that.

## Evals, proposed

This run waits for the user's agreement.

- Question: does a writer that reads the new skills produce plans, code, and reviews that meet the checklists below, where a writer on `HEAD` does not?
- Arms: the skills on `HEAD` against this branch, because the new skills are unproven.
- Writers: Sonnet 5.5, three per arm per task.
- Tasks: a webhook endpoint that marks orders paid, a queue consumer that writes to Postgres, a fourth customer tier added to a pricing `switch`, and two reviews, one of a diff with a planted bug and one of a correct diff.
- Grader: Opus 5.5, one pass per output.
- Measures: checklist items met, plan checks that cannot fail, paperwork lines, false issues on the correct diff, and whether the planted bug got reported with reproduction steps.
