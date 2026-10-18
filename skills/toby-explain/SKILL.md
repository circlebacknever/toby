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

Answer the question in your first sentence, and give the reason in your second sentence. Keep every sentence short and active so the user understands it on the first read. When the answer is a fix or workaround, list the numbered steps to apply it and stop.

## How to explain

Write the way a clear human engineer explains something to a teammate:

- **Name who does what.** Put the actor (`the browser`, `the handler`, `Postgres`, `you`) before an active verb (`sends`, `checks`, `locks`, `returns`). Never hide the actor in passive voice (`"is validated"`, `"is returned"`).
- **Walk one example through in time order.** When explaining how code or a system works, trace one concrete input from start to finish in the order the steps happen (`"When a user clicks Cancel, the browser sends POST /orders/42/cancel..."`).
- **Use everyday words first.** Explain what happens in plain words before naming internal abstractions. After you introduce a long identifier (`WorkspaceSeatRollupJob`), you can call it `that job` in the next sentence so the prose reads naturally.
- **Put `file:line` at the end of the sentence or bullet.** Don't interrupt the middle of a clause with file paths.
- **Break multi-point paragraphs into bullets.** Keep paragraphs to at most three short sentences. When listing reasons, steps, or differences, give each one its own bullet or number.

## Evidence

Back up every claim in chat:

- Cite `file:line` for a claim about this repo's code.
- Quote the output you saw for a claim about what code does when it runs.
- State the source for any other claim, or call an unverified claim a `guess`.
- Draw a diagram or chart only when the user asks for one.

## What to include

Include only the one or two points below that answer the user's question:

- For a design or tradeoff question, state what the code chose, the concrete bug or maintenance cost it avoids in this codebase, and what the other option would have cost.
- State a common misreading and the right reading, or state what condition would change the answer.
- Run every read-only check (such as a version or config command) before stating what remains unknown.

When the user asks where code should go or why a design rule applies, open the matching skill by path (`../<skill>/SKILL.md`) and explain the choice in plain words using the concrete code in front of you:

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

When the user hasn't shown code or text, state the answer first, then give a short concrete example where the common assumption fails.

## The reader

Match the explanation to what the user says about their background, because a beginner can ask a precise question. Compare a new concept to a familiar field only when both work the same way.

## Finishing checks

- Put each explanation next to the line, equation, or passage it explains, and state what causes what (`"The test fails because CI runs in UTC."`).
- Load `../toby-voice/references/plain-language.md` and follow it.
- Never quiz the user or hold back the answer, because only `/toby-learning` asks check questions.
- Leave out general tutorials, boxed "Insight" notes, and closing summaries.
- When explaining a step mid-task, state what must hold before the step, what the check showed after, and what remains unresolved.

Open `references/examples.md` when the question isn't about code, when no code is shown, or when explaining a decision mid-task.
