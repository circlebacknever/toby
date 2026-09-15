---
name: toby-code-review
description: >-
  Report the real risks in a change the user asked about, and stop. Use it for code
  review, PR review, diff review, commit review, working-tree review, or findings on
  changed code: bugs, regressions, missing tests, security issues, and repo-rule breaks.
  It reports findings and makes no edits to the code. Skip it when the user asked for the code to be changed,
  which `toby-simplify-code` is for.
---

# Toby Code Review

Validate the change, report the real risks, and stop. Six findings that look confident but turn out fake waste more time than the bug itself. Size the report to the change. A busy engineer should read it once and trust it.

**Report problems and do not fix them.** This skill reports and edits nothing. A bug or a security finding does not name a skill for the fix, because the finding already states the fix. A design or coverage finding names the skill for the fix, so the next agent knows which skill to load. The skills for these fixes are `toby-swd-interfaces` for a contract, `toby-swd-modules` for placement, `toby-swd-complexity` for an error path or a cache, `toby-swd-testing` for coverage, `toby-swd-clarity` for a name or a comment, `toby-swd-strategy` for a design that got worse. `toby-simplify-code` is for behavior-preserving cleanup the user asked for.

## Disposition

- Favor precision over recall. A missed minor issue costs less than a finding that turns out fake or trivial. When unsure, drop it.
- A review with no findings is the normal result. It tells the next agent the diff is sound, which is a complete report.
- Prove a finding before you report it. Until you have that proof, the default is to report nothing.
- Drop what you can't prove. Report a finding that meets the standard of proof in plain words. Cut every other finding. Phrasing a hunch as "might possibly" does not prove it.
- Never invent a finding to show effort. Never add "you might consider" to an empty result. An empty result is a valid report.

## Scope

- Default to the current diff when no scope is given.
- For a PR, inspect the PR metadata and diff with the tools available.
- Read the repo guidance and scoped instructions that apply to the changed files.
- Report issues the change introduces. When the cause is in the diff, follow it to the callers it affects even where they are outside the diff. List a pre-existing problem under residual risk only when it affects the change.

## Evidence for each finding

Write each finding as three labelled lines, and make each line a whole sentence. If you can't fill them from the file you are reviewing, there's no finding, so drop it.

- **Consequence** — This line says in plain words what breaks and for whom, at file:line. An example is "The account page returns last month's balance to a logged-in user on first load (api/account.ts:42)." Claim only the effects that the trigger and path can cause. If the path ends at a failed request, the consequence ends there. Claim data loss only when the path includes the write.
- **Fires when** — This line names the concrete input or state that triggers the failure, and the real caller, route, input, or test that supplies it. If you can't name where the value comes from, you're guessing it can happen, so move it to a question or drop it.
- **Guard** — This line quotes the check that should stop the failure and says why the check misses. When no check exists, write one sentence that says so and names where you looked, such as "No check in the router or `api/middleware/` stops it." Before writing this line, assume the code is right and you are wrong. Search for the guard that would make your finding fake, and then say why that guard still fails. Most fake findings fail at this step.

Run the changed code before writing findings, so you find what you have missed. Run unasked what `toby-swd-environment` calls safe inspection or narrow verification: the changed function in a REPL, a scratch script, the one test file covering it. Ask before anything on that skill's ask-list: the full suite, a migration, an install, a dev server. Name the command you want and why. In the report, say which findings depend on reading alone.

Give changed arithmetic and changed predicates the inputs a quick read misses: negative, zero, empty, and the value either side of every boundary. Then paste what came back into the Consequence line. These inputs reveal sign errors, unit mismatches, and totals that disagree with what got stored. No catalog lists those bugs.

A design smell finding has three different lines: the entry name from `references/smells.md`, the file:line, and the code there that meets the entry's Fires-when criterion. A smell costs future readers and future changes. So if you demand a runtime consequence for a smell, you will drop every real smell or invent a consequence for it. The drop rule above still applies, so fill all three lines from the file or drop the finding.

When the fix isn't plain, add one sentence that says how to fix it. Don't restate the code, because the author has the diff. Order findings by how much harm each one causes.

Leave off P1/P2 labels, because a severity label is a claim about impact. The reviewer has the diff but not the roadmap, the incident history, or what ships Thursday. A consequence sentence claims only what the traced path shows, but a severity label depends on information the reviewer never had.

The author reads a P1 and answers "this is a nit, get over yourself". The author is the one who can tell how severe it is. Let the consequence sentence show the harm.

If you've written more than three findings in one pass, stop and check each one against the standard of proof again. More than a handful of findings means the list includes unproven suspicions.

## Four passes, each run to completion

Run them in this order. Give each pass its own standard of proof and its own findings, so the fourth pass gets the same attention as the first.

