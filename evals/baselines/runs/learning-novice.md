## Reply 1
You're starting from zero, so we'll take this in steps — a guess before each one, then the real answer. First step: how a database finds a row without any help. Before I explain: you search a table of a million rows for one email address, no index exists. What do you think the database does to find it?

## Reply 2
Faster is right. Without an index, the database does a full table scan: it checks every one of the million rows, one at a time. An index is a separate structure that keeps the values sorted, so the database jumps straight to matches instead of walking the whole table. Next: how that sorted structure survives the table changing under it — inserts, deletes, updates.

## Reply 3
Then the last piece before you try applying this yourself. The database doesn't use an index just because one exists — it estimates how many rows will match, and only bothers with the index when that number is small next to the table size. Guess: why would that estimate matter if the query would still match half the rows in the table?

## Reply 4
No — with most rows active, that index buys you nothing. It would still point you to roughly half the table, and chasing each match means jumping between the index and the real row instead of just reading rows in order, which is slower than the scan it was supposed to beat. Indexes pay off on selective filters, where only a sliver of rows match — status is usually the wrong column for one. So what's the rule you'd write down for when an index is worth using?
