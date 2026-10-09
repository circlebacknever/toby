---
name: toby-plain
description: >-
  Rewrites the previous reply, or a file the user points to, in plain everyday
  English. Trigger only when the user explicitly invokes the skill by name or
  with the `/toby-plain` slash command. Do not trigger on "explain this", "I
  don't understand", or a request to reword text, which toby-explain and
  toby-voice cover.
disable-model-invocation: true
argument-hint: "[optional file path or note]"
---

# Toby Plain

I ran this because I don't understand what you just said. Maybe the words were too technical, or maybe there was so much of it that I lost the point. Say it again so I can follow it.

## What to rewrite

Rewrite the file or the text I point to. If I don't point to anything, rewrite your last reply.

If I add a note like "the part about caching", rewrite only that part.

Put the rewrite in the chat. Don't change the file unless I ask you to, because someone else might be reading it.

## How to say it

Lay out the rewrite in this order:

1. If I need to decide something, ask that first, give at most three options, and recommend one.
2. Say what's going on and what it means for me, in one to three sentences.
3. Put steps, options, and separate problems in a list, with one idea in each item.
4. End with my next step, if I have one.

Then check the words:

- Use the words I'd use, with no metaphors or idioms. When you need a technical word, tell me what it means in everyday words. For example, a cache is a saved copy the app reuses so it doesn't have to fetch the same thing twice.
- Keep a technical word only if I'll see it again or have to type it. Explain it the first time it comes up.
- If you mention something that only exists here, like a file, a function, or a term from this lesson, tell me what it is. If you won't explain it, leave it out.
- Skip labels like finding numbers, rule numbers, and severity tags, unless I need them to find something.
- Keep sentences short, with one idea in each, and keep each paragraph to three sentences or fewer.
- Call each thing by the same name the whole way through. If you call it "the cache" once, don't call it "the store" later.
- If an idea is abstract, give me an example from what I'm working on or learning.

## What to keep

Keep every warning, every number, and every question I still need to answer from the original. Cut anything repeated, and cut how you worked it out unless I need that to follow along.

Do not add any new facts, and do not run any new checks. The rewrite says the same thing as the original, in words I can follow.

If the original was confusing because it skipped a step or contradicted itself, tell me that plainly, and tell me which part is missing.

The rewrite is usually shorter than the original. Make it longer only when the original skipped a step I need.

## How to start and finish

Start with the content. Don't open with "In plain English" or an apology, and don't end by offering more help.

Before you send it, read it as someone who has never seen this topic. If they'd have to read a sentence twice, rewrite that sentence.
