# Checks

Read "Don't build" before writing the plan or the first edit. Read "Red flags" and "Final response" before the handoff.

## Don't build

Build none of these unless a criterion requires it and that criterion's Source quotes the user or the ticket. Never write a criterion yourself to allow one. When one ships anyway, state the entry and the criterion that allowed it.

- A setting, hook, or extension point that one call site reads and nobody changes from its default. A release flag that a later slice removes does not count.
- An interface or adapter with one implementation whose methods only forward calls. Extend the interface you already have, as `toby-swd-interfaces` describes, and wait for a second implementation, which shows what the two have in common. Moving a rule into the module that reads and writes its data is allowed, such as a discount rule moved out of a view into the pricing module.
- Error handling for a state that the types or an earlier check already rule out.
- A feature the request implies but does not ask for, or a defect you found while building. List each as a follow-up, and leave it out of the change.
- A migration, rename, or reorganization that no criterion asks for.
- A metric, alert, or shutdown hook that no similar entry point in the repo has. List it as a follow-up.
- Performance work with no baseline. A claim such as 40% faster needs a number from before the change.
- A package the user has not approved.

These items are part of the change:

- the checks that the `toby-swd-hardening` table lists for code this change adds
- the outcome log that `toby-swd-observability` requires for a new entry point
- a refactor that `toby-swd-campfire` allows and that you stated before the first edit
- a fix for what the design check in `toby-swd-architecture` finds, reported on its own line

## Red flags

Check the finished work against each problem below. Fix what you can before the handoff. Report each problem still in the work at file:line, in plain words.

- The handoff reports a criterion met, but its check never reached the changed lines, or nobody saw its test fail. A green type-check, a lint pass, or a suite that skips the changed lines proves only that the repo still builds.
- The unit tests pass, but nothing registers the route.
- A signature changed, and nobody listed its callers, as "Brownfield Work" in `toby-swd-interfaces` describes.
- The change uses a symbol that nobody read in the installed source, as step 7 of `toby-build` requires. Docs for a later version than the lockfile pins do not count.
- A criterion covers less than its approved wording, or a design decision went ahead without the user's yes.
- An edit came before the user approved its step, or a step ran differently from its approved wording and nobody edited the plan. A design-check fix that you add to the plan before you make it is allowed. Report that fix at the next stop.
- Production code contains a placeholder, such as a TODO, a hardcoded return in place of real work, an unimplemented branch, a swallowed error, or a fixture the runtime reads.
- The handoff calls a feature done and moves its unbuilt slices to a closing note, such as "the rest is just wiring".
- A file changed, and neither a criterion nor a reported cleanup explains it.
- The handoff leaves out an assumption stated mid-run.

## Final response

After the lead line, write only what the user needs to act on:

1. Each criterion in its pre-code wording, marked met or unmet, with the check that proved it or what is missing. When nothing could run, say so once and give each criterion's check. For multi-slice work, mark each slice done or not done.
2. The structure chosen and the main alternative rejected, one line each, or the `Structure: follows <path:line>` line. Say where the plan is.
3. For work with more than one slice, the whole-feature test, with its run before the last slice and its run after it.

Then add these, leaving out each one that has nothing in it:

- Each step you could not run, with what blocked it.
- Each question whose answer changes what gets built, on its own line, with the answer you will use if the user says nothing. Ask it before the work it affects whenever you can.
- Each problem you saw and left alone, one line each at file:line. Leave out a follow-up for a problem you did not see in the code.
