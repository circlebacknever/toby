# Learning suite

This suite tests two questions: whether `toby-learning` changes how the agent teaches compared to plain chat, and whether it teaches a complete beginner in turns of five sentences or fewer.

## Suite A: skill vs. plain chat

The agent answers the four scripted learner turns in `fixtures/learner-turns.md` twice: once with `toby-learning` loaded (`runs/learning-with-skill.md`) and once with the operating guide alone (`runs/learning-plain-chat.md`).

For each arm, count how many turns ask the learner to produce a prediction or step, how many turns end by waiting for the learner's response, and whether turn 4's `"ok that makes sense"` receives an immediate application prompt.

With the skill loaded, the recorded run asked three production questions, waited for the learner at the end of three turns, and gave the learner a small application task after `"ok that makes sense"`. Without the skill, the agent lectured without asking check questions and accepted `"ok that makes sense"` without testing understanding.

## Suite B: the beginner path

Suite B runs `toby-learning` on `fixtures/learner-novice.md`, where the learner says they know nothing about database indexes.

A passing run:

- asks for a quick opening guess before explaining a new concept, and says `"I don't know"` is fine
- gives the full explanation in the very next reply after the learner's opening guess, without answering a guess with another question
- keeps every reply to five sentences or fewer (counting list items)
- covers one step per turn
- closes by having the learner state the reusable one-line rule in their own words
- uses everyday English without unexplained jargon

A failing run holds back the explanation after the learner's opening guess, answers a guess with a second question, or sends a reply longer than five sentences.
