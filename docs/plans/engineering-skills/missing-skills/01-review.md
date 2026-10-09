# Group 1: a review reports plain issues or "No issues found."

This group meets criteria 1 and 2 in the overview. Its owner edits `skills/toby-code-review/**`, `skills/toby-refactor/**`, `evals/fixtures/review-*`, `evals/suites/review.md`, and the review prompt in `evals/run.py`.

## Steps

- [x] Copy `skills/toby-code-review/references/architecture.md` to the session scratchpad before any edit.
- [x] Rewrite `skills/toby-code-review/SKILL.md` to under 1,300 words. Keep the parts the audit found right: the report format, "No issues found." as the expected result, dropping an issue that has no steps, the per-kind steps table, no severity labels, running the changed code, boundary inputs, the guard search, and the subagent recheck.
- [x] Write the design questions in the skill under the four headings the user picked. Keep only questions whose steps can end in a wrong result:
  - Module boundaries:
    - a rule that decides an outcome, such as a price, a limit, or a status change, written in an entry point when a second entry point needs the same rule
    - code that writes another module's data and skips a rule that module enforces
    - one decision, such as a format or a status list, written in two modules
  - Extensibility:
    - a switch or if-chain on a type, kind, status, or provider, when another switch on the same field exists and has a default branch
    - a subclass or implementation that breaks what its parent promises
  - Special cases and duplication:
    - a branch for one caller, customer, or input inside shared code
    - a rule written twice where the copies can drift apart
  - Production readiness, for new entry points, jobs, consumers, and outbound calls:
    - a write in a webhook, consumer, job, or payment that runs twice on retry
    - an input with no size limit and no framework limit in front of it
    - an outbound call with no timeout
    - a database write plus a message or call that a crash between them leaves half done
    - a message or stored format the previous release cannot read
    - a migration that drops or renames a column the running release reads, or locks a large table
    - data kept in one process that a request served by another instance must read
    - a new state-changing entry point with no outcome log, where its sibling handlers log one
    - a secret or personal data written to a log
- [x] Give each question one line on when to leave the code alone. Include the carve-outs the plan review found: a lookup by id scoped to the caller belongs in the handler, a sibling view may repeat that lookup, and two switches that compute different values stay separate.
- [x] Add two checks outside the four areas: a break of a rule written in the repo's agent instructions file, such as `AGENTS.md`, quoted at path:line, and a new route, job, or consumer that no test drives through its entry point. Name no coding tool in the skill, because the validator rejects tool names there.
- [x] Make the steps for a design issue end in a wrong result. The reviewer makes the next change in the obvious place only, then shows what the place it missed does wrong. For a module boundary or extensibility issue, the next change comes from the request, a ticket, a TODO, or `git log`. When none of those shows a next change, the issue gets dropped. A special case or a copied rule needs no written next change, because its steps can change one copy or add a second customer with the same need.
- [x] Add a second example to the Report section, a design issue in the same three-part form, in a domain other than customer tiers. Its fix is one change, such as an exhaustive match that fails the type check until every case is handled.
- [x] Allow at most one `Question:` line, for a fact in a file the reviewer cannot read or a product decision. Add one `Not run:` line that lists the issues that come from reading alone. Neither line counts as an issue.
- [x] Add the rule that one cause gets one issue, however many questions point at it.
- [x] Narrow the hardening exclusion to a missing rate limit or audit log the diff did not remove. Add "a pattern the repo uses in every sibling, copied correctly" to Don't report.
- [x] When the fix is unclear, open the method skill that covers it. List those skills one per line, with `toby-swd-architecture` for structure and `toby-swd-hardening` for production checks.
- [x] Add a row for skill and guide changes to the steps table, and change "finding" to "issue" in `references/skills-diff.md`.
- [x] Rewrite `skills/toby-refactor/references/smells.md` as plain entries with no "Fires when" or "Exception" labels. Keep only cleanups inside one module, and bring back the local entries the earlier pass moved out: the flag argument, the long parameter list, the message chain, feature envy, getters and setters, and primitive obsession. Point `toby-refactor` and `references/cleanup.md` at `smells.md` alone.
- [x] In `skills/toby-refactor/SKILL.md`, open `toby-swd-architecture` for a split, merge, move, or extraction, and add `toby-swd-extensibility` to the out-of-scope routing list.
- [x] Delete `skills/toby-code-review/references/architecture.md` after `smells.md` holds the local entries.
- [x] Fix `evals/fixtures/review-clean.diff` so it is correct. Add a test that requests another account's receipt and gets 404. Give `status_label` a case for every status the model allows. Keep the tax base at zero or above.
- [x] Add `evals/fixtures/review-tier.diff`, which adds a `platinum` case to a tier switch in `pricing.py` while `invoice.py` has its own switch on tier with a default branch. Add `evals/fixtures/review-tier-log.txt` with the `git log -p` excerpt that shows `gold` added to both switches two months earlier.
- [x] Move the production-readiness questions to `references/production.md`, which `SKILL.md` opens for an entry point, job, consumer, outbound call, migration, or format change. This keeps `SKILL.md` under 1,300 words by `wc -w`.
- [x] Remove the hide-tax option from `evals/fixtures/review-clean.diff`, because its false branch let a reviewer ask a product question on a correct change.
- [x] Update `evals/suites/review.md` with what passes on each fixture, and point the review prompt in `evals/run.py` at `SKILL.md` alone.

