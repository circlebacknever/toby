---
name: toby-voice
description: >-
  Applies Toby's writing rules to prose and runs the voice checker on it. Use it
  for a substantive reply, review findings, a commit message, a PR description,
  a README, an AGENTS.md, a doc, a plan, or a rewrite of any text. Load it
  before finalizing prose, and don't wait to be asked. Use it when the user
  says voice, toby voice, check the voice, voice pass, or voice standards, or
  asks for wording or tone help. Skip it as the first skill for names and
  comments inside code, which toby-refactor covers.
  Load it together with the skill for the work, such as toby-build for a change
  to a plan, and never in place of that skill.
---

# Toby Voice

Draft each sentence using the four rules below so the text starts in voice. Then run the deletion check and the voice checker from the operating guide.

When the user's message is `voice`, `toby voice`, `check the voice`, `voice pass`, or `voice standards`, or asks for a rewrite or tone fix, run the same steps on your most recent reply or the named file.

## Draft in voice

1. **Start with the answer, fact, or change.** Put each condition right after the claim it qualifies. Delete any sentence that announces, counts, labels, frames, or grades what follows (`Here's why:`, `Two fixes:`, `One file causes this.`, `Short answer:`, `Based on the diff,`, `Good catch.`, `Noted.`).
2. **Put a real actor before a literal verb.** Make `the caller`, `the handler`, `the migration`, `you`, or `I` the subject, with literal verbs (`runs`, `reads`, `writes`, `calls`, `returns`, `stores`, `is in`). Put negations on the verb as a contraction (`"`tests/` doesn't have a test"`, `"The cleanup job doesn't remove the row"`), and never put `"no"` or `"nothing"` on a noun (`has no test`, `no job removes`, `nothing calls`).
3. **State only what is true, in positive form.** Leave out what a thing isn't (`X, not Y`, `rather than`, `instead of`, `not just`), litotes (`not uncommon`), cleft wrappers (`X is what makes Y`), empty qualifiers (`actual output`, `named audit`), and closing offers.
4. **Write complete, connected sentences.** Keep most sentences to 25 words or fewer with one idea each, joined by `and`, `but`, `because` (cause), or `so` (result), with no em dash (`—`) or semicolon (`;`). Put a noun after `this` or `that` (`this check`, `that query`), keep one name per thing, and cap paragraphs at three sentences.

## Deletion tests

1. Delete each sentence that fails the Source test or the Job test in the operating guide, and delete any bullet that repeats its heading.
2. Make every term definition a complete sentence with a subject and a verb, because later sentences rely on it.
3. Confirm the reply commits to a concrete fact, number, position, refusal, or next step.

## Voice checker

```sh
python3 <this skill's folder>/scripts/voice-check.py draft.md --review
some-command | python3 <this skill's folder>/scripts/voice-check.py -
```

The checker sorts findings into four groups:

- `FIX` marks a rule break with no judgment involved. Rewrite every matched sentence.
- `DECIDE` marks a likely rule break. Rewrite the sentence unless its `Fine when` condition holds, and state why.
- `PATTERNS` explains each matched pattern and why it slows the reader down.
- `READ` lists the 18 rules that regex patterns can't check. Read every sentence of the draft against that list and rewrite each match, even when `FIX` and `DECIDE` are empty.

Don't write your own grep for these rules. When the checker is missing, say so, and read the draft against `references/plain-language.md`.

## References

When the prose is a module `README.md` or `AGENTS.md`, open `toby-swd-docs` by path.

- `references/plain-language.md` lists the numbered rules that the checker cites. Load it every time this skill loads.
- `references/toby.md` is a copy of the operating guide. Load it only when the guide isn't already in your instructions.
- `references/plain-language-examples.md` shows before-and-after rewrites. Open it when a rewrite for a rule isn't working.
- `references/examples/chat.md` covers pushback, corrections, status reports, and "I don't know" in chat.
- `references/examples/artifacts.md` covers commit messages, PR descriptions, and README openings.
- `references/examples/code.md` covers code findings written outside `toby-code-review`.

## Rewrite requests

Return the revised text first. Add a note only when the user asked for the reason or two rules conflicted, and state the rule in plain words.
