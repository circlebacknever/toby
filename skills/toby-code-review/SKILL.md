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

Validate the change, report the real risks, stop. Six confident-looking findings that turn out fake waste more time than the bug would have. Size the report to the change. A busy engineer should read it once and trust it.

**Flag, don't fix.** This skill reports and edits nothing. A bug or a security finding needs no routing, because the fix is the finding. A design or coverage finding names the skill that owns the fix, so the next agent starts where the evidence ends: `toby-swd-interfaces` for a contract, `toby-swd-modules` for placement, `toby-swd-complexity` for an error path or a cache, `toby-swd-testing` for coverage, `toby-swd-clarity` for a name or a comment, `toby-swd-strategy` for a design that got worse. `toby-simplify-code` owns behavior-preserving cleanup the user asked for.

## Disposition

- Precision over recall. A missed minor issue costs less than a finding that turns out fake or trivial. When unsure, drop it.
- A review with no findings is the normal result. It tells the next agent the diff is sound, which is a complete report.
- Prove, then report. The burden sits on the thing you want to say, so the default verdict is silence.
- Drop what you can't prove. A finding clears the bar and goes in plain, or it's cut. A hunch wrapped in "might possibly" is still noise.
- Never manufacture a finding to show effort, and never soften an empty result with "you might consider." An empty result is a result.

## Scope

- Default to the current diff when no scope is given.
- For a PR, inspect the PR metadata and diff with the tools available.
- Read the repo guidance and scoped instructions that apply to the changed files.
- Report issues the change introduces. When the cause is in the diff, follow it to the callers it affects even where they sit outside the diff. Pre-existing problems go in residual risk only when they bear on the change.

## Every finding is its own proof

Write each finding as three short lines. If you can't fill them from the file in front of you, there's no finding, so drop it.

- **Consequence** — what breaks and for whom, in plain words, at file:line: "returns last month's balance to a logged-in user on first load (api/account.ts:42)." Claim only what the trigger and path reach. If the path ends at a failed request, the consequence ends there. Data loss needs a path to the write.
- **Fires when** — the concrete input or state that triggers it, and the real caller, route, input, or test it comes from. If you can't name where the value comes from, you're guessing it can happen, so move it to a question or drop it.
- **Guard** — the check that should stop it and why it misses, quoted from the code, or "none — searched <where you looked>." Before writing this line, assume the code is right and you are wrong. Hunt for the guard that makes your finding fake, then say why it still fails. Most fake findings die here.

Run the changed code before writing findings, as a hunt for what you have missed. Run unasked what `toby-swd-environment` calls safe inspection or narrow verification: the changed function in a REPL, a scratch script, the one test file covering it. Ask before anything on that skill's ask-list: the full suite, a migration, an install, a dev server. Name the command you want and why, and say in the report which findings rest on reading alone.

Feed changed arithmetic and changed predicates the inputs a read glides over: negative, zero, empty, and the value either side of every boundary. Then paste what came back into the Consequence line. Sign errors, unit mismatches, and totals that disagree with what got stored surface here and appear in no catalog.

A design smell holds three different lines: the entry name from references/smells.md, the file:line, and the code there that meets the entry's Fires-when criterion. A smell costs future readers and future changes. Demanding a runtime consequence of it would therefore drop every real one or invent a consequence for it. The drop rule above still governs — three lines you can fill from the file, or there's no finding.

Add one line of fix direction when it isn't plain. Don't restate the code back, because they have the diff. Order findings by which bites hardest.

No P1/P2 labels. Severity is a claim about impact. The reviewer has the diff, without the roadmap, the incident history, or what ships Thursday. A consequence sentence is bounded by the path the reviewer traced, and a severity label by information they never had.

The author reads a P1 and answers "this is a nit, get over yourself", and they are the one who can tell. Order by which bites hardest and let the consequence sentence carry the weight.

If you've written more than three findings in one pass, stop and re-run the bar on each. Past a handful, suspicions slipped through.

## Four passes, each run to completion

Run them in this order. Each pass has its own bar and writes its own findings, so the fourth one gets the attention the first one did.

1. **Bugs and regressions.** What breaks, and for whom.
2. **Security.** Auth, authorization, injection, secrets, exposure.
3. **Compliance.** The change against what was agreed. Skip it when none of those artifacts exist.
4. **Design.** What the change cost the next person to touch this, and which document it left wrong.

The count ceiling below applies to each pass on its own. Three findings in the bugs pass leaves the compliance pass its own three.

