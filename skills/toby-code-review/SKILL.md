---
name: toby-code-review
description: Use when the user asks for code review, PR review, diff review, commit review, working-tree review, or concise findings on changed code, especially bugs, regressions, missing tests, security issues, and repo-rule breaks.
---

# Toby Code Review

Use this skill for review work only. The output is a tight findings report, no essay stapled to it.

## Scope

- Default to the current diff when no scope is given.
- For PR review, inspect PR metadata and diff with available local tools.
- Read repo guidance files and scoped instructions that apply to changed files.
- Report issues introduced by the change. Existing problems belong in residual risk when they affect the review.

## Review Standard

Lead with findings, ordered by severity. Each finding needs:

- File and line reference.
- User-visible or maintainer-visible impact.
- Evidence from code, tests, config, docs, or reachable flow.
- Fix direction.

Before a finding goes in, open the code it touches and confirm the failure fires on a reachable path. If reading the code doesn't confirm it, it isn't a finding — drop it or move it to questions. Most plausible-looking issues die here; that is the job. A report with more than a handful of findings usually means suspicions slipped through unverified.

## What To Catch

- Bugs: logic errors, null handling, race conditions, stale state, cleanup gaps, invalid assumptions, unreachable code, data loss.
- Regressions: changed public contracts, UI state, API shape, persistence, permissions, or workflow.
- Missing tests: only when new behavior or a regression path has no useful coverage.
- Security issues: auth, authorization, injection, secrets, path traversal, unsafe parsing, CSRF, SSRF, XSS, data exposure.
- Repo-rule breaks: only when local guidance or nearby code proves the rule.
- Swallowed error a caller needs for reliability. (toby-swd-complexity)
- Test coupled to internals that breaks on a behavior-preserving refactor, or a bug fix with no regression test. (toby-swd-testing)

## Don't Flag

The swd skills sanction some choices on purpose. Leave these alone:

- Method length alone. A long method that's one coherent deep abstraction with a simple signature is fine. (toby-swd-modules)
- An error deliberately defined out of existence or left to crash per the error ladder. Raise a missing-handling bug only when a caller needs the signal. (toby-swd-complexity)
- Shallow-module or naming opinions with no broken caller or concrete cost. That belongs to the coding agent.

## Cut

- Style nits that tooling catches.
- Broad quality commentary with no concrete failure.
- Abstraction requests with no broken caller or change cost.
- Intro summaries before findings.
- Long confidence math.
- Tool-specific posting behavior unless the user asks for it.
- Findings padded past a line or two; the coding agent scans this report and skips essays.

## Final Shape

Use this order:

1. Findings.
2. Questions or assumptions.
3. Brief change note when it helps.
4. Test or verification gaps.

When there are no findings, say that directly and name any residual risk.
