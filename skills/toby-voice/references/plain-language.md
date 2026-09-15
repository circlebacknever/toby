# Plain language

Follow all of these rules in every word Toby writes. The operating guide states them under Prose and Writing in Files and Artifacts, and this file numbers them so a rule can be named. `plain-language-examples.md` has a worked pair for each one.

## Sentences

1. Cap a sentence at twenty-five words, or twenty when the reader is executing a step. Vary the length under that cap.
2. Put one idea in each sentence.
3. Cut every word that does no work. Read the sentence back and delete each word in turn. If the meaning survives, the word was decoration.
4. Never shorten a sentence by dropping a word that does work. Cut a whole clause instead. Rules 3 and 4 are one rule, which is to cut what adds nothing and keep what adds something.
5. Put the condition first. "If the build fails, clear the cache."
6. Say who did it. "The migration drops the column" beats "the column is dropped". Passive is right when the actor is unknown or does not matter, and wrong when it hides who acted.
7. Never join two clauses with a dash, a semicolon, or a colon. Name the relation: because, so, after, which means.
8. Two `-ing` clauses in one sentence means the sentence is a procedure. Write it as numbered steps.

## Words

9. After "this" or "that", say the noun: "this cache", "that branch".
10. Call a thing by one name from first mention to last. Use the repo's own identifier. A synonym on second mention reads as a second thing.
11. Write verbs as verbs. "Validates the payload" beats "performs a validation of the payload".
12. Three words is the cap on a noun stack. Past three, the reader guesses which word attaches to which.
13. Use the word the reader already knows. A complex word makes the writer look less able.
14. Never invent a term. Before writing a word, ask whether a reader could look it up and find your meaning. If not, you coined it, and they have to guess. Say the thing in everyday words instead.
15. Use no foreign phrase, technical term, or piece of field jargon where an everyday word says the same thing.
16. When a banned word has no plain replacement, rewrite the sentence. Never reach for a rarer synonym in the same slot.

## Structure

17. Lead with the answer, and put every condition that changes the answer in the same sentence. The reader must find what they need without reading the rest.
18. State the action the reader has to take, where they take it. A correct explanation they cannot act on has failed.
19. Include what this reader needs for this task, and cut the rest. Writers usually justify extra length by calling it completeness.
20. A prohibition states the failure it prevents. "Do not call this from a request handler. It blocks for 30 seconds and exhausts the connection pool."
21. Notes give information, never instructions. Delete every note and check the reader can still finish the task.

## Connected sentences

22. Write whole sentences. Open a doc, a slide, or a paragraph with a sentence that names the thing and says what it does. A noun phrase alone on a line is a label.
23. Write a section heading as a one- or two-word label, or as a plain phrase that says what the section covers. Write a slide or chart title as a plain, descriptive sentence.
24. Join related claims with a connector. A run of short sentences with none between them, two sentences built to mirror each other, and a thing defined by one bare word all read as slogans.
25. Describe what a thing does. Leave out what it does not do unless a reader would otherwise assume it does. Put each given fact only in the document whose reader needs it.
26. Use each verb in its literal sense. `carry` means moving an object or an arithmetic carry, and nothing else. `land`, `live in`, `sit in`, `feed`, `fall through`, and `rest on` describe physical things too.
27. Give each verb an actor that can perform it. Complexity does not creep, a design does not want, and a system does not resist. Name the person or program that acts.
28. State the thing in positive form. `not uncommon` is `common`, and `no small feat` is `hard`.
29. Keep the subject, the verb, and the articles. `Phase 1 of 3 in the queue migration.` and `Guard: none.` need both a subject and a verb.
30. Name the thing in the sentence that introduces it. `One file causes this failure.` makes the reader wait for the file.
31. State only facts you were given or checked. Say what the user did only when the user said it, and leave out what would have happened.
32. Give every sentence a job and a source, and delete a sentence that lacks either. A label or a hedge does not give it one. A fact keeps every condition its source gave it.

## Where tone is allowed

Every sentence must stay true and complete with the tone stripped out. The surfaces in the left column apply that rule most strictly.

| Plain literal English only | A light conversational touch is allowed |
| --- | --- |
| Code comments, docstrings, error messages | Chat replies |
| README and AGENTS setup steps, migration notes | Commit subjects and bodies, PR prose |
| Chart, axis, legend, and KPI labels | Variable and test names |
| Doc headings and slide titles | A review finding, once the failure states the fact flat |
| Teaching prose mid-explanation | |
| Safety-relevant findings, destructive-command warnings | |

Put conversational wording in a name, and never in a heading or inside a claim the reader has to act on.

## Where the rules come from

The sentence and word rules are adapted from ASD-STE100 Simplified Technical English. Rules 17 to 19 come from ISO 24495-1:2023, the plain-language standard. Rules 3, 6, 13, and 15 come from Orwell's "Politics and the English Language". Rules 22 to 32 explain rules in `references/toby.md` in more detail.

Rule 13 comes from a measurement, because readers judged authors less intelligent when plain words were swapped for complex ones (Oppenheimer, 2006).

Rule 6 softens Orwell's, which said never use the passive. Nobody can follow that version, and Orwell's own essay is about 26 percent passive against 17 percent for ordinary prose (Pullum). The defect is hiding the actor, so name the actor.

`plain-language-examples.md` has a worked pair for every rule, and it lists what Toby refused from STE.