### The compliance pass

Read the audit trail `toby-feature-dev` leaves, because a review of the diff alone reads half the change. Where acceptance criteria, a plan file, or a behavior record exist for this work, check three things and report what failed:

- Every acceptance criterion against the diff. A criterion with nothing in the diff serving it is the finding, quoted in its own pre-code wording.
- Every plan step against what landed. A step that ran differently from its approved wording, with no note saying it moved, is the finding.
- Every behavior-record sentence against the tests. A sentence the product claims with no test defending it is the finding, at the entry's heading.

None of the three needs a runtime consequence. The consequence is that the change and the agreement disagree, and the reviewer can quote both.

### The design pass

Ask whether the design is at least as good after the change as before it, which no other question here does. Sourced to `toby-swd-strategy`:

- What special case did this diff add, and which caller now has to know about it?
- What hidden dependency did it create — a decision in two modules, an ordering a caller must respect, a field layout two files agree on with nothing enforcing it?
- Which of these was cheaper to fix in this diff than it will ever be again?

One finding at most, at file:line, naming `toby-swd-strategy`. The author was already inside this question. Answering it is in scope. Reopening the design is not.

## What to catch

- Bugs: logic errors, null handling, race conditions, stale state, cleanup gaps, invalid assumptions, unreachable code, data loss.
- Regressions: a changed public contract, UI state, API shape, persistence, permissions, or workflow.
- Security: auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, data exposure.
- A swallowed or dropped error a caller needs to stay correct or recover.
- Missing coverage: new behavior or a regression path with no useful test, including a bug fix that ships without a regression test.
- A test asserting on internals that would break under a behavior-preserving refactor.
- A repo-rule break, only when the rule can be quoted at path:line. Proof sources are local guidance files, nearby code, the repo's own `SKILL.md` files, and its conventions and config files. Those files run the next agent, so breaking one costs what breaking a lint rule costs.
- A try/catch, guard, or validation for a condition already ruled out by the surrounding types, contract, or an earlier check, only when that proof can be quoted from the code.
- A new or changed public interface whose comment leans on call-order words ("first", "then", "after"), references internals, runs past four sentences, or leaves a caller unable to use it correctly from the comment alone.
- A structural change — a moved or split module, a changed public API, a cross-module decision — that leaves an existing AGENTS.md or README stale.
- A design smell matching a named entry in references/smells.md, only when the entry's criteria can be quoted against the code. Method length on its own and the bare presence of a comment stay non-findings no matter what the catalog calls them.

## Don't flag

- Method length on its own. A long method with a simple signature doing one coherent job is fine. Length is a finding only when it causes a named problem.
- An error the code deliberately makes impossible (validated upstream, unreachable by type) or correctly lets crash. Raise missing handling only when a real caller needs the signal.
- Code that's correct but over-built, awkwardly named, or non-idiomatic. If it doesn't match a named entry in references/smells.md, that's behavior-preserving cleanup, out of scope here. When a reader would trip on it, check the catalog's exception for whatever it resembles first. An exception that covers it means the code is right and you say nothing. Otherwise drop one pointer at the end — "cleanup candidate: file:line" — no severity, no argument. At most two. More than that means you're reviewing for taste. A match against a named entry there counts as a finding, covered under What to catch.
- Style nits a formatter or linter catches.

## A skills or config diff reviews differently

Review a change to a `SKILL.md`, an operating guide, a hook, or an agent config for what it does to every later run. Reading it as prose misses all of that. Three questions no other section asks:

- **Does this rule contradict another skill?** Quote both, at path:line. Two skills stating opposite rules is a finding whichever one is right.
- **Does a description edit change what fires?** A widened trigger noun loads a skill on tasks it should skip. A narrowed one drops it from tasks that need it. Name the task that now routes somewhere else.
- **Did a rule vanish while text moved?** Text moved between files reads as a tidy diff. Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent, and report any unmatched deletion at its old path:line.

## Final report

Match length to the change. A diff with nothing wrong gets one line: no findings, plus residual risk if any — named specifically, with why it stayed unverified. A trivial diff gets at most one finding. Then, in order, dropping any section that's empty:

1. Findings.
2. A question — something you'd ask the author, only when the answer needs information the code can't give (runtime config, an external service, product intent). Drop a hunch you couldn't prove, because it doesn't belong here.
3. A one-line change note, only when the diff's intent isn't plain from the diff.
4. A named test or verification gap, only when a real one exists.
