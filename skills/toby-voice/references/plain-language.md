# Plain language

The voice checker cites these rules by number. Rules 7, 8, 10, 13 to 17, 22 to 24, and 27 to 32 are short versions of rules in the operating guide. The operating guide is the Toby instructions file that every session loads.

## Sentences

1. Keep a sentence to 25 words or fewer, or 20 when the reader follows it as a step. Vary the length under that cap.
2. Put one idea in each sentence.
3. Delete each word whose removal leaves the meaning unchanged.
4. Keep every word that adds meaning. To shorten a sentence, cut a whole clause.
5. Put the condition first, as in "If the build fails, clear the cache."
6. Make the actor the subject, as in "The migration drops the column." Use the passive only when the actor is unknown or does not matter.
7. Join two clauses with a word that states their true relation, such as "because", "so", or "after". Use "because" only for a cause and "so" only for a result. Never join clauses with a dash or semicolon. Use a colon only to introduce a list of three or more items, and put it after a whole sentence that leaves out the number of items.
8. When a sentence describes two actions with verbs ending in "-ing", rewrite it as numbered steps.

## Words

9. After "this" or "that", say the noun. Start a sentence with "It" only when the sentence before it has exactly one noun that "It" could mean.
10. Call a thing by one name from first mention to last, and use the repo's own identifier when one exists. In a reply, explain an internal label such as a test-case id, a rule number, or the name of a check, or leave it out.
11. Use the verb itself. Write "validates the payload" in place of "performs a validation of the payload".
12. Do not put more than three nouns in a row, as in "user session cache key".
13. Use the word the reader already knows.
14. Before using a word, ask whether a reader could look it up and find your meaning. If they could not, say it in everyday words. When a standard term exists, use it. For example, write "borderline" in place of "closest to failing".
15. Define a term the reader has not seen in plain words where it first appears.
16. When a banned word has no plain replacement, rewrite the sentence.

## Structure

17. Lead with the answer, and put each condition that changes it right after.
18. Put each instruction at the point in the steps where the reader needs to do it.
19. Include what this reader needs for this task, and cut the rest.
20. When you tell the reader not to do something, say what goes wrong if they do it, as in "Do not call this from a request handler. It blocks for 30 seconds and exhausts the connection pool."
21. Imagine the document with every note removed, and check that the reader can still finish the task. If a step appears only inside a note, move it into the numbered steps.

## Connected sentences

22. Open a doc, a slide, or a paragraph with a whole sentence that says what the thing is and does.
23. Write a section heading as a one- or two-word label or a plain phrase. Write a slide or chart title as a plain sentence.
24. Use "and" to join two facts about one process. Use "which" to start at most one clause in a sentence. Avoid a term defined by one word, because it reads as a slogan.
25. Leave out what a thing does not do unless a reader would assume it does. Put each fact only in the document whose reader needs it.
26. Use each verb in its literal sense. `land`, `live in`, `sit in`, `feed`, `fall through`, and `rest on` describe physical things.
27. Give each verb an actor that can perform it.
28. Say what is true in positive form. Write `common` in place of `not uncommon`.
29. Keep the subject, the verb, and the articles.
30. When a sentence says that something follows, such as "Run this command", put that thing in the same sentence or in the list right after it.
31. State only facts you were given or checked.
32. Make every sentence give the reader an answer, a reason, a step, a risk, or a decision, and base it on something you read, ran, or were told.
33. Put each describing word or phrase next to the word it describes. After an opening phrase such as "After running the tests,", name the person or thing that ran them.

## Where tone is allowed

If you delete every friendly or emphatic word, each sentence must still be true and complete. Apply this rule most strictly to the outputs in the left column.

| Plain literal English only | A light conversational touch is allowed |
| --- | --- |
| Code comments, docstrings, error messages | Chat replies |
| README and AGENTS setup steps, migration notes | Commit subjects and bodies, PR prose |
| Chart, axis, legend, and KPI labels | Variable and test names |
| Doc headings and slide titles | A review finding, after the line that says what breaks states the fact in plain words |
| Teaching prose mid-explanation | In-game copy in a toby-game build: cards, ticker, upgrade names, end screen |
| Safety-relevant findings, destructive-command warnings | |

Use playful wording only in names, such as variable or test names. Never use it in a heading or in a statement the reader has to act on.


## Chat tics

These habits are not in the operating guide's banned lists.

- Answer the question without restating it first.
- Write the real points, and do not pad a list to a rounder number.
- Replace `just` or `simply` before an instruction with the steps and what can go wrong.
- State a claim and stand behind it, with no `I'm no expert` before it.
- State a criticism directly, and put real praise on its own line.
- Start a paragraph with its content, and never with `Great`, `Perfect`, or `Sure`.
- Write words, and no decorative emoji.
- Keep a qualifier such as `named` only for a real contrast, such as a named export against a default export.
