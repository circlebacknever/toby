## Per file

holdout-01.md: 4 distracting sentences.

- "Two follow-ups are agreed." Task 2. Setup sentence. It names a count and makes the reader wait for the two bullets that follow.
- "The session read runs once per page load, so Option B makes that read 7 ms slower at p95 on every page load." Task 3. Given-fact test. The 7 ms gap was measured in staging, and the sentence states it as the production result without "in staging".
- "This one is in how the parser reads your export, so `--date-format dmy` is the fix to try." Task 6, turn 3. Claim of fixed about something that did not change. Nothing in Ledgerline changed, and nobody has run the flag, yet the sentence calls the flag "the fix".
- "Start with those 12, since the other 27 are within $1 of the ledger." Task 6, turn 5. Consecutive replies ending on the same move. Turn 4 ended on "Check those 39 before you call the run good.", and turn 5 ends on another instruction about which rows to check.

holdout-02.md: 9 distracting sentences.

- "It reads exports from four banks, which are Chase, Monzo, Wise, and ING." Task 1. Padding and a category named before its members. The words "four banks, which are" can be deleted with no loss.
- "Two follow-ups are agreed." Task 2. Setup sentence. It names a count, and the next sentence then splits the items into a mirrored "One is ... the other is" pair.
- "Because every page load runs one session read, Option B adds that 7 ms difference at p95 to each page load." Task 3. Given-fact test. The staging measurement is stated as a production effect, and the "in staging" qualifier is dropped.
- "The handler builds one object per row and then reads only `.length`." Task 4. Actor test. The database client builds the row objects, and the task never said what `findMany()` builds.
- "**Fix:** If `db` is a Prisma client, `db.users.count()` returns the number from the database without fetching the rows." Task 4. Given-fact test. The task never names Prisma, so the writer guessed the library and then stated how it behaves.
- "The parser read the dates in the wrong order." Task 6, turn 2. Connection test. The next sentence says the same thing in detail with no connector, so this opener is a summary the reader reads twice.
- "Three in one week is a lot." Task 6, turn 3. Human-moment sentence. The frustration gets its own sentence of reaction, and "a lot" is a vague judgment with no fact behind it.
- "No." Task 6, turn 5. Connection test. The verdict stands alone, and the reader has to link it to the reason in the next sentence.
- "Start with the 12, because the bank and the ledger disagree on their amounts." Task 6, turn 5. Actor test. A bank export and a ledger cannot disagree, because only people disagree. The amounts differ.

holdout-03.md: 5 distracting sentences.

- "The session read runs once per page load, so its latency is part of every page load." Task 3. No job. The second clause restates the first clause, so the reader learns nothing new.
- "Because the session read runs once per page load, Option B raises its staging p95 from 2 ms to 9 ms on every page load." Task 3. Literal test. A staging p95 is one measured number, so it cannot be raised on each page load.
- "I read the diff and did not run the handler, so a cache elsewhere in the handler is unchecked." Task 4. Given-fact test. The task mentions no cache, and the sentence reads as though one might exist.
- "The parser misread the dates." Task 6, turn 2. Connection test. The next sentence gives the same fact in detail with no connector.
- "861 of 900 is about 96 percent, up from 3." Task 6, turn 4. Specific test. The sentence compares a percentage with a row count, and it never answers "good?".

holdout-04.md: 4 distracting sentences.

- "The session read runs once per page load, so the 7 ms difference at p95 applies to every page load." Task 3. Given-fact test. The staging gap is stated as the production effect without "in staging".
- "It was deprecated in version 2.1, so remove it from any command that still passes it." Task 5. Connection test. The deprecation in 2.1 is not the reason to edit commands. The removal in 2.4 is the reason, so "so" names the wrong cause.
- "This one is in different code from the other two, which were in the reports service and were both fixed on Tuesday." Task 6, turn 3. Specific test. "different code" hides the parser, which the writer knew about and could have named.
- "I wouldn't." Task 6, turn 5. Whole-sentence test. The main verb is dropped, and the reader has to supply "auto-accept them".

