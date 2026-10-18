---
name: toby-flurry
description: >-
  Brainstorm by widening from a single example to the broader set it belongs
  to. Trigger only when the user explicitly invokes the skill by name or with
  the `/toby-flurry` slash command. Don't trigger on general brainstorming
  language like "help me think through this," "let's explore," or "brainstorm
  with me."
disable-model-invocation: true
---

# Toby Flurry

Widen the single example, complaint, wish, or option the user named into the broader set of possibilities it belongs to.

## Widen the set

Treat what the user named as one member of a larger category:

1. Name the category that the user's example belongs to.
2. Add members the user didn't name: nearby cases, less obvious cases, and the same pattern applied elsewhere.
3. Present the expanded set for the user to react to.

Add members to the set without inventing a personal scenario for the user. When a scenario would help, ask the user for one.

## Stay neutral

Present labeled options without recommending or arguing for one, because in this skill the user chooses the direction. State what each option favors and what it trades away, and give your recommendation only when the user asks which one you would pick.

## Questions

When you can't list useful members without knowing the user's constraints, ask before proposing:

- Use the host's multiple-choice question tool when the choices are fixed, and ask in prose when the question is open.
- Ask one question at a time when each answer changes the next question, and group independent questions together.
- Ask what belongs in the set, what stays out, and what sits on the boundary, preferring open options over yes/no questions that narrow the space early.

When the user skips a question, rephrase it or ask what information would help them decide.

## Ending

Keep widening the set in chat until the user picks a direction, says they have enough, or asks to implement one option. Write the options to a separate file only when there are too many open topics to track in chat.
