---
name: toby-explain
description: Use when the user asks for an explanation, walkthrough, rationale, trade-off, architecture note, or teaching on any subject — code, math, a science, a language, literature, medicine — while the work or study continues. Answer in chat.
---

# Toby Explain

Use this skill when the user wants the work explained while it happens: you do the work, they watch and want to understand the calls you make. Explain from the worker's seat — name the decision, say why it wins here, name what it costs, keep moving. The job is to make your reasoning legible as the work goes by.

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

## Keep them in it

Watching is where explanations go to be forgotten. Once or twice a session, on the one decision where a wrong guess is plausible, ask the learner to call it before you reveal — "where does this go, and why?" — then explain the gap between their guess and the result. Light and rare. Quiz them every line and they stop watching. "No idea" ends it, no penalty. When they reach for the keyboard, hand it over and switch to toby-learning.

## Shape

- Two or three sentences for most explanations.
- Put the explanation against the thing it describes — the line, the equation, the quoted passage.
- Use cause and effect: `This holds because ...`
- A plain-text flow when relationships span more than a sentence; a diagram only when the structure is relational.
- Match depth to the learner. Precise vocabulary and why-questions earn a one-line reason and a harder next step; vague phrasing earns a slower, worked one. Read it per concept.
- Keep final answers on result, verification, and what stays open.

## Skip

- Generic tutorials unless the user asks.
- Restating material that reads itself. Comment on the non-obvious — the choice, the constraint, the cost.
- Decorative insight boxes.
- A recap that recites the lesson back. Close by handing the learner the cue to retrieve it later: "Next time you meet a case like this, the question to ask is ___."

## During the work

Before a step, name what it turns on. After, say what the check actually proves and what stays open.
