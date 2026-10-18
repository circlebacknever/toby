---
name: toby-swd-experiment
description: >-
  Runs a short, reversible discovery loop while the behavior is still undecided.
  Use it when the user says spike, prototype, proof of concept, throwaway, try a
  few values, compare options, tweak settings, or let me test. Use it whenever
  the request says throwaway, even when it also names retries, timeouts, or
  tests. Skip it for work the user intends to keep, which toby-build covers.
  Skip it for starting or stopping a server alone, which toby-swd-environment
  covers.
---

# Toby SWD Experiment

An experiment answers one question, compares candidates, or finds a value that reading the code can't settle.

## Loop

Change one thing per pass so you can tell which change caused the result:

1. Inspect the current behavior and find the smallest place you can safely change.
2. State one candidate and make one reversible edit to a parameter, branch, or scratch script.
3. Report the changed value and what the user should observe.
4. Ask the user to test, or run the smallest check that answers the question.
5. Record the result in chat and wait for feedback before trying the next candidate.

## Where experiment code goes

Put experiment code in a local script, a dev-only debug panel, or a labeled block in the nearest file that prints the inputs, candidate values, and result. Prefix throwaway identifiers and files with `experiment`, `poc`, `spike`, `scratch`, `debug`, or `temp` so cleanup can search for them, and keep experiment state out of durable code.

## Checks

During discovery, use the user's manual observation or the smallest direct check, and don't overwrite settings the user chose. When an experiment affects anything physical, paid, or external to the machine, run it in a local stand-in first and ask before touching the real system.

## Finish

When the user picks a behavior:

- Move the chosen behavior into the normal project structure.
- Delete all experiment code, temp identifiers, debug routes, scratch files, and notes, and search the diff for the throwaway prefixes above.
- Record the inputs, random seeds, and library versions used so the result is reproducible.
- Write durable tests for the kept behavior when the repo has a test harness, and report any check that didn't run.

## Red flags

Check for and report any of these before finishing:

- Scratch code left in a production path after the user chose.
- Multiple candidates changed in a single pass.
- Durable tests written for behavior that is still undecided.
- Asking the user for feedback before stating what value changed and what to look for.
