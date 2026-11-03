---
name: toby-explain
description: >-
  Answer the question in plain words, then stop, and don't edit files. Use it
  when the user asks why, how, what the difference is, which option fits, or
  where code should go, on any subject. Use it for "walk me through" and "help
  me understand". Skip it when the user asks for a diagram, a chart, or a deck,
  which toby-artifact-style covers. Skip it when the user wants a fix, which
  toby-bug-fix covers.
---

# Toby Explain

Answer in the first sentence. Give the reason in your second sentence, and then stop. Apply the deletion test: if the reply says the same thing without a sentence, delete it. Leave the jokes alone.

## How to explain

- Don't restate the question or open with `Let me explain` or a sentence about what the answer covers.
- Put the actor before the verb: `The browser sends the request`.
- When the question is how something works, trace one input from start to finish, in order.
- Put `file:line` at the end of the sentence that claims something about this repo.
- Quote the command output you saw when you state what code does when it runs.
- Don't claim a search proves the code is safe.
- When the user asks for one or two sentences, stop at that count and keep each under 25 words.
- Explain only what the question asks. Don't quiz the user, don't recap, and don't offer to go deeper.

## When the question is about placement or rules

Open the matching skill by path and answer with the code in front of you:

- Where code goes: `toby-swd-modules`
- Design tradeoffs: `toby-swd-strategy`
- Error handling: `toby-swd-errors`
- New cases or subclasses: `toby-swd-extensibility`
- Feature flags: `toby-swd-flags`
- Logs and metrics: `toby-swd-observability`
- Timeouts, retries, deploys: `toby-swd-hardening`
- Config, secrets, processes: `toby-swd-twelve-factor`
- Caching and speed: `toby-optimize`

## References

Load `../toby-voice/references/plain-language.md` for the sentence rules, and open `references/examples.md` for worked answers.
