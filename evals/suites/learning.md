# Learning suite

Two questions. Does the skill change what the agent does? And does a beginner
get taught without being buried?

## Suite A — does it change anything

Four scripted learner turns in `fixtures/learner-turns.md`, answered twice: once
with the skill loaded, once with the operating guide alone. Recorded runs are
`runs/learning-with-skill.md` and `runs/learning-plain-chat.md`.

Counted per arm: questions that force the learner to produce something, turns
that end with the learner owing something, and whether turn 4's "ok that makes
sense" gets accepted or handed work.

Recorded result: with the skill, three of each and the assent refused. Plain
chat, none of either and the assent accepted.

## Suite B — the beginner path

`fixtures/learner-novice.md`. The learner invokes the skill and says they know
nothing. This is the case the skill was rebuilt for, and it is the one that
fails quietly, because a wall of text reads as thorough.

A passing run:

- asks for a guess before each step, and says a wrong guess is fine
- answers every guess in the same message that follows it, always
- runs to five sentences or fewer per reply
- covers one step per reply and says what the next step is
- ends by asking the learner to state the rule
- uses no word outside its ordinary meaning

A failing run withholds an answer to make the learner work for it, asks a second
question in place of an answer, or sends a reply longer than five sentences.

Recorded result in `runs/learning-novice.md`: four replies at three to four
sentences each, a guess in front of every step, and every guess answered.