## Removed on purpose

- The 22-entry catalog in `references/architecture.md`, because its labels are the wording the user could not read and its style entries produced issues on correct code.
- The rule to report an entry whenever its "Fires when" line matches, because the steps rule replaces it.
- Shallow module, pass-through method, divergent change, artificial coupling, speculative generality, shotgun surgery, and fat interface as review checks. Their steps cannot end in a wrong result. `toby-swd-modules` and `toby-swd-extensibility` still cover them when code gets written.
- A dependency built inside domain code, a flag parameter, and a provider type passed past its module, as review checks, for the same reason. The design check in `toby-swd-architecture` catches them during a build.
- A flag read in more than one file, because both reads see the same value, so the steps cannot end in a wrong result. `toby-swd-flags` keeps the rule.
- The definitions of an audit log and an outcome log in Don't report, because the outcome-log question now says in plain words what the log holds.
- A separate leave-alone line under each production question. One line now skips any production question that the code, the framework, or middleware already handles, because those questions share that case. The questions with their own case keep a line.
- The per-kind steps table as a table. Each kind of issue in "What to check" now states its own steps, because the table repeated each kind's label. The steps for a skill or guide change moved to `references/skills-diff.md`, beside the questions they prove.
- `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-errors`, `toby-swd-observability`, `toby-swd-flags`, `toby-swd-testing`, and `toby-swd-twelve-factor` as rows in the review's fix table, because the word limit left room for four rows. `toby-swd-architecture` and `toby-swd-hardening` point to the method skills behind their areas.
- The line to write each issue as you would explain it at the author's desk, in short sentences. The opening line asks for plain English, and the first Report bullet asks for the names the code uses.
- The fallback "or cite the function name" for a line number the reviewer cannot count, and the note that boundary inputs find sign errors and unit mismatches, to keep the skill under the word limit.
- The magic-number line that says to report a literal already quoted for another finding, because the review no longer reads `smells.md`.
- The feature-envy condition that the method could be a method of the other object, and the long-parameter note that a count alone proves nothing. The fix line and the leave-alone line of each entry now state those cases.
- In `review-clean.diff`, the tax computed from the subtotal at render time. The receipt now shows the stored `order.tax_cents`, because a receipt that recomputes tax at today's rate can disagree with the tax charged. With no tax computed, the receipt has no tax base that can go below zero.

## Verification

- Run `grep -rniE "fires when|diff-visible|\*\*exception" skills/toby-code-review skills/toby-refactor`. Any hit fails this group.
- Give an Opus subagent `skills/toby-code-review/SKILL.md` and `evals/fixtures/review-clean.diff`, and ask it to quote every sentence of the skill that could lead to an issue or a question on that diff. A quoted sentence that holds up when Toby reads it fails this group.
- Give a second subagent the skill, `evals/fixtures/review-tier.diff`, and `review-tier-log.txt`. It fails this group when it can quote sentences that lead to two issues for the one cause, to steps that stop at a list of files, or to a fix with two options.
- Give a third subagent the skill and ask it to mark every word a reader must look up before following a question. A marked word that has no plain replacement in the text fails this group.
- Run `python3 scripts/validate-skills.py`. An error in an owned file fails this group.
