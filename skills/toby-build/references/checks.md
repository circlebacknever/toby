# Checks

Read "Don't build" before writing the plan or the first edit, and read "Red flags" and "Final response" before the handoff.

## Don't build

Build none of these unless a criterion requires it and quotes the user or the ticket as its Source. Never write a criterion yourself to allow one. When one ships anyway, state the entry and the criterion that allowed it.

- A setting, hook, or extension point that one call site reads and that stays at its default. A release flag that a later slice removes doesn't count.
- An interface or adapter with one implementation whose methods only forward calls. Extend the existing interface, as `toby-swd-interfaces` describes, and wait for a second implementation. Moving a rule into the module that reads and writes its data is allowed.
- Error handling for a state that the types or an earlier check already rule out.
- A migration, rename, or reorganization that the criteria don't ask for.
- Performance work without a measured baseline.
- A package that the user hasn't approved and the request doesn't name.

Include these items in the change:

- Work the request implies, such as the docs, config, and old code that a migration replaces. Put each item in the plan so the user can reject it before the build.
- A metric, alert, or shutdown hook that a new entry point needs, marked optional in the plan.
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
- You changed a file without a criterion or a reported cleanup explaining it, or the handoff omits an assumption you stated mid-run.

## Final response

After the lead line, list each choice you made as an assumption, and state any decision the next slice needs before it starts. Then write only the items that apply:

1. Each criterion in its pre-code wording, marked met or unmet, with the check that proved it or what blocked it. For multi-slice work, mark each slice done or not done.
2. The structure you chose and the main alternative you rejected, one line each, or `Structure: follows <path:line>`, plus the plan path when a plan exists.
3. For work with two or more slices, the whole-feature test with its run before and after the last slice.
4. Each step you couldn't run, with what blocked it.
5. Each problem outside the request that you saw in the code and left alone, one line each at `file:line`.
