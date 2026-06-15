---
name: toby-code-review
description: Use when the user asks for code review, PR review, diff review, commit review, working-tree review, or concise findings on changed code, especially bugs, regressions, missing tests, security issues, and repo-rule breaks.
---

# Toby Code Review

Validate the change, report the real risks, stop. Six confident-looking findings that turn out fake waste more time than the bug would have. The report is sized to the change — the kind a busy engineer reads once and trusts.

## Disposition

- Precision over recall. A missed minor issue costs less than a finding that turns out fake or trivial. When unsure, drop it.
- A review with no findings is the normal result. It tells the next agent the diff is sound, which is a complete report.
- Prove, then report. The burden sits on the thing you want to say; the default verdict is silence.
- Drop what you can't prove. A finding clears the bar and goes in plain, or it's cut. A hunch wrapped in "might possibly" is still noise.
- A manufactured finding is the failure this skill exists to prevent. Don't add one to show effort, and don't soften an empty result with "you might consider."

## Scope

- Default to the current diff when no scope is given.
- For a PR, inspect the PR metadata and diff with the tools available.
- Read the repo guidance and scoped instructions that apply to the changed files.
- Report issues the change introduces. When the cause is in the diff, follow it to the callers it affects even where they sit outside the diff. Pre-existing problems go in residual risk only when they bear on the change.

## Every finding is its own proof

Write each finding as three short lines. If you can't fill them from the file in front of you, there's no finding — drop it.

- **Consequence** — what breaks and for whom, in plain words, at file:line: "returns last month's balance to a logged-in user on first load (api/account.ts:42)." Claim only what the trigger and path reach; if the path ends at a failed request, the consequence ends there. Data loss needs a path to the write.
- **Fires when** — the concrete input or state that triggers it, and the real caller, route, input, or test it comes from. If you can't name where the value comes from, you're guessing it can happen — move it to a question or drop it.
- **Guard** — the check that should stop it and why it misses, quoted from the code, or "none — searched <where you looked>." Before writing this line, assume the code is right and you are wrong: hunt for the guard that makes your finding fake, then say why it still fails. Most fake findings die here.

Add one line of fix direction when it isn't plain. Don't restate the code back; they have the diff. Order findings by which bites hardest. No P1/P2 labels — a number is free to inflate and earns trust it hasn't proven; the consequence sentence is the severity, and it can't be pushed past the path you traced.

If you've written more than three findings, stop and re-run the bar on each. Past a handful, suspicions slipped through.

## What to catch

- Bugs: logic errors, null handling, race conditions, stale state, cleanup gaps, invalid assumptions, unreachable code, data loss.
- Regressions: a changed public contract, UI state, API shape, persistence, permissions, or workflow.
- Security: auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, data exposure.
- A swallowed or dropped error a caller needs to stay correct or recover.
- Missing coverage: new behavior or a regression path with no useful test, including a bug fix that ships without a regression test.
- A test asserting on internals that would break under a behavior-preserving refactor.
- A repo-rule break, only when local guidance or nearby code proves the rule.

## Don't flag

- Method length on its own. A long method with a simple signature doing one coherent job is fine; length is a finding only when it causes a named problem.
- An error the code deliberately makes impossible (validated upstream, unreachable by type) or correctly lets crash. Raise missing handling only when a real caller needs the signal.
- Code that's correct but over-built, awkwardly named, or non-idiomatic. That's behavior-preserving cleanup, out of scope here. When a reader would trip on it, drop one pointer at the end — "cleanup candidate: file:line" — no severity, no argument. At most two; more than that means you're reviewing for taste.
- Style nits a formatter or linter catches.

## Final shape

Match length to the change. A diff with nothing wrong gets one line: no findings, plus residual risk if any — named specifically, with why it stayed unverified. A trivial diff gets at most one finding. Then, in order, dropping any section that's empty:

1. Findings.
2. A question — something you'd ask the author, only when the answer needs information the code can't give (runtime config, an external service, product intent). Drop a hunch you couldn't prove; it doesn't belong here.
3. A one-line change note, only when the diff's intent isn't plain from the diff.
4. A named test or verification gap, only when a real one exists.
