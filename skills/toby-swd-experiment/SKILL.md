---
name: toby-swd-experiment
description: >-
  Run exploratory engineering loops when behavior is being discovered through
  rapid experiments, proof-of-concept work, spikes, throwaway debug surfaces,
  parameter tweaks, manual tests, or user feedback. Use when an agent needs to
  make small reversible changes, expose state for inspection, defer durable
  tests during discovery, and delete or fold in the experiment after the user
  chooses the behavior.
---

# Toby SWD Experiment

Use this skill when the work is exploratory and the user expects fast learning before durable implementation.

An experiment is a probe. It exists to answer a question, compare candidates, or find a value that cannot be known from static analysis alone.

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

Useful surfaces:

- A visible state panel.
- A debug route.
- A fixture or seeded sample.
- A local script or temp command.
- A local flag or toggle.
- A labeled block in the nearest file when a separate surface would add churn.

Expose the current inputs, outputs, candidate values, and selected state. If the user will test manually, show the exact thing they need to observe.

## Disposable Markings

Mark throwaway work so reversal is boring.

Use names such as `experiment`, `poc`, `spike`, `scratch`, `debug`, or `temp`. Keep the work behind a dev-only route, local flag, isolated file, fixture, script, or labeled block. Avoid threading experiment state into durable project flow.

If a change touches production behavior during discovery, keep the diff as small as the question allows and report the exact path or value changed.

## Iteration Loop

For each pass:

1. Name the candidate.
2. Change one behavior, parameter, path, or surface.
3. Report the changed value and expected observation.
4. Ask the user to test or run the smallest useful check.
5. Record the result in the chat.
6. Repeat only after feedback.

Batching candidates hides cause and effect. The loop should make each result attributable to one change.

## Finish Phase

When the user chooses a behavior, retire the experiment:

- Delete the throwaway surface.
- Fold the chosen behavior into the normal project path.
- Remove temp names, flags, debug routes, scratch files, and notes that no longer serve the final behavior.
- Keep only artifacts that now belong to the product, module, docs, or tests.

If the experiment changed production code, review the diff before the finish phase ends.

If the selected behavior becomes durable inside a meaningful module, check whether the nearest module root has an AGENTS.md. Offer to create or update it with the module facts learned during the experiment. Keep the docs offer separate from the tuning loop so the loop stays fast.

## Testing Boundary

During discovery, user feedback and manual observation may be the validation source. Automated tests, browser automation, screenshots, and broad checks wait unless the user asks for them or they are required to run the experiment surface.

After the behavior settles, use toby-swd-testing to decide what durable tests should protect the contract. Write tests for the selected behavior. Discarded candidates can stay in the experiment notes.

## Environment Boundary

Use toby-swd-environment before commands, ports, processes, browsers, broad checks, dependency installs, migrations, generated files, cache clearing, or destructive work.

During a user-led loop, automated checks that add latency need approval. The user is part of the instrument panel; leave the controls where the user put them.

## Failure Modes

- Hidden scratch work in a production path.
- Several candidate changes in one turn.
- Tests written for behavior still being discovered.
- State hidden from the user while asking for feedback.
- Experiment code left behind after selection.