holdout-05.md: 5 distracting sentences.

- "Add a second Redis node and shard sessions across both." Task 3. Body restates the heading. It repeats "Shard sessions across two Redis nodes" as a command, and a command in an undecided design doc reads as a decision.
- "Move sessions to the existing Postgres cluster, which has 40 percent headroom." Task 3. Body restates the heading. It is the same fault as Option A, in a command form that reads as the chosen plan.
- "The parser read the dates in the wrong order." Task 6, turn 2. Connection test. The next sentence restates this one in detail with no connector.
- "Both were in the reports service, and both were fixed on Tuesday." Task 6, turn 3. Slogan, a mirrored pair. The two "both" clauses mirror each other, and "fixed" repeats the sentence before.
- "861 and 39 add up to all 900 rows, so every row either matched or was written to `review.csv`." Task 6, turn 4. No job. The user asked "good?", and the reply opens on arithmetic the user does not need.

holdout-06.md: 5 distracting sentences.

- "It reads exports from four banks, which are Chase, Monzo, Wise, and ING." Task 1. Padding and a category named before its members. The words "four banks, which are" do no work.
- "The session read runs once per page load, so every page load makes one session read that is 7 ms slower at p95." Task 3. Given-fact test. The staging gap is stated as the production effect without "in staging", and a page load does not make a read.
- "Fix direction is to have the database count the rows, so the query returns one number." Task 4. Invented term and missing article. "Fix direction" is not a phrase a reader can look up, and it is not a label from the review skill.
- "The parser read the export's day/month/year dates as month/day/year, so the dates did not line up with the ledger." Task 6, turn 2. Idiom. "line up" is a figure of speech for "did not match the ledger dates".
- "Of the three, only the parser's date order is still open." Task 6, turn 3. Literal test. A date order cannot be open. The bug is what is still open.

holdout-07.md: 7 distracting sentences.

- "Two follow-ups are agreed:" Task 2. Setup sentence. It is a count with a colon, and the reader waits for the bullets.
- "The session read runs once per page load, so the 7 ms difference at p95 applies to every page load." Task 3. Given-fact test. The staging gap is stated as the production effect without "in staging".
- "Fix direction: ask the database for the count, such as `db.users.count()` if `db` is a Prisma client." Task 4. Invented term and a fact not given. "Fix direction" is a coined label, and the task never names Prisma.
- "Ledgerline read the dates in the wrong order." Task 6, turn 2. Connection test. The next sentence restates it with no connector, and it calls the reader "Ledgerline" where the next sentence says "the parser".
- "They were in the reports service, and both were fixed on Tuesday." Task 6, turn 3. No job. The sentence before already said the two bugs are fixed, and this one says "fixed" again.
- "This one is the parser reading day/month/year dates as month/day/year, and `--date-format dmy` handles it." Task 6, turn 3. Actor test. "handles" is vague, and it also repeats turn 2 word for word.
- "Check the 12 first." Task 6, turn 5. Slogan, a clipped run. It is followed by "The other 27 are within $1 of the ledger." with no connector between the two short sentences.

holdout-08.md: 2 distracting sentences.

- "Count the rows in the database with a count query, such as `db.users.count()` if `db` is a Prisma client." Task 4. Given-fact test. The task never names Prisma, and "Count ... with a count query" says "count" twice.
- "The parser read your export's dates as month/day/year, but the export writes them as day/month/year, so the dates did not line up with the ledger." Task 6, turn 2. Idiom. "did not line up" is a figure of speech for "did not match".

holdout-09.md: 4 distracting sentences.

