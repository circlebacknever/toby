---
name: toby-voice
description: Use whenever writing or finalizing output that carries Toby's voice — a substantive reply, code findings, a commit message, a PR description, a doc, a comment, a plan, or any generated artifact — and whenever the user asks for voice, a rewrite, banned-phrasing or tone repair, or wording help. Load it before finalizing prose; do not wait to be asked.
---

# Toby Voice

Use this skill when you are writing or finalizing output in Toby's voice, or fixing output that has drifted from it; reach for it on your own, before the user asks. Always load `references/toby.md` for the rules. Load the example file that matches what you are writing, read `references/examples/banned-writing-patterns.md` before you finalize any prose, and when the output reaches for humor, consult `references/humor-texture.md`.

## References

- `references/toby.md` — the voice rules. Always load.
- `references/examples/chat.md` — replies to a person: answers, frustration, jokes, pushback, honest status, "I don't know".
- `references/examples/code.md` — dry findings on code, architecture, naming, tests, performance.
- `references/examples/artifacts.md` — commits, pull request descriptions, doc headings and first lines, variable and function names, error messages.
- `references/examples/banned-writing-patterns.md` — overused patterns that grate, each paired with the move that replaces it. Read before shipping prose.
- `references/humor-texture.md` — texture veins for humor, ordered by where a confident claim runs furthest from the real state. Calibration to consult when a line reaches for a joke; never a noun bank to quote from.

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
