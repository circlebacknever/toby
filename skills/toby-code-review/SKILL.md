---
name: toby-code-review
description: >-
  Reports the proven risks in a change and edits nothing. Use it when the user
  asks to review, check, or audit a diff, a PR, a commit, a branch, or the
  working tree. Use it when the user asks what is wrong with a change. Skip it
  when the user wants the code changed, which toby-refactor or toby-bug-fix
  covers. Skip it for a question about how code works, which toby-explain
  covers.
---

# Toby Code Review

**Report problems and do not fix them.**

**Write every finding so a reader without these skills can act on it**, because the author often does not have the Toby skills installed. State the fix in plain engineering words, and never name a Toby skill or a skill-only term in the report, such as "reactive pass" or "comment test". Use the skills yourself to decide the fix: `toby-swd-interfaces` for a contract, `toby-swd-modules` for where code belongs and how much a module hides behind its interface, `toby-swd-errors` for an error path, `toby-optimize` for a cache, `toby-swd-testing` for coverage, `toby-swd-clarity` for a name or a comment, and `toby-swd-strategy` for a design that got worse. When a finding's fix depends on one of those skills, open its SKILL.md by path.

## What to report

- Report only a finding that fills the three evidence lines below, and drop every other one, because a false positive costs the reader more than a missed minor issue. Writing a hunch as "might possibly" does not prove it.
- A review with no findings is a complete report. Never invent a finding to show effort, and never add "you might consider" to an empty result.

## Scope

- Default to the current diff when no scope is given.
- For a PR, read its title and description before the diff.
- Read the repo guidance and scoped instructions that apply to the changed files.
- Report issues the change introduces. When the cause is in the diff, follow it to the callers it affects even where they are outside the diff. List a pre-existing problem under residual risk only when it affects the change.

## Evidence for each finding

Write each finding as three labelled lines, filled from the file you are reviewing.

- **Consequence.** This line says in plain words what breaks and for whom, at file:line. An example is "The account page returns last month's balance to a logged-in user on first load (api/account.ts:42)." Describe only the effects that the triggering input can cause as it moves through the code. If the code stops at a failed request, describe only the failed request. Claim data loss only when that code path writes the bad data to storage.
- **Fires when.** This line states the input or state that triggers the failure, and the real caller, route, input, or test that supplies it. If you cannot show which caller, route, or test supplies the triggering input, the failure is a guess. Ask the author about it as a question, or drop the finding.
- **Guard.** This line quotes the check that should stop the failure and says why the check misses. When no check exists, write one sentence that says so and lists where you looked, such as "The router and `api/middleware/` have no check that stops it." Before writing this line, assume the code is right and you are wrong. Search for a check that would prevent the failure and prove your finding wrong. If you find one, say why it still does not stop the failure. When the guard could be in a file you cannot read, such as authentication middleware or settings, ask the author a question and report no finding.

Run the changed code before writing findings, using only commands that `toby-swd-environment` lists as safe to run without asking. Use a REPL call, a scratch script, or the one test file that covers the change. Ask before anything broader, and state the command and why. In the report, say which findings depend on reading alone.

Test changed arithmetic and changed conditions with the inputs a quick read misses. Use negative values, zero, empty values, and the values just above and below every boundary. Then paste what came back into the Consequence line. These inputs reveal sign errors, unit mismatches, and totals that disagree with what got stored.

A design smell finding has four lines. They are the entry name from `references/smells.md`, the file:line, the code that meets the entry's Fires-when criterion, and the fix. Write the fix from the entry's Fix line, applied to this code. The entry names are standard smell names that a reader can look up. A smell finding needs no runtime consequence, because a smell costs future readers and future changes. Fill all four lines from the file or drop the finding.

State the fix in one sentence, or as a code block when five lines or fewer at one site fix the whole issue. Do not quote the current code back, because the author has the diff. Check the fix against the diff before writing it. A fix that deletes a method an interface requires, or a method a caller uses, breaks the code, so the finding is wrong. Work out each line number by counting from the starting line in the diff's hunk header. When you cannot count it, cite the function name.

Leave off severity labels such as P1 or P2. Severity depends on the roadmap, the incident history, and the release plan, which the reviewer does not have. Let the Consequence line show the harm.

Before the report, recheck every finding. When you can start a subagent, give it one finding and the changed files, and ask it for the guard that makes the finding wrong. Report only the findings the recheck confirms.

