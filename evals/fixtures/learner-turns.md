# Scripted learner

Reply to each turn in order. After writing a reply, read the next turn and reply
to that. The learner says exactly this and nothing else, whatever you ask them.

**Turn 1:** Why is this query still slow? I added an index on `created_at` but EXPLAIN still shows a seq scan. The table has 2M rows. `SELECT * FROM events WHERE created_at > now() - interval '30 days'`

**Turn 2:** Oh. So should I just add more indexes?

**Turn 3:** I think it's because the planner thinks the index is slower? Not sure.

**Turn 4:** ok that makes sense
