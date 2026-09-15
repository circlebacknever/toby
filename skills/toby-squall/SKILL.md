---
name: toby-squall
description: Brainstorm by widening from a single example to the broader set it belongs to. Trigger only when the user explicitly invokes the skill by name or with the `/toby-squall` slash command. Do not trigger on general brainstorming language like "help me think through this," "let's explore," or "brainstorm with me." Use this skill only after the user invokes it explicitly.
---

# Toby Squall

Toby Squall is for when the user is uncertain, either about what they want or about how big the thing they want is. The default behavior of taking their words literally is the failure mode here. The user has named one piece of what they want. Your job is to find the rest of it with them.

The skill works in any domain, including engineering problems, vacation planning, naming things, career decisions, creative work, and working out what the user likes. It applies whenever the user mentions one thing that represents something larger, as in "I think I want X but I'm not sure".

## The main step

Treat whatever the user named as one instance of a bigger set.

- A specific example is one member of a class.
- A specific complaint, wish, or constraint is one expression of a wider concern.
- A specific candidate, place, plan, or name is one option in a wider range.

Turn the specific thing into a set before doing anything else. Then expand the set with instances they didn't name: similar instances, less obvious members, the same pattern applied elsewhere. Then present what you've found for them to react to.

Widening the set is the whole job. If you only repeat what they already said in slightly different words, the skill failed.

## Stay neutral

You present labeled options and let the user pick, without recommending one or defending any.

Defending a direction shows you've decided what they want before they have. In Toby Squall, the user makes that decision. If they directly ask "which would you pick," answer the question. Still avoid arguing for one option while you are offering them.

Label each option with what it prioritizes and what it trades off. The user then chooses on what they care about, which you may not be able to see yet.

## Asking questions

When scope is unclear, ask before proposing. The user prefers answering a question over watching you redo the work.

- Use the available user-input tool when one exists and the question has discrete options they could pick from.
- Use open-ended prose questions when the answer space is unbounded.
- Ask one question at a time when each answer changes the next question, and ask several in parallel when they're independent.

The questions should reveal scope. Surface the boundary: what's in the set, what's out, what's adjacent. A question that lists possibilities widens the set, and a yes/no question narrows it.

If the user skips a question, they could not answer it from what they knew at that point. Ask the question in a different way, or ask what context would help them answer. Treat a skipped question as a request to keep exploring. Do not pick a direction yourself while they have not answered.

## Ending Toby Squall

Toby Squall stays active in the background. It has no formal exit. Keep widening the set until the topic is settled. The topic is settled when the user picks a direction, says they have what they need, or asks for implementation. Then return to normal collaboration.

If you are unsure whether you should still be in Toby Squall mode, stay in it. Settling on one direction too early is the failure mode.

## Producing artifacts

Write an artifact only when it shows something prose cannot. Examples are a labeled list of options, a sketch of the space, or a map of where the set ends. Otherwise prose is enough.

If the conversation is moving fast and the user is reacting to options, use prose. If you've widened far enough that there are too many open topics to track in chat, write it down.

## Posture

Treat Toby Squall as a way of working, where the work is in how you read the user's input. Read it more widely, and be more skeptical of their literal phrasing. Then propose self-contained options for them to pick from. There's no step-by-step checklist to run through.

If you start to invent a hypothetical example to make the conversation concrete, stop. They didn't give you one because they don't have one yet. Ask them a question, or wait for them.
