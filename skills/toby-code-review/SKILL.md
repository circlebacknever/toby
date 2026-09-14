---
name: toby-code-review
description: >-
  Report the real risks in a change the user asked about, and stop. Use it for code
  review, PR review, diff review, commit review, working-tree review, or findings on
  changed code: bugs, regressions, missing tests, security issues, and repo-rule breaks.
  It reports and does not repair. Skip it when the user asked for the code to be changed,
  which `toby-simplify-code` owns.
---

# Toby Code Review

Validate the change, report the real risks, and stop. Six confident-looking findings that turn out fake waste more time than the bug would have. Size the report to the change. A busy engineer should read it once and trust it.

**Flag, don't fix.** This skill reports and edits nothing. A bug or a security finding needs no routing, because the fix is the finding. A design or coverage finding names the skill that owns the fix, so the next agent knows which skill to load. The owners are `toby-swd-interfaces` for a contract, `toby-swd-modules` for placement, `toby-swd-complexity` for an error path or a cache, `toby-swd-testing` for coverage, `toby-swd-clarity` for a name or a comment, `toby-swd-strategy` for a design that got worse. `toby-simplify-code` owns behavior-preserving cleanup the user asked for.

## Disposition

- Favor precision over recall. A missed minor issue costs less than a finding that turns out fake or trivial. When unsure, drop it.
- A review with no findings is the normal result. It tells the next agent the diff is sound, which is a complete report.
- Prove a finding before you report it. Until you have that proof, the default is to report nothing.
- Drop what you can't prove. A finding that meets the bar goes in the report in plain words, and every other finding is cut. A hunch phrased as "might possibly" is still an unproven hunch.
- Never manufacture a finding to show effort, and never soften an empty result with "you might consider." An empty result is a valid report.

## Scope

- Default to the current diff when no scope is given.
- For a PR, inspect the PR metadata and diff with the tools available.
- Read the repo guidance and scoped instructions that apply to the changed files.
- Report issues the change introduces. When the cause is in the diff, follow it to the callers it affects even where they are outside the diff. List a pre-existing problem under residual risk only when it affects the change.

## Evidence for each finding

Write each finding as three short lines. If you can't fill them from the file in front of you, there's no finding, so drop it.

- **Consequence** — This line says in plain words what breaks and for whom, at file:line. An example is "returns last month's balance to a logged-in user on first load (api/account.ts:42)." Claim only what the trigger and path reach. If the path ends at a failed request, the consequence ends there. Data loss needs a path to the write.
- **Fires when** — This line names the concrete input or state that triggers the failure, and the real caller, route, input, or test that supplies it. If you can't name where the value comes from, you're guessing it can happen, so move it to a question or drop it.
- **Guard** — This line quotes the check that should stop the failure and says why the check misses. When no check exists, write one sentence that says so and names where you looked, such as "No check in the router or `api/middleware/` stops it." Before writing this line, assume the code is right and you are wrong. Hunt for the guard that makes your finding fake, then say why it still fails. Most fake findings fail at this step.

Run the changed code before writing findings, as a hunt for what you have missed. Run unasked what `toby-swd-environment` calls safe inspection or narrow verification: the changed function in a REPL, a scratch script, the one test file covering it. Ask before anything on that skill's ask-list: the full suite, a migration, an install, a dev server. Name the command you want and why, and say in the report which findings depend on reading alone.

Give changed arithmetic and changed predicates the inputs a quick read misses: negative, zero, empty, and the value either side of every boundary. Then paste what came back into the Consequence line. These inputs expose sign errors, unit mismatches, and totals that disagree with what got stored, and no catalog lists those bugs.

A design smell finding has three different lines: the entry name from `references/smells.md`, the file:line, and the code there that meets the entry's Fires-when criterion. A smell costs future readers and future changes. Demanding a runtime consequence of it would therefore drop every real one or invent a consequence for it. The drop rule above still applies, so fill all three lines from the file or drop the finding.

Add one line of fix direction when the fix isn't plain. Don't restate the code, because the author has the diff. Order findings by how much harm each one causes.

Leave off P1/P2 labels, because a severity label is a claim about impact. The reviewer has the diff, without the roadmap, the incident history, or what ships Thursday. A consequence sentence claims only what the traced path shows, but a severity label depends on information the reviewer never had.

The author reads a P1 and answers "this is a nit, get over yourself", and they are the one who can tell. Order by harm, and let the consequence sentence show the harm.

If you've written more than three findings in one pass, stop and check each one against the bar again. More than a handful of findings means the list includes unproven suspicions.

## Four passes, each run to completion

Run them in this order. Give each pass its own bar and its own findings, so the fourth pass gets the same attention as the first.

