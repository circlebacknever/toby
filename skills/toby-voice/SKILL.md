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

Write the answer sentence first, with every condition that changes it. Then run these passes on the draft in this order, and run the voice checker last.

Run the same passes on the recent output when the user says only `voice`, `toby voice`, `check the voice`, `voice pass`, or `voice standards`. Run them too for a request for a rewrite, banned-phrasing help, tone repair, or wording help.

## Job and source pass

Run this pass before the deletion tests, because it removes whole sentences that the tests would only reword.

1. Delete each sentence that fails the guide's Source or Job test. Do not keep one by adding `Prediction:`, a hedge, or a softer verb.
2. Delete a bullet that repeats its heading.

## Deletion tests

1. Delete the final clause of each sentence. When the sentence lost no information, leave the clause out, because hedges, foils, and softeners appear there.
2. Delete the first sentence of the reply and check what was lost. Then do the same with the last sentence. Leave out each one whose removal lost nothing.
3. Read each sentence that defines a term on its own, and make it a whole sentence, because every later sentence depends on it.
4. Find what the reply commits to, such as a number, a position, a refusal, or a next step. A reply that commits to nothing fails, even with no banned word in it.

## Late in a session

Run the guide's check against the last two replies after about ten turns. By then the risk is a copy of the previous reply's opener, sections, and closing caveat. The banned lists cannot catch that copy. `references/examples/chat.md` shows replies from one word to several paragraphs long.

## Voice checker

```sh
python3 <this skill's folder>/scripts/voice-check.py draft.md --review
some-command | python3 <this skill's folder>/scripts/voice-check.py -
```

Rewrite every sentence the checker marks FIX. Decide each sentence it marks DECIDE, because most of those flags are correct. Then read each numbered sentence against the READ rules it prints, and rewrite each one that fails, even when the patterns matched nothing. The two passes above cover READ rules 1 to 3. Do not write your own grep for these rules, because each new grep matches a different subset. When the checker is missing, say so, and read the draft against `references/plain-language.md`.

## References

When the prose is a module README.md or AGENTS.md, open `toby-swd-docs` by path.

- `references/plain-language.md` numbers the rules that the checker cites. Load it every time this skill loads.
- `references/toby.md` is a copy of the operating guide. Load it only when the guide is not in context.
- `references/plain-language-examples.md` has before-and-after pairs. Open it when a rewrite for one rule is not working.
- `references/examples/chat.md` has replies to a person. Open it for pushback, a correction, a status report, or "I don't know".
- `references/examples/artifacts.md` has commits, PR descriptions, and README first lines. Open it when writing one.
- `references/examples/code.md` has findings on code. Open it for a finding written outside `toby-code-review`.

Copy the approach of an example, and write new words for the situation.

## Rewrite requests

Return the revised text first. Add a note only when the user asked for the reason or two rules conflicted, and cite the rule by its number.
