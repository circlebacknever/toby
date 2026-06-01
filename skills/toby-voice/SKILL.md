---
name: toby-voice
description: Use when the user asks for Toby voice, voice compliance, rewrite style, banned phrasing, output tone, artifact copy, review prose, comments, docs, commit messages, or plan wording.
---

# Toby Voice

Use this skill for explicit Toby voice passes and repair work. Always load `references/toby.md`, apply it to the current output, and keep task-specific skill instructions for method.

## Use

- Rewrite prose into Toby voice.
- Check banned phrasing and contrastive framing.
- Repair artifact copy, review findings, comments, docs, commit messages, and plan wording.
- Explain which voice rule changed the output when the user asks.

## Output

- Return the revised output first.
- Add a short note only when the user asked for rationale or when a rule conflict matters.
- Keep workflow rules from the active task skill. This skill controls voice.
