# Checks

Read "Don't build" before writing the plan or the first edit. Read "Red flags" and "Final response" before the handoff.

## Don't build

Build none of these unless a criterion requires it and that criterion's Source quotes the user or the ticket. Never write a criterion yourself to allow one. When one ships anyway, state the entry and the criterion that allowed it.

- A setting, hook, or extension point that one call site reads and that stays at its default. A release flag that a later slice removes doesn't count.
- An interface or adapter with one implementation whose methods only forward calls. Extend the interface you already have, as `toby-swd-interfaces` describes, and wait for a second implementation, which shows what the two have in common. Moving a rule into the module that reads and writes its data is allowed, such as a discount rule moved out of a view into the pricing module.
- Error handling for a state that the types or an earlier check already rule out.
- A migration, rename, or reorganization that the criteria don't ask for.
- Performance work with no baseline. A claim such as 40% faster needs a number from before the change.
- A package that the user hasn't approved and the request doesn't name.

These items are part of the change:

- the work the request implies, such as the docs, config, and old code that a migration replaces. Put each item in the plan, so the user can reject it before the build.
- a metric, alert, or shutdown hook that the new entry point needs, marked optional in the plan
- a defect you found while building, with its file:line in the plan, so the user sees it before the work ends
- the checks that the `toby-swd-hardening` table lists for code this change adds
- the outcome log that `toby-swd-observability` requires for a new entry point
- a refactor that `toby-swd-campfire` allows and that you stated before the first edit
- a fix for what the design check in `toby-swd-architecture` finds, reported on its own line

## Red flags

Check the finished work against each problem below. Fix what you can before the handoff. Report each problem still in the work at file:line, in plain words.

- The handoff reports a criterion met, but its check never reached the changed lines, or nobody saw its test fail. A green type-check, a lint pass, or a suite that skips the changed lines proves only that the repo still builds.
- The unit tests pass, but the code doesn't register the route.
- A signature changed, and you didn't list its callers, as "Brownfield Work" in `toby-swd-interfaces` describes.
- The change uses a symbol that nobody read in the installed source, as step 7 of `toby-build` requires. Docs for a later version than the lockfile pins don't count.
- A criterion covers less than its approved wording or than the request's words, or you made a choice without asking that the Decisions section of the operating guide says to ask about.
- An edit came before the user approved its step, or a step ran differently from its approved wording and you didn't edit the plan. A design-check fix that you add to the plan before you make it is allowed. Report that fix at the next stop.
- Production code contains a placeholder, such as a TODO, a hardcoded return in place of real work, an unimplemented branch, a swallowed error, or a fixture the runtime reads.
- The handoff moves part of the requested result to a closing note or a next step for the user, such as unbuilt slices or "the rest is just wiring".
- A file changed, and neither a criterion nor a reported cleanup explains it.
- The handoff leaves out an assumption stated mid-run.

## Final response

After the lead line, list each choice you made as an assumption. Ask only a question that the Decisions section of the operating guide allows, with the answer you recommend. Then write only what the user needs to act on:

1. Each criterion in its pre-code wording, marked met or unmet, with the check that proved it or what is missing. When you couldn't run anything, say so once and give each criterion's check. For multi-slice work, mark each slice done or not done.
2. The structure chosen and the main alternative rejected, one line each, or the `Structure: follows <path:line>` line. Say where the plan is.
3. For work with more than one slice, the whole-feature test, with its run before the last slice and its run after it.

Then add these, leaving out each one that has nothing in it:

- Each step you couldn't run, with what blocked it.
- Each problem outside the request that you saw and left alone, one line each at file:line. Leave out a follow-up for a problem you didn't see in the code.
