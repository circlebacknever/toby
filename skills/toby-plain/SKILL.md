---
name: toby-plain
description: >-
  Rewrites the previous reply, or a file the user points to, in plain everyday
  English. Trigger only when the user explicitly invokes the skill by name or
  with the `/toby-plain` slash command. Don't trigger on "explain this", "I
  don't understand", or a request to reword text, which toby-explain and
  toby-voice cover.
disable-model-invocation: true
argument-hint: "[optional file path or note]"
---

# Toby Plain

Rewrite the previous reply, or the file or passage the user points to, in plain everyday English so a reader who hasn't seen the topic can follow every sentence on the first read.

## What to rewrite

Rewrite the file or passage the user names, or rewrite your previous reply when the user names nothing. When the user adds a scope note such as "the part about caching", rewrite only that part. Put the rewrite in chat and leave the file on disk unchanged unless the user asks to edit the file.

## Layout and words

Order the rewrite in four parts:

1. When the user must decide something, ask that question first, give at most three options, and recommend one.
2. State what is happening and what it means for the user in one to three sentences.
3. Put ordered steps, options, and separate problems in a list, with one idea per item.
4. End with the user's next action when one exists.

Check every word and sentence:

- Use everyday words without metaphors or idioms. Keep a technical term only when the user will see it again or must type it, and define it in everyday words the first time it appears.
- Explain any repo-specific file, function, or term, or leave it out, and omit finding numbers, rule numbers, and severity tags unless the user needs them to locate something.
- Keep one name for each thing throughout, and give a concrete example from the user's task when an idea is abstract.

## What to keep

Keep every warning, number, and open question from the original, and cut repeated points and how you derived the answer unless the user needs that reasoning. Don't add new facts or run new checks. When the original was confusing because it skipped a step or contradicted itself, state which part was missing or contradictory.

## Start and finish

Start directly with the rewritten content without "In plain English" or an apology, and don't end with an offer of more help.
