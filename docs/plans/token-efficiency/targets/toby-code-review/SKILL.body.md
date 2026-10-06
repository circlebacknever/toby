# Toby Code Review

**Report problems and do not fix them.**

**Write every finding so a reader without these skills can act on it**, because the author often does not have the Toby skills installed. State the fix in plain engineering words, and never name a Toby skill or a skill-only term in the report, such as "reactive pass" or "comment test". Use the skills yourself to decide the fix: `toby-swd-interfaces` for a contract, `toby-swd-modules` for placement or depth, `toby-swd-complexity` for an error path or a cache, `toby-swd-testing` for coverage, `toby-swd-clarity` for a name or a comment, and `toby-swd-strategy` for a design that got worse.

## Disposition

- Report only a finding that fills the three evidence lines below, and drop every other one, because a fake finding costs the reader more than a missed minor issue. Writing a hunch as "might possibly" does not prove it.
- A review with no findings is a complete report. Never invent a finding to show effort, and never add "you might consider" to an empty result.

## Scope

- Default to the current diff when no scope is given.
- For a PR, read its title and description before the diff.
- Read the repo guidance and scoped instructions that apply to the changed files.
- Report issues the change introduces. When the cause is in the diff, follow it to the callers it affects even where they are outside the diff. List a pre-existing problem under residual risk only when it affects the change.

## Evidence for each finding

Write each finding as three labelled lines, filled from the file you are reviewing.

- **Consequence** — This line says in plain words what breaks and for whom, at file:line. An example is "The account page returns last month's balance to a logged-in user on first load (api/account.ts:42)." Claim only the effects that the trigger and path can cause. If the path ends at a failed request, the consequence ends there. Claim data loss only when the path includes the write.
- **Fires when** — This line states the input or state that triggers the failure, and the real caller, route, input, or test that supplies it. If you can't show where the value comes from, you're guessing it can happen, so move it to a question or drop it.
- **Guard** — This line quotes the check that should stop the failure and says why the check misses. When no check exists, write one sentence that says so and lists where you looked, such as "The router and `api/middleware/` have no check that stops it." Before writing this line, assume the code is right and you are wrong. Search for the guard that would make your finding fake, and then say why that guard still fails. When the guard could be in a file you cannot read, such as authentication middleware or settings, ask the author a question and report no finding.

Run the changed code before writing findings, within what `toby-swd-environment` allows without asking. Use a REPL call, a scratch script, or the one test file that covers the change. Ask before anything broader, and state the command and why. In the report, say which findings depend on reading alone.

Give changed arithmetic and changed predicates the inputs a quick read misses: negative, zero, empty, and the value either side of every boundary. Then paste what came back into the Consequence line. These inputs reveal sign errors, unit mismatches, and totals that disagree with what got stored.

A design smell finding has four lines. They are the entry name from `references/smells.md`, the file:line, the code that meets the entry's Fires-when criterion, and the fix. Write the fix from the entry's Fix line, applied to this code. The entry names are standard smell names that a reader can look up. A smell finding needs no runtime consequence, because a smell costs future readers and future changes. Fill all four lines from the file or drop the finding.

State the fix in one sentence, or as a code block when five lines or fewer at one site fix the whole issue. Do not quote the current code back, because the author has the diff. Check the fix against the diff before writing it. A fix that deletes a method an interface requires, or a method a caller uses, breaks the code, so the finding is wrong. Cite line numbers only from the diff's hunk headers, and cite the function name when you cannot count the line.

Leave off severity labels such as P1 or P2. Severity depends on the roadmap, the incident history, and the release plan, which the reviewer does not have. Let the Consequence line show the harm.

Before the report, recheck every finding. When you can start a subagent, give it one finding and the changed files, and ask it for the guard that makes the finding wrong. Report only the findings the recheck confirms.

## Four passes, each run to completion

Run them in this order. Give each pass its own standard of proof and its own findings, so the fourth pass gets the same attention as the first.

1. **Bugs and regressions.** Find what breaks, and for whom, including a changed public contract, persisted format, permission, or workflow. Report a swallowed error a caller needs, and a bug fix with no regression test. Report other new behavior that no test asserts only when the repo's guidance requires tests. Report a test asserting on internals that a behavior-preserving refactor would break.
2. **Security.** Check auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, and data exposure.
3. **Compliance.** Check the change against what was agreed. Skip this pass when no acceptance criteria or plan file exists.
4. **Design.** Ask what the change cost the next person to touch this code, and which document it left wrong.

### The compliance pass

Where acceptance criteria or a plan file exist for this work, check three things and report what failed:

- Check every acceptance criterion against the diff. When nothing in the diff meets a criterion, report that criterion as the finding, quoted in the wording it had before coding started.
- Check every plan step against what the diff contains. A step that ran differently from its approved wording, with no note recording the change, is the finding.
- Check the plan's design block against the diff. A module, boundary, or signature that the diff builds differently from the block, with no note recording the change, is the finding.

Write a compliance finding as the criterion, plan step, or design line quoted in its agreed wording, and the diff's file:line that departs from it. It needs no runtime consequence.

### The design pass

Ask whether the design is at least as good after the change as before it. Ask these questions of each new or changed module and signature:

- What special case did this diff add, and which caller now has to know about it?
- What hidden dependency did it create? Examples are a decision in two modules, an ordering a caller must respect, and a field layout two files share with nothing enforcing it.
- Does the change break a SOLID principle? `toby-swd-modules`' `references/solid.md` maps each principle to its check. Report the break under the matching entry in `references/smells.md`, and write the principle's name in the finding.

Also report these:

- A repo-rule break, only when the rule can be quoted at path:line. Proof sources are local guidance files, nearby code, the repo's own `SKILL.md` files, and its conventions and config files.
- A try/catch, guard, or validation for a condition already ruled out by the surrounding types, contract, or an earlier check, only when that proof can be quoted from the code.
- A new or changed public interface whose comment relies on call-order words ("first", "then", "after"), references internals, or is longer than four sentences. Report it too when a caller cannot use it correctly from the comment alone.
- A structural change, such as a moved or split module, a changed public API, or a cross-module decision, that leaves an existing AGENTS.md or README stale.
- A design smell matching an entry in `references/smells.md`, only when the entry's criteria can be quoted against the code.

Use the smell format when an entry in `references/smells.md` matches. Otherwise use the three evidence lines, with the Consequence line stating what the next change will cost. When a plan's design block approved a choice, report it only where the diff differs from the block.

## Don't flag

- Method length on its own.
- An error the code deliberately makes impossible (validated upstream, unreachable by type) or correctly lets crash. Raise missing handling only when a real caller needs the signal.
- Code that's correct but over-built, awkwardly named, or non-idiomatic. If the code doesn't match an entry in `references/smells.md`, the fix is behavior-preserving cleanup and out of scope here. When the code would confuse a reader, first check the catalog's exception for the entry it resembles. If an exception covers it, the code is right, so say nothing. Otherwise add one pointer at the end, written as "cleanup candidate: file:line", with no severity and no argument. Add at most two pointers.
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
