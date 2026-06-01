---
name: toby-feature-dev
description: Use when the user asks to build a non-trivial feature, continue feature work, design a multi-file behavior change, or move from vague product request to code while preserving repo patterns, tests, and approval checkpoints.
---

# Toby Feature Dev

Use this skill to turn a feature request into a small, reviewable implementation. The job is to find the owner of the behavior, make one coherent change, and leave evidence that it works.

This skill owns the workflow and the approval checkpoints. The engineering method at each step lives in the named toby-swd-* skills; load and apply them as the steps call for.

## Workflow

1. Classify the work.
   - Tactical: local behavior change, low public-API risk, existing pattern is obvious.
   - Strategic: new boundary, public API, data model, architecture, persistence, auth, billing, privacy, migration, or broad UI workflow.
   - State the mode for non-trivial work.
   - This split and the standard behind it — leave the system's design at least as good as you found it — come from toby-swd-strategy.

2. Discover before designing.
   - Inspect repo guidance, tests, config, docs, call sites, and similar features.
   - Use `rg` or `rg --files` first.
   - Read the files that own the behavior. Summaries are cheap; unread files are where defects rent space.
   - If an independent explorer is available, ask for file paths and evidence, then read the files yourself.
   - When the behavior is still being discovered, drop into toby-swd-experiment for short reversible loops before committing to a design.

3. Resolve ambiguity.
   - Ask only questions that change behavior, public contracts, data, permissions, migrations, test expectations, or product vocabulary.
   - Use a concrete assumption when risk is low, then state it before coding.
   - Stop for confirmation when a wrong assumption would create bad behavior or lost data.
   - The resolved answers are the acceptance criteria. State what done looks like as an observable result before coding.

4. Design the change.
   - For tactical work, choose the smallest design that matches nearby code.
   - For strategic work, run the design pass from toby-swd-strategy: sketch two approaches that differ in where complexity lives, then pick the one with the simpler caller-side interface.
   - For any new or changed callable surface, write the interface comment first and run the comment test from toby-swd-interfaces. Decompose around the knowledge each module owns and check for deep modules per toby-swd-modules.
   - Recommend one route with the reason. Keep it short.

5. Implement vertically.
   - Protect one behavior at a time.
   - When the feature is too big for one diff, split it into chunks that each ship and demo on their own. Give each chunk its own check — automated tests and manual steps — so it's validated as you go.
   - Add or update a focused test first when the contract is settled; follow toby-swd-testing for what to assert and how to name it.
   - Make the smallest production change that satisfies it.
   - Handle errors by the ladder in toby-swd-complexity and hold performance work until a measured problem. Name and comment per toby-swd-clarity.
   - Keep refactors separate from behavior changes unless the refactor makes the behavior fit.
   - Update docs when public API, module usage, or a cross-module decision changed; toby-swd-docs covers AGENTS.md and README.

6. Review before final.
   - Inspect the diff for unrelated churn, weakened tests, broad formatting, generated files, hidden environment effects, and shallow wrappers.
   - Run the narrowest useful verification. Ask before broad validation, snapshots, migrations, installs, or runtime-affecting commands — toby-swd-environment owns command discipline and port handling.
   - Report changed files, verification, skipped checks, risk, and any process left running.
   - Hand off how to validate the change: the automated tests to run and the manual steps to check it by hand.

## Output Shape

- During work: short status updates that say what is being inspected or changed and why.
- Before edits: name touched files or systems.
- Final response: result, verification, and remaining risk.
- No marketing language, long recaps, or fake certainty.
