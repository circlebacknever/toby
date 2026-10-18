---
name: toby-explain
description: >-
  Answers a question in plain words, then stops, and doesn't edit files. Use it
  when the user asks why, how, what the difference is, which option fits, or
  where code should go, on any subject. Use it for "walk me through", "help me
  understand", and any request for a clear, short, or simple explanation. Skip
  it when the user asks for a diagram, a chart, or a deck, which
  toby-artifact-style covers. Skip it when the user wants a fix, which
  toby-bug-fix covers.
---

# Toby Explain

Answer the question in your first sentence, and give the reason in your second sentence. When the answer is a fix or workaround, list the steps to apply it and stop.

## Evidence

Back up every claim in chat:

- Cite `file:line` for a claim about this repo's code.
- Quote the output you saw for a claim about what code does when it runs.
- State the source for any other claim, or call an unverified claim a `guess`.
- Draw a diagram or chart only when the user asks for one.

## What to say

Include the one or two points below that the user needs:

- For a design or tradeoff question, state what was chosen, why it fits better than the alternative, and what the other option would have cost.
- State a common misreading and the right reading, or state what condition would change the answer.
- Run every read-only check (such as a version or config command) before stating what remains unknown.

For a design choice in code, open the matching skill by path (`../<skill>/SKILL.md`) and explain the choice with its rule:

- Where code goes: `toby-swd-modules` and `references/placement-note.md`
- Feature structure: `toby-swd-architecture`
- Design tradeoffs: `toby-swd-strategy/references/design-note.md`
- Error handling: `toby-swd-errors`
- New cases or subclasses: `toby-swd-extensibility`
- Feature flags: `toby-swd-flags`
- Logs and metrics: `toby-swd-observability`
- Timeouts, retries, and deploys: `toby-swd-hardening`
- Config, secrets, and process state: `toby-swd-twelve-factor`
- Caching or speed: `toby-optimize`

## Without code

When the user hasn't shown code or text, state the answer first, then give the smallest example where the common wrong assumption predicts a different result from the actual one.

## The reader

Match the explanation to what the user says about their background, because a beginner can ask a precise question. Compare a new concept to a familiar field only when the two mechanisms match closely.

## How to write it

- Put each explanation next to the line, equation, or passage it explains, and state what causes what (`"The test fails because CI runs in UTC."`).
- Use a short arrow chain (`request → cache → database`) when one sentence can't show how parts connect.
- Load `../toby-voice/references/plain-language.md` and follow it.
- Never quiz the user or hold back the answer, because only `/toby-learning` asks check questions.
- Leave out general tutorials, boxed "Insight" notes, and closing summaries.
- When explaining a step mid-task, state what must hold before the step, what the check showed after, and what remains unresolved.

Open `references/examples.md` when the question isn't about code, when no code is shown, or when explaining a decision mid-task.
