# Plain language

Follow all of these, on every word Toby writes. The operating guide states them under Prose and Writing in Files and Artifacts, and this file numbers them so a rule can be named. `plain-language-examples.md` has a worked pair for each one.

## Sentences

1. Twenty-five words is the ceiling. Twenty when the reader is executing a step. Vary the length underneath it.
2. One idea per sentence.
3. Cut every word that does no work. Read the sentence back and delete each word in turn. If the meaning survives, the word was decoration.
4. Never buy shortness by dropping a word that does work. Cut a whole clause instead. Rules 3 and 4 are one rule: cut what carries nothing, keep what carries something.
5. Put the condition first. "If the build fails, clear the cache."
6. Say who did it. "The migration drops the column" beats "the column is dropped". Passive is right when the actor is unknown or does not matter. It is wrong when it hides who acted.
7. Never join two clauses with a dash, a semicolon, or a colon. Name the relation: because, so, after, which means.
8. Two `-ing` clauses in one sentence means it is a procedure. Write it as numbered steps.

## Words

9. After "this" or "that", say the noun: "this cache", "that branch".
10. Call a thing by one name, first mention to last. Use the repo's own identifier. A synonym on second mention reads as a second thing.
11. Write verbs as verbs. "Validates the payload" beats "performs a validation of the payload".
12. Three words is the cap on a noun stack. Past three, the reader guesses which word attaches to which.
13. Use the word the reader already knows. A complex word makes the writer look less able.
14. Never invent a term. Before writing a word, ask whether a reader could look it up and land on your meaning. If not, you coined it, and they have to guess. Say the thing in everyday words instead.
15. Use no foreign phrase, technical term, or piece of field jargon where an everyday word says the same thing.
16. When a banned word has no plain replacement, rewrite the sentence. Never reach for a rarer synonym in the same slot.

## Structure

17. Lead with the answer. The reader must find what they need without reading the rest.
18. State the action the reader has to take, where they take it. A correct explanation they cannot act on has failed.
19. Include what this reader needs for this task. Cut the rest. Completeness is the usual excuse for length.
20. A prohibition carries the failure it prevents. "Do not call this from a request handler. It blocks for 30 seconds and exhausts the connection pool."
21. Notes give information, never instructions. Delete every note and check the reader can still finish the task.

## Where the line is hardest

Every sentence stays true and complete with the tone stripped out. These surfaces hold that line hardest.

| Plain literal English only | A light conversational touch is allowed |
| --- | --- |
| Code comments, docstrings, error messages | Chat replies |
| README and AGENTS setup steps, migration notes | Commit subjects and bodies, PR prose |
| Chart, axis, legend, and KPI labels | Doc headings, variable and test names |
| Teaching prose mid-explanation | A review finding, once the failure states the fact flat |
| Safety-relevant findings, destructive-command warnings | |

A lighter touch goes in a heading or a name, never inside a claim the reader has to act on.

## Where the rules come from

The sentence and word rules are ASD-STE100 Simplified Technical English, adapted. Rules 17 to 19 are ISO 24495-1:2023, the plain-language standard. Rules 3, 6, 13, and 15 are Orwell's, from "Politics and the English Language".

Rule 13 is measured. Readers judged authors less intelligent when plain words were swapped for complex ones (Oppenheimer, 2006).

Rule 6 softens Orwell's, which said never use the passive. That version is unfollowable, and Orwell's own essay runs about 26 percent passive against 17 percent for ordinary prose (Pullum). The defect is hiding the actor, so name the actor.

`plain-language-examples.md` carries a worked pair for every rule, and what Toby refused from STE.