## Four passes, each run to completion

Run them in this order. Apply each pass's own evidence rules and keep its findings separate, so the fourth pass gets the same attention as the first.

1. **Bugs and regressions.** Find what breaks, and for whom, including a changed public contract, persisted format, permission, or workflow. Report an error that the code catches and hides when a caller needs to see it. Report a bug fix that has no regression test. When the repo's guidance requires tests, also report any other new behavior that no test checks. Report a test asserting on internals that a behavior-preserving refactor would break.
2. **Security.** Check auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, and data exposure.
3. **Compliance.** Check the change against what was agreed. Skip this pass when no acceptance criteria or plan file exists.
4. **Design.** Ask what the change cost the next person to touch this code, and which document it left wrong.

### The compliance pass

Where acceptance criteria or a plan file exist for this work, check three things and report what failed:

- Check every acceptance criterion against the diff. When nothing in the diff meets a criterion, report that criterion as the finding, quoted in the wording it had before coding started.
- Check every plan step against what the diff contains. When the diff implements a plan step differently from its approved wording, with no note recording the change, report that step.
- Check the plan's design section against the diff. When the diff builds a module, boundary, or signature differently from that section, with no note recording the change, report it.

Write a compliance finding as the criterion, plan step, or design line quoted in its agreed wording, and the diff's file:line that departs from it. It needs no runtime consequence.

### The design pass

Ask whether the design is at least as good after the change as before it. Ask these questions of each new or changed module and signature:

- What special case did this diff add, and which caller now has to know about it?
- What hidden dependency did it create? Examples are the same decision coded in two modules, a call order the caller must follow, and a data layout two files rely on with no shared definition.
- Does the change break a SOLID principle? `toby-swd-modules`' `references/solid.md` maps each principle to its check. Report the break under the matching entry in `references/smells.md`, and write the principle's name in the finding.

Also report these:

- A repo-rule break, only when the rule can be quoted at path:line. Proof sources are local guidance files, nearby code, the repo's own `SKILL.md` files, and its conventions and config files.
- A try/catch, guard, or validation for a condition already ruled out by the surrounding types, contract, or an earlier check, only when that proof can be quoted from the code.
- A new or changed public interface whose comment relies on call-order words ("first", "then", "after"), references internals, or is longer than four sentences. Report it too when a caller cannot use it correctly from the comment alone.
- A structural change, such as a moved or split module, a changed public API, or a cross-module decision, that leaves an existing AGENTS.md or README stale.
- A design smell matching an entry in `references/smells.md`, only when the entry's criteria can be quoted against the code.

Use the smell format when an entry in `references/smells.md` matches. Otherwise use the three evidence lines, with the Consequence line stating what the next change will cost. When the plan's design section already approved a design choice, report that choice only where the diff departs from the plan.

## Don't flag

- Method length on its own.
- An error that cannot happen because earlier code validates the input or the types rule it out, and an error the code correctly lets crash the program. Report missing error handling only when a real caller needs to know the error happened.
- Code that's correct but over-built, awkwardly named, or non-idiomatic. If the code doesn't match an entry in `references/smells.md`, the fix is behavior-preserving cleanup and out of scope here. When the code would confuse a reader, find the closest entry in `references/smells.md` and read that entry's list of cases where the smell is acceptable. If one of those cases covers the code, say nothing. Otherwise add one pointer at the end, written as "cleanup candidate: file:line", with no severity and no argument. Add at most two pointers.
- Style nits a formatter or linter catches.
- A missing hardening measure, such as a rate limit or an audit log, unless the diff removed it. Treat environment variables and CLI flags as trusted input.

When the diff changes a `SKILL.md`, an operating guide, a hook, or an agent config, also ask the three questions in `references/skills-diff.md`.

## Final report

Report a diff with nothing wrong in one line. That line says there are no findings, states any residual risk, and says why that risk stayed unverified. For a longer report, write these sections in order, and drop any section that's empty:

1. Findings, ordered by harm across all passes.
2. Residual risk, which covers pre-existing problems that affect the change, what was not run, and which findings depend on reading alone.
3. A question for the author, only when the answer needs information the code can't give, such as runtime config, an external service, or product intent.
4. A one-line change note, only when the diff's intent isn't plain from the diff.
5. Cleanup candidates, at most two, each written as "cleanup candidate: file:line".
