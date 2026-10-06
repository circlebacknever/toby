# Toby SWD Experiment

An experiment answers one question, compares candidates, or finds a value that reading the code cannot settle.

## Loop

Change one thing per pass, because two changes in one pass hide which one caused the result.

1. Inspect the current behavior and the smallest safe edit point.
2. Write down one candidate, then make one reversible change to a behavior, parameter, path, or surface.
3. Report the changed value and what the user should observe.
4. Ask the user to test, or run the smallest check that answers the question.
5. Record the result in the chat, and wait for feedback before the next candidate.

## Surface

Default to a local script, or a labeled block in the nearest file, that prints the inputs, the candidate values, and the result. When the user tests in a running app, use a dev-only state panel or debug route.

Name throwaway work with `experiment`, `poc`, `spike`, `scratch`, `debug`, or `temp`, so the cleanup can search for those names. Keep experiment state out of durable project code. When discovery has to touch production behavior, keep the diff as small as the question allows, and report the exact path or value changed.

## Checks

During discovery, the user's feedback and manual observation can be the verification. Run automated tests, browser automation, screenshots, or broad checks only when the user asks or the experiment surface needs them. Leave settings where the user put them, because the user is part of the measurement.

When the experiment drives something physical, costly, or visible outside the machine, reverting the code does not undo the effect. Run the candidate first in the cheapest stand-in that behaves like the real system, and ask before acting on the real one.

## Finish

When the user chooses a behavior:

- Move the chosen behavior into the normal project path.
- Delete the throwaway surface, temp names, flags, debug routes, scratch files, and notes the final behavior does not need.
- State the inputs, seeds, and versions the experiment surface left implicit, so the result reproduces outside this session.
- Write durable tests for the chosen behavior when a reliable harness can protect it. When the user tested by hand, report the checks that did not run.
- Search the diff for the throwaway names before saying the experiment is finished.

## Red flags

Before handing back a result, check for each of these, and report each one that occurred:

- Scratch work is hidden in a production path.
- One pass changed more than one candidate.
- A test was written for behavior still being discovered.
- The user was asked for feedback without seeing the state.
- Experiment code is still in the diff after the user chose.
