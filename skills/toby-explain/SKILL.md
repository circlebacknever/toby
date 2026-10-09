---
name: toby-explain
description: >-
  Answers a question in plain words, then stops, and edits no files. Use it when
  the user asks why, how, what the difference is, which option fits, or where
  code should go, on any subject. Use it for "walk me through", "help me
  understand", and any request for a clear, short, or simple explanation. Skip
  it when the user asks for a diagram, a chart, or a deck, which
  toby-artifact-style covers. Skip it when the user wants a fix, which
  toby-bug-fix covers.
---

# Toby Explain

Answer the question in your first sentence. Give the reason in your second sentence, and then stop.

## Length

Use two or three sentences. A list item counts as a sentence, so five bullets are five sentences. Write more only when the user asked for depth, or when leaving a part out would make the answer wrong.

Keep each sentence to 25 words or fewer. Use "because" only for a real cause, and "so" only for a result.

## Evidence

Back up every claim.

- For a claim about this code, give the file path and the line number.
- For a claim about what code does when it runs, quote the output you saw.
- For any other claim, say where it comes from.

When you cannot back up a claim, call it a guess, and use the word "guess".

Answer in the chat. Draw a diagram or a chart only when the user asks for one.

## What to say

Include the one or two points below that the user needs to understand the answer.

- when the question is about a choice, what was chosen and why it fit this case better than the other options
- what the other option would have cost
- a way the user could easily misread the answer, followed by the correct reading
- when the answer stops being true, or what would change it
- what you still don't know after checking

For a design choice in code, open the file below by its path, and explain the choice with its rule:

- for where code goes, `toby-swd-modules` and its `references/placement-note.md`
- for a feature's structure, `toby-swd-architecture`
- for another design choice, `toby-swd-strategy/references/design-note.md`
- for error handling, `toby-swd-errors`
- for a new case or subclass, `toby-swd-extensibility`
- for a feature flag, `toby-swd-flags`
- for logs and metrics, `toby-swd-observability`
- for timeouts, retries, and deploys, `toby-swd-hardening`
- for config, secrets, and process state, `toby-swd-twelve-factor`
- for a cache or a speed-up, `toby-optimize`

## No code shown

When the user has shown no code or text, give the answer first. Then give the smallest example that shows the answer. Pick an example where the most common wrong assumption predicts a different result from the real one.

## The reader

Judge what the user knows from what they say about themselves, since a beginner can ask a precise question. When the user knows a related field, compare the new idea to the closest idea in that field. Leave the comparison out when the two ideas do not match well.

## How to write it

- Put each explanation next to the line, equation, or passage it explains.
- Say what causes what, as in "The test fails because CI runs in UTC."
- When one sentence cannot show how several things connect, draw a short text diagram, such as `request → cache → database`.
- Load `toby-voice/references/plain-language.md`, and follow it.
- Never quiz the user, and never hold back the answer. Only `toby-learning` asks the user questions, and only when the user starts it.
- Leave out a general tutorial, anything the reader can work out alone, a boxed "Insight" note, and a summary at the end.

When you explain a step during other work, say what has to be true before the step runs. After the step, say what your check showed and what is still unresolved.

Open `references/examples.md` for a worked example when the question is not about code, or when the user shows no code or text. Also open that file when you explain a decision you made partway through a task.
