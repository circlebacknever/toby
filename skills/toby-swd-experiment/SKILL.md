---
name: toby-swd-experiment
description: >-
  Run a discovery loop when the behavior is not decided yet. Use it for a
  spike, a proof of concept, a parameter sweep, a throwaway debug surface, a
  manual test, or an iteration driven by user feedback. It covers small
  reversible changes, exposing state for inspection, deferring durable tests
  during discovery, and deleting or merging the experiment into the project once the user
  chooses. The word throwaway takes priority over every noun after it, so this skill covers the
  retry, timeout, and test questions raised inside a spike. Skip it for work
  the user intends to keep.
---

# Toby SWD Experiment

Use this skill when the work is exploratory and the user expects fast learning before durable implementation.

An experiment exists to answer a question, compare candidates, or find a value that cannot be known from static analysis alone.

## Mode Contract

Keep the loop short:

1. Inspect the current behavior and the smallest safe edit point.
2. Pick one candidate change.
3. Make the change reversible.
4. Expose enough state for the user or agent to inspect the result.
5. State what changed and what should be observable.
6. Wait for feedback before changing the next candidate.

Use experiment mode for prompts like:

- "Let's run experiments."
- "Keep tweaking this while I test."
- "Build a proof of concept."
- "Make a throwaway version."
- "Compare a few approaches."
- "Add a debug panel so I can see state."

## Experiment Surface

Make the experiment easy to run and read. Prefer a small surface that shows the values under test and the result they produce.

These surfaces are useful:

- A visible state panel.
- A debug route.
- A fixture or seeded sample.
- A local script or temp command.
- A local flag or toggle.
- A labeled block in the nearest file when a separate surface would add churn.

Expose the current inputs, outputs, candidate values, and selected state. If the user will test manually, show the exact thing they need to observe.

## Disposable Markings

Mark throwaway work so reversing it is easy.

Use names such as `experiment`, `poc`, `spike`, `scratch`, `debug`, or `temp`. Keep the work behind a dev-only route, local flag, isolated file, fixture, script, or labeled block. Avoid passing experiment state through durable project code.

If a change touches production behavior during discovery, keep the diff as small as the question allows and report the exact path or value changed.

## Iteration Loop

Follow these steps for each pass:

1. Write down the candidate.
2. Change one behavior, parameter, path, or surface.
3. Report the changed value and expected observation.
4. Ask the user to test or run the smallest useful check.
5. Record the result in the chat.
6. Repeat only after feedback.

Batching candidates hides which change caused which result, so run the loop with one change per result.

## Finish Phase

When the user chooses a behavior, end the experiment with these steps:

- Delete the throwaway surface.
- Move the chosen behavior into the normal project path.
- Remove temp names, flags, debug routes, scratch files, and notes that are no longer needed for the final behavior.
- Keep only artifacts that now belong to the product, module, docs, or tests.
- When exploratory work becomes durable code, state the inputs, seeds, and versions that the exploratory surface did not state. Then the result can be reproduced outside the original session.

If the experiment changed production code, review the diff before the finish phase ends.

If the selected behavior becomes durable inside a meaningful module, check whether the nearest module root has an AGENTS.md. Offer to create or update it with the module facts learned during the experiment. Keep the docs offer separate from the tuning loop so the loop stays fast.

## Testing Boundary

During discovery, user feedback and manual observation may be the validation source. Run automated tests, browser automation, screenshots, or broad checks only when the user asks or the experiment surface needs them.

After the behavior settles, decide which durable tests should cover the contract, then write them for the selected behavior. Discarded candidates can stay in the experiment notes.

## Environment Boundary

Use toby-swd-environment before commands, ports, processes, browsers, broad checks, dependency installs, migrations, generated files, cache clearing, or destructive work.

During a user-led loop, automated checks that add latency need approval. The user is part of the measurement in this loop, so leave the settings where the user put them.

Reversibility here means software reversibility. When the experiment drives something physical, costly, or externally observable, a reverted change does not undo what already happened. Run the candidate first in the cheapest proxy that behaves like the real system. Treat acting on the real system as a state change that needs approval.

## Failure Modes

- Hidden scratch work in a production path.
- Several candidate changes in one turn.
- Tests written for behavior still being discovered.
- State hidden from the user while asking for feedback.
- Experiment code left behind after selection.

Check the loop against this list before handing the result back, and list any entry that occurred. The last entry costs the most, so search the diff for the
markings before saying the experiment is finished.
