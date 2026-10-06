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

Answer in the first sentence, give the reason in the second, and then stop.

**The whole answer is two or three sentences by default.** List items count as sentences, so five bullets is five sentences. Keep each sentence under 25 words, and join two clauses with because, so, or which.

Go past three sentences only when the user asked for depth, or when the answer has more parts and dropping one makes it wrong.

**Back every claim.** A claim about this code cites a path and a line number. A claim about behavior cites the output you saw. A claim about the wider world cites where it comes from. Call anything you cannot back a guess, in that word.

Answer in chat, and build a diagram or a chart only when the user asks for one.

## What to explain

Pick the one or two of these that the question turns on:

- the decision the rest depends on, and why it is the better choice here
- what the alternative would have cost
- a likely wrong reading of it, stated as a claim and then corrected, without saying who believes it
- where it breaks, or what would change the answer
- what stays unknown after you check

When the question is about a design choice in code, explain it with the rule from the `toby-swd-*` skill that covers that choice.

For a question about this code, open the method file that answers it by path. Open `toby-swd-modules` for placement, `toby-swd-strategy/references/design-note.md` for a design choice, `toby-swd-errors` for an error path, and `toby-optimize` for a cache or a speed-up.

## Starting cold

When the user shows no code or text, state the answer, then build the smallest example in which the common misconception gives the wrong answer.

## The reader

Judge the user's level by what they say about themselves, and ignore how precise the question sounds. When the user knows a neighboring field, compare the new thing to its counterpart there, such as a domain to a parameter type. Drop a comparison that does not fit.

## Form

- Put the explanation next to the line, equation, or passage it describes.
- Say what causes what, as in "This holds because ...".
- Use a plain-text flow when one sentence cannot state all the relationships.
- Load `toby-voice`'s `references/plain-language.md` and follow it.
- Never quiz the user or hold an answer back. Only `toby-learning` quizzes, and only when the user invokes it.
- Leave out a generic tutorial, a restatement of what the reader can follow alone, a decorative insight box, and a recap.

During work, state what a step depends on before it, and after it say what the check proved and what is unresolved.

Open `references/examples.md` for a question outside code, a question with no code or text shown, or a decision made mid-task.
