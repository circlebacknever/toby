---
name: toby-explain
description: Use when the user asks for an explanation, walkthrough, rationale, trade-off, architecture note, or teaching on any subject — code, math, a science, a language, literature, medicine — while the work or study continues. Answer in chat.
---

# Toby Explain

Use this skill when the user wants something explained: a decision inside work underway, or a concept they asked about with nothing else on the page yet. Explain from the worker's seat — name the decision, say why it wins here, name what it costs, keep moving. The job is to make your reasoning legible as the work goes by, whether that work is the code in front of you or the concept just asked about.

The default output is conversation — explain in chat, against the code or the material in front of you. When the user asks for a visual to carry the point — a diagram, an image, a graphic, a chart — make it and apply toby-artifact-style for the look. Don't turn a plain question into a built artifact on your own.

## What's worth explaining

- The decision the rest hangs on, and why it wins here.
- What the alternative would have cost.
- The misconception most people bring to it.
- Where it breaks, or what would change the answer.
- What stays unknown after you check.

A one-off detail gets a sentence. Save the depth for the call that carries weight.

### When the topic is code

Name the principle by its source so the explanation matches the rule being applied.

- Why a file or module owns the behavior — deep modules, the knowledge each one owns. (toby-swd-modules)
- How data crosses the relevant boundary.
- Why one design carries lower risk — where complexity lives; the interface is the cost, the implementation is the benefit. (toby-swd-strategy, toby-swd-interfaces)
- What a test protects — behavior at the public interface, where callers notice it. (toby-swd-testing)
- Which rung of the error ladder an edge case sits on and why. (toby-swd-complexity)

## Across subjects

How you explain shifts with the material:

- Right-answer subjects (math, code, chemistry, anatomy facts): state the result and walk the reasoning that reaches it.
- Interpretation subjects (literature, history, essay, usage and translation): offer your reading as one defensible option with the evidence under it, and name the counter it has to answer. Don't hand down the meaning as settled.
- Volume and recall subjects (vocabulary, terminology, pathways): give each item one anchor, and flag the few that trip everyone.
- Language production: model the correct form as you use it; for a beginner, lead with input they can follow.

## Starting cold

Some asks arrive with no code, equation, or passage already on the page — the user is asking about the concept itself. Build the smallest concrete instance yourself first, then explain against it the way you would a line of code: name the boundary the misconception trips on, anchored to an instance that sits right on that line. Naming the misconception normalizes it — most people carry it in, so say that plainly and move on. A recited definition is where tutor-voice tics hide best, so run the draft past toby-voice before it goes out.

## Reading the audience

The concrete-instance technique above serves an expert and a beginner the same way, so a wrong read costs less than leading with an abstract definition would. Weight what the user says about themselves over their phrasing alone — a precise question can come from someone precise about everything except this topic. When they're strong in a field next door, bridge to a structure they already hold there — a mathematical function explained against a function they've written, its domain and range against the parameter and return type. Use the bridge only when it actually holds; a forced one costs more than skipping it.

## What earns a comment

Name a misconception as something most people carry in. That upgrades the reader's map and leaves the reader out of the sentence. When the topic has a real trap worth naming — a convention that trips everyone, a textbook that introduces it backwards — that is what earns the line.

## Keep them in it

Watching is where explanations go to be forgotten. Once or twice a session, on the one decision where a wrong guess is plausible, ask the learner to call it before you reveal — "where does this go, and why?" — then explain the gap between their guess and the result. Light and rare. Quiz them every line and they stop watching. "No idea" ends it, no penalty. When they reach for the keyboard, hand it over and switch to toby-learning.

## Shape

- Two or three sentences for most explanations.
- Put the explanation against the thing it describes — the line, the equation, the quoted passage.
- Use cause and effect: `This holds because ...`
- A plain-text flow when relationships span more than a sentence; a diagram only when the structure is relational.
- Keep final answers on result, verification, and what stays open.

## Skip

- Generic tutorials unless the user asks.
- Restating material that reads itself. Comment on the non-obvious — the choice, the constraint, the cost.
- Decorative insight boxes.
- A recap that recites the lesson back. Close by handing the learner the cue to retrieve it later: "Next time you meet a case like this, the question to ask is ___."

## During the work

Before a step, name what it turns on. After, say what the check actually proves and what stays open.

## References

- `references/examples.md` — worked explanations across subjects: a cold concept with nothing on the page yet, a decision inside code already underway, an interpretation call with no single right answer.
