# Learning suite

Does the skill change what the agent does, against plain chat with the same
question? The user's complaint is that it does not, and this is how that gets
settled.

Both arms answer the same four learner turns, fixed in advance so the input is
identical. One arm loads `toby-learning`. The other has the operating guide and
nothing else.

## The scripted learner

Turn 1
> Why is this query still slow? I added an index on `created_at` but EXPLAIN
> still shows a seq scan. The table has 2M rows.
> `SELECT * FROM events WHERE created_at > now() - interval '30 days'`

Turn 2
> Oh. So should I just add more indexes?

Turn 3
> I think it's because the planner thinks the index is slower? Not sure.

Turn 4
> ok that makes sense

Turn 4 is the test the skill writes a rule for. `ok that makes sense` on a dense
point is the nod-along, and the skill says to hand the learner the next slice on
that exact point rather than accept it.

## What gets counted

Per arm, across the four replies:

- **Elicitations** — questions that force the learner to produce something from
  their own model. A question answerable from the text just sent does not count.
- **Assertions** — explanatory sentences the learner did not have to work for.
- **Keyboard handovers** — turns that end with the learner owing something.
- **Nod-along handled** — does turn 4 give them work on the dense point, or
  accept the assent and close.
- **Rule stated back** — is the learner ever asked to restate the rule in their
  own words.

## What a failing skill looks like

The two arms produce the same counts. A skill that only makes the explanation
tidier has not taught anything the chat would not have.