- "For each bank row, it searches for a ledger entry with the same amount and a date within 2 days." Task 1. Given-fact test. The task gives the match rule and says nothing about a per-row search.
- "The session read runs once per page load, so that 7 ms difference at p95 applies to every page load." Task 3. Given-fact test. The staging gap is stated as the production effect without "in staging".
- "The parser read this export's dates wrong." Task 6, turn 2. Connection test. The next sentence restates it in detail with no connector.
- "This one needs `--date-format dmy` on the Ledgerline run." Task 6, turn 3. Actor test. A bug cannot need a flag. The user needs to pass it.

holdout-10.md: 4 distracting sentences.

- "When that version is installed, run `brew install ledgerline`." Task 1. Given-fact test. The task never says Python has to be installed before the brew command, and "that version" points at a range, "3.11 or later".
- "The session read runs once per page load, so its latency adds to every page load under either option." Task 3. No job. The clause after "so" restates "once per page load" as "every page load".
- "If `db.users` has a `count()` method, as Prisma clients do, call it so the database returns one number." Task 4. Given-fact test. The task never names Prisma, and "as Prisma clients do" states library behavior nobody gave.
- "Nothing ran for this finding, so it depends on reading line 22 alone." Task 4. Actor test. "Nothing ran" hides who did not run the handler, and a finding does not depend on anything.

## Across files

1. Given-fact test: 12. Six sentences state the staging 7 ms gap as a production effect (01, 02, 04, 06, 07, 09). Three guess that `db` is a Prisma client (02, 08, 10). One invents a cache (03), one invents a per-row search (09), and one invents an install order (10).
2. Connection test: 7. Five are a short summary opener restated by the next sentence (02, 03, 05, 07, 09). One is a bare "No." (02), and one uses "so" for the wrong cause (04).
3. Actor test: 5 (02 twice, 07, 09, 10).
4. No job, where a sentence restates an earlier one: 4 (03, 05, 07, 10).
5. Setup sentence that names a count before the items: 3 (01, 02, 07).
6. Literal test: 2 (03, 06).
7. Idiom: 2, both "line up" (06, 08).
8. Invented term: 2, both "Fix direction" (06, 07).
9. Padding with a category named before its members: 2, both "four banks, which are" (02, 06).
10. Specific test: 2 (03, 04).
11. Slogan, as a mirrored pair or a clipped run: 2 (05, 07).
12. Body restates the heading: 2 (05).
13. Whole-sentence test: 1 (04).
14. Human-moment sentence: 1 (02).
15. Claim of fixed about something that did not change: 1 (01).
16. Consecutive replies ending on the same move: 1 (01).

## Passed

Task 1

- "Rows that Ledgerline cannot match go to `review.csv`, where a person checks them." (holdout-07) Borderline. "go to" is the task's own wording, and "where a person checks them" states the purpose the task gave.
- "The parser must not make network calls, because CI fails any parser that imports `requests` or `httpx`." (holdout-05) Borderline. The "because" clause states the failure the prohibition prevents, which the rules ask for.
- "CI checks this rule and fails any parser that imports `requests` or `httpx`." (holdout-08) Borderline. "this rule" names the sentence before, and the rest of the sentence says what CI checks.
- "It writes each row it cannot match to `review.csv`, so a person can check that row." (holdout-03) Plain pass. Both clauses are given facts, and "so" names the purpose.
- "Each bank format is a parser in `parsers/<bank>.py`, so you add a bank by writing a parser file there." (holdout-01) Plain pass. The fact appears in the section for contributors, who need it.

Task 2

- "The TLS certificate on the payments proxy expired at 14:02 UTC on 9 September, and 38 percent of checkout requests returned errors until 14:47." (holdout-08) Borderline. "and" leaves the cause unstated, but the times put the expiry first.
- "Send payment alerts to the on-call pager." (holdout-07) Borderline. The two follow-up bullets are both commands, but they list agreed actions and do not mirror each other word for word.
- "For 45 minutes on 9 September, from 14:02 to 14:47 UTC, 38 percent of checkout requests returned errors." (holdout-03) Borderline. The 45 minutes is arithmetic on the given times.
- "From 14:02 to 14:47 UTC on 9 September, 38 percent of checkout requests returned errors because the TLS certificate on the payments proxy expired." (holdout-06) Plain pass. The sentence states the result and the cause in one sentence.
- "At 14:31 an engineer saw customer reports, and the same engineer renewed the certificate at 14:45." (holdout-05) Plain pass. The sentence names the actor and both times.

