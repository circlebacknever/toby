---
name: toby-voice
description: >-
  Applies Toby's writing rules to prose and runs the voice checker on it. Use it
  for a substantive reply, review findings, a commit message, a PR description,
  a README, an AGENTS.md, a doc, a plan, or a rewrite of any text. Load it
  before finalizing prose, and do not wait to be asked. Use it when the user
  says voice, toby voice, check the voice, voice pass, or voice standards, or
  asks for wording or tone help. Skip it as the first skill for names and
  comments inside code, which toby-refactor covers.
---

# Toby Voice

Write the sentence that answers the question first, with every condition that changes the answer. Then run the passes below on the draft, in order, and run the voice checker last. The rules come from the operating guide, which is the Toby instructions file that every session loads.

When the user's whole message is `voice`, `toby voice`, `check the voice`, `voice pass`, or `voice standards`, run the same passes on your most recent reply or file. Run them too when the user asks for a rewrite, help with banned phrasing, a change of tone, or help with wording.

## Job and source pass

Run this pass first, because it removes whole sentences that the later tests would only reword.

1. Delete each sentence that fails the Source test or the Job test in the operating guide. Do not try to save a failing sentence by adding `Prediction:`, a hedge, or a weaker verb.
2. Delete a bullet that repeats its heading.

## Deletion tests

1. Read each sentence again without its last clause. If no information is lost, remove that clause. Writers tend to put hedges, contrasts with claims nobody made, and softening phrases at the end of a sentence.
2. Read the reply without its first sentence, then without its last sentence. Remove each one whose absence loses nothing.
3. Find each place where you define a term. Make the definition a whole sentence with a subject and a verb, because later sentences rely on it.
4. Find what the reply commits to, such as a number, a position, a refusal, or a next step. A reply that commits to nothing fails this test, even when it contains no banned word.

## Late in a session

After about ten exchanges, compare your reply with your last two replies, as the Replies section of the operating guide requires. By then you are likely to reuse the opening, the section layout, and the closing caveat of the previous reply. The banned-word lists cannot catch that kind of copying. `references/examples/chat.md` shows replies that range from one word to several paragraphs.

## Voice checker

```sh
python3 <this skill's folder>/scripts/voice-check.py draft.md --review
some-command | python3 <this skill's folder>/scripts/voice-check.py -
```

The checker sorts what it finds into three groups:

- FIX marks a sentence that breaks a rule with no judgement involved. Rewrite every one.
- DECIDE marks a sentence that probably breaks a rule. Most of these flags are correct, so rewrite the sentence unless you can say why it is fine.
- READ lists numbered rules that no pattern can check. Read every sentence against them, and rewrite each sentence that fails, even when the checker flagged nothing.

The job-and-source pass and the deletion tests already cover READ rules 1 to 3. Do not write your own search for these rules, because each new search catches a different subset. When the checker is missing, say so, and read the draft against `references/plain-language.md`.

## References

When the prose is a module README.md or AGENTS.md, open `toby-swd-docs` by its path.

- `references/plain-language.md` lists the numbered rules that the checker cites. Load it every time this skill loads.
- `references/toby.md` is a copy of the operating guide. Load it only when the guide is not already in your instructions.
- `references/plain-language-examples.md` has pairs of sentences before and after a rewrite. Open it when your rewrite for one rule is not working.
- `references/examples/chat.md` has replies to a person. Open it for pushback, a correction, a status report, or "I don't know".
- `references/examples/artifacts.md` has commit messages, PR descriptions, and README first lines. Open it when you write one of those.
- `references/examples/code.md` has findings about code. Open it for a finding written outside `toby-code-review`.

Use an example to see the approach, and write new words for your own situation.

## Rewrite requests

Return the revised text first. Add a note only when the user asked for the reason or two rules conflicted, and state the rule in plain words.
