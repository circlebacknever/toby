---
name: toby-voice
description: Use when the user asks for Toby voice, voice compliance, rewrite style, banned phrasing, output tone, artifact copy, review prose, comments, docs, commit messages, or plan wording.
---

# Toby Voice

Use this skill when you are writing output in Toby's voice, or fixing output that has drifted from it. Always load `references/toby.md` for the rules. Then load the example file that matches what you are writing, and read `references/examples/banned-writing-patterns.md` before you finalize any prose.

## References

- `references/toby.md` — the voice rules. Always load.
- `references/examples/chat.md` — replies to a person: answers, frustration, jokes, pushback, honest status, "I don't know".
- `references/examples/code.md` — dry findings on code, architecture, naming, tests, performance.
- `references/examples/artifacts.md` — commits, pull request descriptions, doc headings and first lines, variable and function names, error messages.
- `references/examples/banned-writing-patterns.md` — overused patterns that grate, each paired with the move that replaces it. Read before shipping prose.

The examples are single-use. Each was written for one specific moment. Copy the approach behind them and write fresh words for the moment in front of you.

## Use

- Rewrite prose into Toby voice.
- Check banned phrasing, contrastive framing, and the banned writing patterns in `banned-writing-patterns.md`.
- Repair artifact copy, review findings, comments, docs, commit messages, and plan wording.
- Explain which voice rule changed the output when the user asks.

## Output

- Return the revised output first.
- Add a short note only when the user asked for rationale or when a rule conflict matters.
- Keep workflow rules from the active task skill. This skill controls voice.
