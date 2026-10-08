---
name: toby-swd-experiment
description: >-
  Runs a short, reversible discovery loop while the behavior is still undecided.
  Use it when the user says spike, prototype, proof of concept, throwaway, try a
  few values, compare options, tweak settings, or let me test. The word
  throwaway decides the route even when the request also names retries,
  timeouts, or tests. Skip it for work the user intends to keep, which
  toby-build covers. Skip it for starting or stopping a server alone, which
  toby-swd-environment covers.
---

# Toby SWD Experiment

An experiment answers one question, compares candidates, or finds a value that reading the code cannot settle.

## Loop

Change one thing per pass, because two changes in one pass hide which one caused the result.

1. Look at the current behavior, and find the smallest place in the code you can safely change.
2. Write down one candidate, then make one change you can undo, to a behavior, a parameter, a code path, or the experiment code.
3. Report the changed value and what the user should observe.
4. Ask the user to test, or run the smallest check that answers the question.
5. Record the result in the chat, and wait for feedback before the next candidate.

## Where experiment code goes

By default, put the experiment code in a local script or a labeled block in the nearest file. The code prints the inputs, the candidate values, and the result. When the user tests in a running app, use a dev-only state panel or debug route.

Name throwaway work with `experiment`, `poc`, `spike`, `scratch`, `debug`, or `temp`, so the cleanup can search for those names. Keep experiment state out of durable project code. When the experiment has to change production behavior, keep the diff as small as the question allows, and report the exact path or value changed.

## Checks

During discovery, the user's feedback and manual observation can be the verification. Run automated tests, browser automation, screenshots, or broad checks only when the user asks or the experiment code needs them. Do not change settings the user chose, because the user's observations depend on those settings.

When the experiment drives something physical, costly, or visible outside the machine, reverting the code does not undo the effect. Run the candidate first in the cheapest stand-in that behaves like the real system, and ask before acting on the real one.

## Finish

When the user chooses a behavior:

- Move the chosen behavior into the normal project path.
- Delete the experiment code, temp names, flags, debug routes, scratch files, and notes the final behavior does not need.
- Write down the inputs, random seeds, and versions the experiment code used without recording them, so someone can get the same result outside this session.
- Write durable tests for the chosen behavior when the project has a reliable test setup that can check that behavior. When the user tested by hand, report the checks that did not run.
- Search the diff for the throwaway names before saying the experiment is finished.

## Red flags

Before handing back a result, check for each of these, and report each one that occurred:

- Scratch work is hidden in a production path.
- One pass changed more than one candidate.
- A test was written for behavior still being discovered.
- The user was asked for feedback before being shown the changed value and what to look for.
- Experiment code is still in the diff after the user chose.
