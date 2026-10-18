# Explain suite

A passing explanation is clear, backed by evidence, and concise. This suite tests `toby-explain` across the four questions in `fixtures/explain-questions.md`, with each question answered in a single turn.

## What a passing answer does

- **Answers in the first sentence.** It starts with the answer and doesn't open with background context, a restatement of the question, or a preview.
- **Walks through concrete steps in time order.** On mechanism questions (such as Q2), it traces what happens step by step using active verbs (`hands control`, `runs`, `resumes`) and keeps sentences under 25 words.
- **Backs every claim.** It cites `path:line` for code claims, quotes output for runtime claims, and marks any unverified claim as a `guess`. Q4 tests whether the agent checks callers and states that the test suite hasn't run before calling a deletion safe.
- **Never quizzes the user.** It gives the full answer directly without asking check questions, because only `/toby-learning` asks check questions.
- **Uses everyday English.** It avoids unexplained jargon, four-noun stacks, and invented metaphors (`first-read surface`, `seam`, `lens`).

## What a failing answer looks like

- Opens with a setup paragraph or restates the question before answering.
- Writes a giant multi-clause paragraph for a one-sentence point, or uses passive voice that hides who acts.
- Claims the retry wrapper is safe to delete without stating that the tests haven't run.
- Turns Q2 into a Socratic quiz.
- Uses a metaphor or coined term.

## Trigger note

Q3 asks for a "clear and concise" explanation. That phrasing routes to `toby-explain` and must not load `toby-swd-clarity`, which covers identifier names and comments inside code.