1. **Bugs and regressions.** Find what breaks, and for whom.
2. **Security.** Check auth, authorization, injection, secrets, and exposure.
3. **Compliance.** Check the change against what was agreed. Skip this pass when no acceptance criteria, plan file, or behavior record exists.
4. **Design.** Ask what the change cost the next person to touch this code, and which document it left wrong.

The count ceiling above applies to each pass on its own. Three findings in the bugs pass leaves the compliance pass its own three.

### The compliance pass

Read the audit trail `toby-feature-dev` leaves, because the diff alone shows only half the change. Where acceptance criteria, a plan file, or a behavior record exist for this work, check three things and report what failed:

- Check every acceptance criterion against the diff. When nothing in the diff serves a criterion, that criterion is the finding, quoted in its pre-code wording.
- Check every plan step against what the diff contains. A step that ran differently from its approved wording, with no note recording the change, is the finding.
- Check every behavior-record sentence against the tests. A record sentence that no test checks is the finding, reported at the entry's heading.

None of the three needs a runtime consequence. The consequence is that the change and the agreement disagree, and the reviewer can quote both.

### The design pass

Ask whether the design is at least as good after the change as before it, and no other question here asks that. These questions come from `toby-swd-strategy`:

- What special case did this diff add, and which caller now has to know about it?
- What hidden dependency did it create? Examples are a decision in two modules, an ordering a caller must respect, and a field layout two files share with nothing enforcing it.
- Which of these was cheaper to fix in this diff than it will ever be again?

Report at most one design finding, at file:line, and name `toby-swd-strategy` in it. The author already had to answer this question, so answering it is in scope, and reopening the design is out of scope.

## What to catch

- Bugs: logic errors, null handling, race conditions, stale state, cleanup gaps, invalid assumptions, unreachable code, data loss.
- Regressions: a changed public contract, UI state, API contract, persistence, permissions, or workflow.
- Security: auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, data exposure.
- A swallowed or dropped error a caller needs to stay correct or recover.
- Missing coverage: new behavior or a regression path with no useful test, including a bug fix that ships without a regression test.
- A test asserting on internals that would break under a behavior-preserving refactor.
- A repo-rule break, only when the rule can be quoted at path:line. Proof sources are local guidance files, nearby code, the repo's own `SKILL.md` files, and its conventions and config files. The next agent follows those files, so breaking one costs as much as breaking a lint rule.
- A try/catch, guard, or validation for a condition already ruled out by the surrounding types, contract, or an earlier check, only when that proof can be quoted from the code.
- A new or changed public interface whose comment relies on call-order words ("first", "then", "after"), references internals, runs past four sentences, or leaves a caller unable to use it correctly from the comment alone.
- A structural change — a moved or split module, a changed public API, a cross-module decision — that leaves an existing AGENTS.md or README stale.
- A design smell matching a named entry in `references/smells.md`, only when the entry's criteria can be quoted against the code. Method length on its own and the bare presence of a comment stay non-findings no matter what the catalog calls them.

## Don't flag

- Method length on its own. A long method with a simple signature doing one coherent job is fine. Length is a finding only when it causes a named problem.
- An error the code deliberately makes impossible (validated upstream, unreachable by type) or correctly lets crash. Raise missing handling only when a real caller needs the signal.
- Code that's correct but over-built, awkwardly named, or non-idiomatic. If the code doesn't match a named entry in `references/smells.md`, the fix is behavior-preserving cleanup and out of scope here. When the code would confuse a reader, first check the catalog's exception for the entry it resembles. An exception that covers it means the code is right and you say nothing. Otherwise add one pointer at the end, written as "cleanup candidate: file:line", with no severity and no argument. Add at most two pointers. More than that means you're reviewing for taste. A match against a named entry there counts as a finding, covered under What to catch.
- Style nits a formatter or linter catches.

## A skills or config diff reviews differently

Review a change to a `SKILL.md`, an operating guide, a hook, or an agent config for what it does to every later run. Reading it as prose misses those effects, so ask these three questions, which no other section asks:

- **Does this rule contradict another skill?** Quote both, at path:line. Two skills stating opposite rules is a finding whichever one is right.
- **Does a description edit change what fires?** A widened trigger noun loads a skill on tasks it should skip. A narrowed one drops it from tasks that need it. Name the task that now routes somewhere else.
- **Did a rule vanish while text moved?** Text moved between files reads as a tidy diff. Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent, and report any unmatched deletion at its old path:line.

## Final report

Match length to the change. A diff with nothing wrong gets one line that says there are no findings and names any residual risk. Name that risk specifically, and say why it stayed unverified. A trivial diff gets at most one finding. For any report longer than one line, write these sections in order, and drop any section that's empty:

1. Findings.
2. A question you'd ask the author, included only when the answer needs information the code can't give (runtime config, an external service, product intent). Drop a hunch you couldn't prove, because it doesn't belong here.
3. A one-line change note, only when the diff's intent isn't plain from the diff.
4. A named test or verification gap, only when a real one exists.
