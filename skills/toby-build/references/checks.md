# Checks

Read "Don't build" before writing the plan or the first edit, and read "Red flags" and "Final response" before the handoff.

## Don't build

Build none of these unless a criterion requires it and quotes the user or the ticket as its Source. Never write a criterion yourself to allow one. When one ships anyway, state the entry and the criterion that allowed it.

- A setting, hook, or extension point that one call site reads and that stays at its default. A release flag that a later slice removes doesn't count.
- An interface or adapter whose methods only forward calls while hiding no provider contract, invariant, or caller obligation. A boundary that hides a current dependency can justify one implementation.
- Error handling for a state that the types or an earlier check already rule out.
- A migration, rename, or reorganization that the criteria don't ask for.
- Performance work without a measured baseline.
- A package that the user hasn't approved and the request doesn't name.

Include these items in the change:

- Work the request implies, such as the docs, config, and old code that a migration replaces. Put each item in the plan so the user can reject it before the build.
- Diagnostics and operational safeguards that changed behavior needs. State why a metric, alert, or shutdown hook applies, and record any actual blocker.
- A defect you found in the touched path while building, with its `file:line` in the plan.
- The checks that `toby-swd-hardening` and `toby-swd-observability` require for code this change adds.
- A refactor before the feature edit that `toby-swd-campfire` allows and that you stated before the first edit, plus any fix from the `toby-swd-architecture` design check.

## Red flags

Check the finished work against each problem below, fix what you can before the handoff, and report any remaining problem at `file:line`.

- The handoff reports a criterion met, but its check never reached the changed lines, or nobody watched its test fail before the change.
- The unit tests pass, but the code doesn't register the route, job, or UI entry point.
- A signature changed without listing its callers, as "Brownfield Work" in `toby-swd-interfaces` requires.
- The change calls an external symbol whose installed source nobody read or cited in the repo.
- A criterion covers less than its approved wording, or you made an irreversible choice without asking.
- An edit came before the user approved its step, or a step ran differently from its approved wording without updating the plan.
- Production code contains a `TODO`, a hardcoded return, an unimplemented branch, a swallowed error, or a test fixture that production code reads at runtime.
- The handoff moves part of the requested result to a closing note, such as unbuilt slices or "the rest is wiring".
- You changed a file without a criterion or a reported cleanup explaining it.

## Final response

After the result, state the material design reason and the checks that ran, including diagnostic output you inspected. Add these items when they apply:

1. Each criterion that's unmet, or each slice that's not done, with what blocked it.
2. Each assumption the user might want changed, and any decision the next slice needs.
3. Each step you couldn't run, with what blocked it.
4. Each problem you noticed outside the request and didn't fix, at `file:line`.

Leave out repeated progress history. Keep the evidence and reason short enough for the user to assess the change.