1. **Bugs and regressions.** Find what breaks, and for whom.
2. **Security.** Check auth, authorization, injection, secrets, and exposure.
3. **Compliance.** Check the change against what was agreed. Skip this pass when no acceptance criteria, plan file, or behavior record exists.
4. **Design.** Ask what the change cost the next person to touch this code, and which document it left wrong.

The three-finding limit above applies to each pass on its own. Three findings in the bugs pass still allow three findings in the compliance pass.

### The compliance pass

Read the audit trail `toby-feature-dev` leaves, because the diff alone shows only part of the change. Where acceptance criteria, a plan file, or a behavior record exist for this work, check three things and report what failed:

- Check every acceptance criterion against the diff. When nothing in the diff meets a criterion, report that criterion as the finding, quoted in the wording it had before coding started.
- Check every plan step against what the diff contains. A step that ran differently from its approved wording, with no note recording the change, is the finding.
- Check every behavior-record sentence against the tests. A record sentence that the tests do not check is the finding, reported at the entry's heading.

None of the three needs a runtime consequence. The consequence is that the change and the agreement disagree. The reviewer can quote both.

### The design pass

Ask whether the design is at least as good after the change as before it, which only this pass asks. These questions come from `toby-swd-strategy`:

- What special case did this diff add, and which caller now has to know about it?
- What hidden dependency did it create? Examples are a decision in two modules, an ordering a caller must respect, and a field layout two files share with nothing enforcing it.
- Which of these was cheaper to fix in this diff than it will ever be again?

Report at most one design finding, at file:line, and name `toby-swd-strategy` in it. The author already had to answer this question, so answering it is in scope. Reopening the design is out of scope.

## What to catch

- Bugs: logic errors, null handling, race conditions, stale state, cleanup gaps, invalid assumptions, unreachable code, data loss.
- Regressions: a changed public contract, UI state, API contract, persistence, permissions, or workflow.
- Security: auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, data exposure.
- A swallowed or dropped error a caller needs to stay correct or recover.
- Missing coverage: new behavior or a regression path with no useful test, including a bug fix that ships without a regression test.
- A test asserting on internals that would break under a behavior-preserving refactor.
- A repo-rule break, only when the rule can be quoted at path:line. Proof sources are local guidance files, nearby code, the repo's own `SKILL.md` files, and its conventions and config files. The next agent follows those files, so breaking one costs as much as breaking a lint rule.
- A try/catch, guard, or validation for a condition already ruled out by the surrounding types, contract, or an earlier check, only when that proof can be quoted from the code.
- A new or changed public interface whose comment relies on call-order words ("first", "then", "after"), references internals, is longer than four sentences, or leaves a caller unable to use it correctly from the comment alone.
- A structural change — a moved or split module, a changed public API, a cross-module decision — that leaves an existing AGENTS.md or README stale.
- A design smell matching an entry in `references/smells.md`, only when the entry's criteria can be quoted against the code. Method length on its own and the presence of a comment are not findings, whatever the catalog says about them.

## Don't flag

- Method length on its own. A long method with a simple signature doing one coherent job is fine. Length is a finding only when it causes a named problem.
- An error the code deliberately makes impossible (validated upstream, unreachable by type) or correctly lets crash. Raise missing handling only when a real caller needs the signal.
- Code that's correct but over-built, awkwardly named, or non-idiomatic. If the code doesn't match an entry in `references/smells.md`, the fix is behavior-preserving cleanup and out of scope here. When the code would confuse a reader, first check the catalog's exception for the entry it resembles. If an exception covers it, the code is right, so say nothing. Otherwise add one pointer at the end, written as "cleanup candidate: file:line", with no severity and no argument. Add at most two pointers. More than that means you're reviewing for taste. A match against an entry in the catalog counts as a finding, as What to catch describes.
- Style nits a formatter or linter catches.

## How to review a skills or config diff

Review a change to a `SKILL.md`, an operating guide, a hook, or an agent config for what it does to every later run. Reading it as prose misses those effects, so ask these three questions. Only this section asks them:

- **Does this rule contradict another skill?** Quote both, at path:line. Two skills stating opposite rules is a finding whichever one is right.
- **Does a description edit change what fires?** A widened trigger noun makes the agent load a skill on tasks it should skip. A narrowed trigger noun stops the agent from loading the skill on tasks that need it. Name the task that now routes somewhere else.
- **Did a rule vanish while text moved?** A diff that moves text between files looks tidy. Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent, and report any unmatched deletion at its old path:line.

## Final report

Match length to the change. A diff with nothing wrong gets one line that says there are no findings and names any residual risk. Name that risk specifically, and say why it stayed unverified. A trivial diff gets at most one finding. For any report longer than one line, write these sections in order, and drop any section that's empty:

1. Findings.
2. A question you'd ask the author, included only when the answer needs information the code can't give (runtime config, an external service, product intent). Drop a hunch you couldn't prove, because it doesn't belong here.
3. A one-line change note, only when the diff's intent isn't plain from the diff.
4. A named test or verification gap, only when a real one exists.