Task 3

- "The session read runs once per page load, so every page load would include one read that was 7 ms slower at p95 in staging." (holdout-08) Borderline. It keeps "in staging", so the number stays a staging measurement.
- "Because the session read runs once per page load, every page load would wait on the slower read." (holdout-05) Borderline. It moves no staging number into production, and a request does wait on a read.
- "No option has been chosen yet." (holdout-04) Borderline. The task gave this fact, and it tells the reader the section recommends nothing.
- "Its memory use grows about 3 percentage points a week, so at that rate the node is full in roughly 10 weeks." (holdout-01) Borderline. The 10 weeks is arithmetic on given numbers, and "at that rate" and "roughly" keep the qualifier.
- "Session reads stay on Redis, where they took 2 ms at p95 in staging." (holdout-02) Borderline. The staging number came from a single node, but the sentence does not claim sharded reads take 2 ms.

Task 4

- "**Guard.** Line 22 passes no filter or limit to `findMany()`, and nothing else on that line reduces the rows it returns." (holdout-01) Borderline. Naming a line as the subject is ordinary code-review usage, and the text after the label is a sentence.
- "The time and memory for each dashboard load therefore grow with the `users` table." (holdout-03) Borderline. The claim follows from fetching every row, and it states no measured number.
- "**Consequence.** Every load of the admin dashboard fetches all 1.2 million rows of the `users` table into the handler and builds an array of 1.2 million objects to read its `.length` (admin/stats.ts:22)." (holdout-10) Borderline. The array is visible from `.length` on the result, and "objects" is a close inference.
- "A count query, such as `db.users.count()` if the client provides it, returns the number without fetching the rows." (holdout-05) Borderline. The "if" clause names the unknown client and does not guess a library.
- "**Fires when.** The dashboard handler runs this line on every load, and the `users` table has 1.2 million rows." (holdout-04) Borderline. The text after the label is a sentence, though its second clause repeats the consequence.

Task 5

- "Users in time zones east of UTC saw report dates one day early." (holdout-01) Borderline. The past tense under the `Fixed` heading marks the bug as the old behavior.
- "Reports no longer show dates one day early for users in time zones east of UTC." (holdout-04) Borderline. "no longer" describes a behavior the users did see, so the denial answers a real belief.
- "Fixed report dates that showed one day early for users in time zones east of UTC." (holdout-07) Borderline. A changelog bullet may open on its verb, and it adds the dates and time zones the heading does not state.
- "Removed the `--legacy-match` flag, which version 2.1 deprecated." (holdout-06) Plain pass. The bullet opens on its verb and contains both given facts.
- "Users in time zones east of UTC saw report dates one day early, and 2.4 fixes those dates." (holdout-09) Plain pass. The task lists this item as fixed.

Task 6

- "`--date-format dmy` reads this export's dates correctly, and the other two date bugs were in the reports service, where both were fixed on Tuesday." (holdout-10) Borderline. "and" joins two separate points, but the fix comes first after the user's frustration.
- "The other 27 differ from the ledger by $1 or less." (holdout-06) Borderline. The number is arithmetic on 12 of 39, though some of the 27 may not differ in amount at all.
- "Nobody has looked at the 39 rows in `review.csv` yet, so this run is not verified." (holdout-08) Borderline. "not verified" names the unchecked rows as the reason.
- "Add `--date-format dmy` so the parser reads them correctly." (holdout-04) Borderline. "Add" leaves "to the command" for the reader to supply.
- "Two of the three are already fixed." (holdout-05) Borderline. It is a given fact, and it answers the user's count directly.

