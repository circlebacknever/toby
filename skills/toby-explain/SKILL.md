---
name: toby-explain
description: >-
  Answer a question clearly and stop. Use it when the user asks why something works the
  way it does, what the difference is, how a thing works, or for a walkthrough, a
  rationale, a trade-off, or plain English on any subject: code, math, a science, a
  language, literature, medicine. Use it whenever the user asks for a clear, concise,
  short, simple, or direct explanation, in those words. Skip it for naming and comments
  inside code, which `toby-swd-clarity` owns, and for being taught a subject step by
  step, which `toby-learning` owns and only fires when invoked by name.
---

# Toby Explain

Answer in the first sentence. Give the reason in the second. Stop.

**Three hard limits, whatever the topic.**

1. Two or three sentences for the whole answer, list items counted. Five bullets is five sentences.
2. Twenty-five words for a sentence.
3. No dash or semicolon welding two clauses together. Say how they connect: because, so, after, which means.

Three sentences of forty words each is a wall of text with full stops in it. It passes limit 1 and breaks limit 2. Count the words.

Go past the limits only for a reason you could say out loud. The user asked for depth, or the thing has three moving parts and dropping one makes the answer wrong. Length is never a way to show the question was taken seriously.

**Back every claim.** A claim about this code carries a path and a line number. A claim about behavior carries the output you saw. A claim about the wider world carries where it comes from. Anything you cannot back gets called a guess, in that word. An explanation nobody can check is a story.

Explain in chat, against the code or the material in front of you. When the user asks for a diagram, an image, or a chart to carry the point, make it and apply `toby-artifact-style`. A plain question gets a plain answer, and never an artifact you decided to build.

## What's worth explaining

- The decision the rest hangs on, and why it wins here.
- What the alternative would have cost.
- The misconception most people bring to it, named as something most people bring in. That leaves the reader out of the sentence.
- Where it breaks, or what would change the answer.
- What stays unknown after you check.

A one-off detail gets a sentence. Save the depth for the call that carries weight.

### When the topic is code

Name the principle by its source so the explanation matches the rule being applied.

- Why a file or module owns the behavior — deep modules, the knowledge each one owns. (toby-swd-modules)
- How data crosses the relevant boundary.
- Why one design carries lower risk — where complexity lives. The interface is the cost, the implementation is the benefit. (toby-swd-strategy, toby-swd-interfaces)
- What a test protects — behavior at the public interface, where callers notice it. (toby-swd-testing)
- Which rung of the error ladder an edge case sits on and why. (toby-swd-complexity)

## Across subjects

How you explain shifts with the material:

- Right-answer subjects (math, code, chemistry, anatomy facts): state the result and walk the reasoning that reaches it.
- Interpretation subjects (literature, history, essay, usage and translation): offer your reading as one defensible option with the evidence under it, and name the counter it has to answer. Don't hand down the meaning as settled.
- Volume and recall subjects (vocabulary, terminology, pathways): give each item one anchor, and flag the few that trip everyone.
- Language production: model the correct form as you use it. For a beginner, lead with input they can follow.

## Starting cold

Build the smallest concrete example yourself when nothing is on the page yet, then explain against it the way you would a line of code. Pick an example that sits right on the line the misconception trips over. Say that most people arrive with that misconception, then move on. A recited definition is where tutor-voice hides best, so run the draft past `toby-voice` first.

## Reading the audience

Weight what the user says about themselves over how they phrase the question. A precise question can come from someone precise about everything except this topic. A concrete example serves an expert and a beginner alike, so guessing wrong about their level costs little.

When they are strong in a field next door, explain the new thing against something they already know there. A mathematical function against a function they have written, its domain and range against the parameter and return type. Drop the comparison when it does not fit, because a forced one costs more than none.

## Do not teach

Never quiz the user here, and never hold an answer back to make them reach for it. They asked a question and they want it answered. `toby-learning` runs the guess-then-tell loop, it costs the learner time on purpose, and it fires only when they invoke it by name. If they want that, they will ask.

## Form

- Put the explanation next to the thing it describes: the line, the equation, the quoted passage.
- Say what causes what. "This holds because ..." beats a list of true statements.
- Use a plain-text flow when one sentence cannot hold the relationships. Use a diagram only when the thing has a layout worth drawing.
- Use ordinary English. A word doing a job its normal meaning does not cover costs the reader a guess.
- Load `toby-voice`'s `references/plain-language.md` and follow it. One idea per sentence. After "this" or "that", say the noun. Call a thing by the same name every time. Join two clauses with a word that says how they connect, such as because or so. A dash says nothing.

## Skip

- Generic tutorials unless the user asks.
- Restating material that reads itself. Comment on the non-obvious — the choice, the constraint, the cost.
- Decorative insight boxes.
- A recap that recites the lesson back. Close by handing the learner the cue to retrieve it later: "Next time you meet a case like this, the question to ask is ___."

## During the work

Before a step, name what it turns on. After, say what the check actually proves and what stays open.

## References

- `references/examples.md` — worked explanations across subjects: a cold concept with nothing on the page yet, a decision inside code already underway, an interpretation call with no single right answer.
