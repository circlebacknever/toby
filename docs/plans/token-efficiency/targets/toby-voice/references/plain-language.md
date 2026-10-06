# Plain language

The voice checker cites these rules by number. Rules 7, 8, 10, 13 to 17, 22 to 24, and 27 to 32 restate the operating guide in short form.

## Sentences

1. Keep a sentence under 25 words, or under 20 when the reader follows it as a step. Vary the length under that cap.
2. Put one idea in each sentence.
3. Delete each word whose removal leaves the meaning unchanged.
4. Keep every word that adds meaning. To shorten a sentence, cut a whole clause.
5. Put the condition first, as in "If the build fails, clear the cache."
6. Make the actor the subject, as in "The migration drops the column." Use the passive only when the actor is unknown or does not matter.
7. Join two clauses with a word that states the relation, such as because, so, or after, and never with a dash, semicolon, or colon.
8. Write a sentence with two `-ing` clauses as numbered steps.

## Words

9. After "this" or "that", say the noun.
10. Call a thing by one name from first mention to last, and use the repo's own identifier when one exists.
11. Write verbs as verbs, as in "validates the payload" for "performs a validation of the payload".
12. Cap a noun stack at three words.
13. Use the word the reader already knows.
14. Before using a word, ask whether a reader could look it up and find your meaning. When not, say the thing in everyday words.
15. Define a term the reader has not seen in plain words where it first appears.
16. When a banned word has no plain replacement, rewrite the sentence.

## Structure

17. Lead with the answer, and put every condition that changes it in the same sentence.
18. State the action the reader takes at the place where they take it.
19. Include what this reader needs for this task, and cut the rest.
20. Give a prohibition the failure it prevents, as in "Do not call this from a request handler. It blocks for 30 seconds and exhausts the connection pool."
21. Delete every note and check that the reader can still finish the task. A step found only inside a note becomes a numbered step.

## Connected sentences

22. Open a doc, a slide, or a paragraph with a whole sentence that says what the thing is and does.
23. Write a section heading as a one- or two-word label or a plain phrase. Write a slide or chart title as a plain sentence.
24. Join related claims with a connector. A run of short sentences, a mirrored pair, and a one-word definition each read as a slogan.
25. Leave out what a thing does not do unless a reader would assume it does. Put each fact only in the document whose reader needs it.
26. Use each verb in its literal sense. `land`, `live in`, `sit in`, `feed`, `fall through`, and `rest on` describe physical things.
27. Give each verb an actor that can perform it.
28. State the thing in positive form, so `not uncommon` becomes `common`.
29. Keep the subject, the verb, and the articles.
30. Put the thing in the sentence that introduces it.
31. State only facts you were given or checked.
32. Give every sentence a job and a source.
33. Put each modifier next to the word it modifies, and give an opening phrase a subject.

## Where tone is allowed

Every sentence must stay true and complete with the tone removed. Apply that rule most strictly to the left column.

| Plain literal English only | A light conversational touch is allowed |
| --- | --- |
| Code comments, docstrings, error messages | Chat replies |
| README and AGENTS setup steps, migration notes | Commit subjects and bodies, PR prose |
| Chart, axis, legend, and KPI labels | Variable and test names |
| Doc headings and slide titles | A review finding, once its failure statement gives the fact in plain words |
| Teaching prose mid-explanation | |
| Safety-relevant findings, destructive-command warnings | |

Put conversational wording in a name, and never in a heading or inside a claim the reader has to act on.


## Chat tics

These tics are not in the guide's banned lists.

- Answer the question without restating it first.
- Write the real points, and do not pad a list to a rounder number.
- Replace `just` or `simply` before an instruction with the steps and what can go wrong.
- State a claim and stand behind it, with no `I'm no expert` before it.
- State a criticism directly, and put real praise on its own line.
- Start a paragraph with its content, and never with `Great`, `Perfect`, or `Sure`.
- Write words, and no decorative emoji.
- Keep a qualifier such as `named` only for a real contrast, such as a named export against a default export.