## Sentence types

1. A given fact restated as a plain statement, often with a "which" or "that" clause. About 41 percent. Not grating.
   - "Option B moves sessions to the existing Postgres cluster, which has 40 percent headroom." (holdout-01)
   - "An alert fired at 14:09 and went to a Slack channel that was archived in July." (holdout-02)
   - "Ledgerline needs Python 3.11 or later." (holdout-03)
2. A fact followed by a "so" or "because" clause that states a consequence. About 20 percent. Not grating when both halves are given. It is grating when the consequence stretches a fact, as in the staging 7 ms sentences.
   - "Nobody has run it with that flag yet, so I don't know how many rows it will match." (holdout-03)
   - "Nobody has looked at those 39 rows yet, so I can't call the run good until someone checks them." (holdout-04)
   - "The `findMany()` call at line 22 passes no arguments, so nothing in the query limits the rows it returns." (holdout-06)
3. An instruction for the next step. About 10 percent. Not grating, except in a design doc where no decision has been made.
   - "Install it with `brew install ledgerline`." (holdout-01)
   - "Run it again with `--date-format dmy`, which reads that order correctly." (holdout-02)
   - "Count the rows in the database, for example with `db.users.count()` if this client provides it." (holdout-03)
4. A changelog or follow-up bullet. About 8 percent. Not grating.
   - "Renew the certificate on the payments proxy automatically." (holdout-01)
   - "Removed the `--legacy-match` flag, which was deprecated in version 2.1." (holdout-07)
   - "Version 2.4 removes the `--legacy-match` flag, which was deprecated in version 2.1." (holdout-08)
5. A statement of what was not run or checked. About 7 percent. Not grating, except when the actor is hidden.
   - "I did not run the handler, so this finding comes from reading line 22." (holdout-01)
   - "This finding comes from reading the diff." (holdout-02)
   - "Nothing ran for this finding, so it depends on reading line 22 alone." (holdout-10) This one is grating.
6. A short summary opener that the next sentence restates in detail. About 4 percent. Grating.
   - "The parser misread the dates." (holdout-03)
   - "The parser read the dates in the wrong order." (holdout-05)
   - "Ledgerline read the dates in the wrong order." (holdout-07)
7. A sentence built on arithmetic from given numbers. About 4 percent. Grating when it has no job or mixes units, and not grating otherwise.
   - "861 of 900 is about 96 percent, up from 3." (holdout-03) Grating.
   - "861 and 39 add up to all 900 rows, so every row either matched or was written to `review.csv`." (holdout-05) Grating.
   - "At that rate, the node reaches 100 percent in about 10 weeks." (holdout-06) Not grating.
8. A setup sentence that names a count or category before the items. About 2 percent. Grating.
   - "Two follow-ups are agreed." (holdout-01)
   - "It reads exports from four banks, which are Chase, Monzo, Wise, and ING." (holdout-02)
   - "Two follow-ups are agreed:" (holdout-07)
9. A guess about the code or library stated as fact or near-fact. About 2 percent. Grating.
   - "**Fix:** If `db` is a Prisma client, `db.users.count()` returns the number from the database without fetching the rows." (holdout-02)
   - "I read the diff and did not run the handler, so a cache elsewhere in the handler is unchecked." (holdout-03)
   - "If `db.users` has a `count()` method, as Prisma clients do, call it so the database returns one number." (holdout-10)
10. A clipped verdict or command of one to four words. About 1 percent. Grating.
    - "No." (holdout-02)
    - "I wouldn't." (holdout-04)
    - "Check the 12 first." (holdout-07)
11. A reaction to the user's mood. Under 1 percent. Grating. Only one example exists across the ten files.
    - "Three in one week is a lot." (holdout-02)
