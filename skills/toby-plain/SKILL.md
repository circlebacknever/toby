---
name: toby-plain
description: >-
  Rewrites the previous reply, or a file the user points to, in plain everyday
  English. Trigger only when the user explicitly invokes the skill by name or
  with the `/toby-plain` slash command. Don't trigger on "explain this" or
  "I don't understand", which toby-explain covers, or on general voice repair,
  which toby-voice covers.
disable-model-invocation: true
argument-hint: "[optional file path or note]"
---

# Toby Plain

Rewrite the text the user names, or your previous reply when the user names nothing. Put the rewrite in chat, and leave files on disk unless the user asks for an edit. Apply the deletion test to every sentence: if the text says the same thing without it, delete it.

## Fix four things

1. **One point per paragraph.** State the one fact in a single short sentence, and cut the preamble and the recap.
2. **Actor before verb.** Write `The server cancels the token`.
3. **Everyday words.** Replace jargon and long noun chains with what happens, and explain any term the user must type or see.
4. **Outcome before internals.** State what the user sees first, then walk one concrete case in the order it happens.

Keep every warning, number, and open question from the original. Start with the answer, and skip any closing offer. Open `../toby-voice/references/plain-language-examples.md` for the assistant register to cut and the before-and-after pairs.
