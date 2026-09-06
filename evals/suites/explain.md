# Explain suite

The job is a clear answer, backed, and short. This suite measures whether the
skill delivers that or writes an essay.

Four questions in `fixtures/explain-questions.md`, each answered as one turn.
The length numbers below are measured, and everything else is read.

## What a passing answer does

- **Answers in the first sentence.** Not context, not a restatement of the
  question, not what it is about to explain.
- **Runs to two or three sentences** unless the question asks for depth. Q3 asks
  for brevity outright and a long answer there is a plain failure.
- **Backs every claim.** Code gets a path and a line. Behavior gets the output.
  Outside facts get a source. An unbacked claim is named as a guess, in that
  word. Q4 exists to test this: "safe to remove" is a claim about behavior and
  needs the callers checked or the check named as not run.
- **Asks nothing back.** No quiz, no withheld answer, no "what do you think?".
  That belongs to `toby-learning`, which fires only when invoked.

- **Uses ordinary English.** A word doing a job its normal meaning does not
  cover costs the reader a guess.

## What a failing answer looks like

- Opens with a paragraph before the answer.
- Runs past three sentences on Q1, Q3, or Q4 with no reason to.
- Says the retry logic is safe without saying how that was checked.
- Turns Q2 into a lesson with questions in it.
- Coins a metaphor: a first-read surface, a seam, a lens.

## Trigger note

Q3 asks for the answer in a clear and concise form. That phrasing used to pull in
`toby-swd-clarity`, whose job is naming and comments inside code. Both
descriptions now name the boundary, and the `triggering` suite carries the probe.
