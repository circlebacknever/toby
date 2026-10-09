# Toby's plan for the code review rewrite

Work mode: durable implementation. The review skill reports issues that are not there, in wording the user has to ask for again. It misses the architecture problems the user cares about.

The user wants each issue in this form, and "No issues found." when there are none:

```text
<issue>
<reproduction steps>
<1 specific way to fix the problem>
```

## Group 7: a review reports real issues in plain English, or says there are none

- [x] Rewrite the body of `skills/toby-code-review/SKILL.md` to under 1,600 tokens, in this order:
  - The report format comes first. Each issue says what goes wrong and for whom, in plain English, with file:line. Numbered reproduction steps follow, then one fix.
  - When no issue has reproduction steps, the report is "No issues found." A report adds nothing to it except a line naming any check that could not run.
  - An issue with no reproduction steps gets dropped. The skill gives one form of steps per kind of issue, in a short table:
    - For a bug, the steps are an input, a call, or a test that shows the wrong result.
    - For a bug fix with no regression test, the steps are to revert the fix and see the suite still pass.
    - For security, the steps are the request or input an attacker sends.
    - For an agreed criterion, the steps are its Check command and what comes back.
    - For architecture, the steps are the next change and each file:line it would edit. The next change comes from the request, a ticket, a TODO, or `git log` showing the same code gained a case in recent commits.
    - For production readiness, the steps are an operational scenario. An example is a request that fails, followed by the log search that finds no line naming the order.
  - "Run the changed code" and the boundary-input rule stay by name, because they produce the steps for a bug.
  - The guard search and the subagent recheck stay, because both remove false issues.
  - What to check: bugs, security, the agreed criteria or plan when one exists, and the four architecture areas the user picked. Those areas are module boundaries, extensibility, special cases and duplication, and production readiness.
  - The Don't-flag list stays short. It keeps the existing rule on rate limits and audit logs, because that rule came from the security review's exclusions. One sentence separates an audit log, which records who did what for compliance, from an outcome log, which records what a request did for the on-call engineer.
- [x] Remove the cleanup-candidate pointers, the labelled evidence lines, and the rule that runs every pass to completion. Keep the rule against severity labels. Each of these pushed the report toward listing something.
- [x] Move the entries in `references/smells.md` that belong to the four architecture areas into `references/architecture.md`, under one heading per area. Leave the other entries, such as magic numbers and stale comments, in `smells.md` for `toby-refactor`. Keep each entry's wording, so the lost-rules gate can match it.
- [x] Add production-readiness entries to `architecture.md`. They cover a new entry point with no log of its outcome, a secret or personal data in a log line, a flag checked in more than one place or with no removal step, and a service that keeps state on local disk. Each entry points to the skill with the fix.
- [x] Point `toby-swd-campfire` and the SOLID mapping in `toby-swd-extensibility/references/solid.md` at `architecture.md`. `toby-refactor` keeps reading `smells.md`.
- [x] Add a review suite to `evals/suites/` for the eval the overview proposes. The correct diff contains bait that today's skill tends to report: a three-case `switch` that has not changed in a year, a five-parameter function called with named arguments, and a long method that does one job. Its expected report is "No issues found." The second diff has a planted bug, with its expected reproduction steps.
- [x] Ask the user to agree to running that suite, with three Sonnet 5.5 writers per arm and an Opus 5.5 grader. The rewrite deletes rules on purpose, so it stays unverified until that run.

### Verification

- Run `python3 evals/run.py gates`. Show the user every lost rule from the old review body, because the rewrite removes rules on purpose, and run `record` only after the user approves the list.
- Trace the bait diff from the new suite through the rewritten skill. The trace passes when the report is "No issues found." and fails when it lists anything.
- Trace a review of a diff that adds a fourth `case "platinum"` to a tier `switch` copied in `pricing.py` and `invoice.py`. The diff's `git log` shows the `switch` gained `gold` two months ago. The trace passes when the issue's reproduction steps say that the next tier means editing both files, at their file:line, with one fix. It fails when the issue uses a smell name the user would have to look up.
- Trace a review of a diff that adds `log.info(f"login {email} {password}")`. The trace passes when the issue is reported with the input that writes the password to the log.
- Run `python3 scripts/voice-check.py --review` on every new or changed file, and read each sentence against the READ list.

Stop here and report the result, the gate numbers, and the lost-rules list to the user.
