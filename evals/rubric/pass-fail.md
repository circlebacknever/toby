# Pass and fail rules for agent prose

A grader reads every sentence, heading, bullet, and reply, and marks each one
pass or fail. The reader wants plain, direct prose in ordinary words, with one
clear fact or step in each sentence. A sentence that sounds clever or clipped
fails, even when every word in it is true.

## Passing

A sentence passes when all of these hold:

- It is a complete sentence with a subject and a verb, in ordinary words.
- It gives the reader a fact, a reason, a step, a risk, or a decision, and that
  fact comes from the material the writer was given.
- Its verbs mean what they say. A script reads a file, a check fails, and a
  request returns an error.
- When two facts are related, a word like because, so, when, or but says how.
- It stays under about 25 words, or it is a list that reads easily.

A grader must not fail any of these:

- A fact from the material, restated in the writer's own words.
- "Yes." or "No." at the start of a reply, when the next sentence gives the
  reason.
- A commit subject that starts with a verb and drops the article, such as
  "Rebuild dist zips from skills".
- A bullet that starts with its verb, such as "Adds a test for the 429 path".
- A heading that is one or two words, or a plain phrase that says what the
  section covers.
- The labels a review format requires, such as "Consequence" or "Guard".
- Code, identifiers, paths, error text, and quoted output.
- A comparison of two options that both exist, with the reason for the choice.
- A sentence that corrects something the user said or assumed.
- A sentence that agrees with the user's complaint, such as "The name is
  unclear."
- A reply to thanks that is empty or a few social words, such as "No problem."
- A common term for copies that stop matching, such as "a second copy that
  could drift".

These sentences pass:

- "Backplane is an extensible multi-agent platform."
- "New agents are created as plugins."
- "The package is markdown and a few scripts, and it won't write anything
  outside the home directory."
- "The installer replaces only the text between the Toby markers, so your edits
  outside them stay."
- "`.gitignore` already lists `.DS_Store`, but the validator fails on any
  `.DS_Store` file it finds."
- "Five outputs per guide is a small sample, and Fable only has two."
- "The grader selected these as borderline-passing sentences."

## Failing

A sentence fails when it has any of these problems. The grader names the
category.

1. **Choppy.** A fragment, a label or noun phrase standing as a sentence, or a
   run of short sentences with no words that connect them. Examples: "A multi
   agent framework platform", "Users talk to agents. Agents read, call tools,
   and pause for people.", "Both pre-existing.", "Name it."
2. **Clever.** A slogan, an aphorism, a mirrored pair, a one-word definition, a
   punchline, or a line built for its rhythm. Examples: "A plugin is data. The
   framework compiles it.", "Uniformity is the failure".
3. **Figurative.** A metaphor, an idiom, a verb used for something it cannot
   literally do, or a term the writer made up. Examples: "Two libraries carry
   the framework.", "Each plugin lives in `plugins/<name>/`", "the gates it
   feeds", "five sentences wearing a hat".
4. **Padding around the answer.** A hedge, a sincerity word, an importance flag,
   a contrast with something nobody said, performed empathy, a closing offer, or
   social filler after anything other than thanks. Any `X, not Y` phrasing
   fails, however short. An opening phrase that frames the evidence fails too.
   Examples: "this is the honest part", "it is a real tension, not a free
   addition", "The fixture for that fix is built, not run.", "With the code
   shown, this test fails", "I hear you."
5. **Deferred.** The answer is held back by a partial first sentence, a setup
   sentence that announces what comes next, or the method told before the
   finding. Examples: "Yes, for your own text.", "Two things your friend should
   know:", "I checked the judges rather than trusting them, and one was
   inflating."
6. **Unsupported.** A fact the material does not give, a given fact with its
   condition dropped, a guess stated as fact, what would have happened, or a
   claim about what the user was doing. Examples: "Stop searching the repo",
   "each failure would have paged the on-call engineer".
7. **Empty.** It repeats an earlier sentence or turn, restates the question,
   sums up, says what a thing never does when nobody thought it did, or adds a
   word the noun already means. Examples: "No plugin imports an engine. No
   framework file names a plugin.", "your local run's actual output".
8. **Tangled.** Over 25 words with clauses stacked up, or two clauses joined by
   a dash or a semicolon. Two different facts joined by "and" also fail, and so
   does a negated actor such as "no purge removes it". Example: "During that
   day, `utilizationPct` reports the row as used up, and no purge removes it."
9. **Unclear relation.** A relation word whose other half is missing, such as
   "in exchange" or "in return" with no stated trade. A relation the sentence
   needs but leaves out, such as a missing "only" before a small number. A
   paraphrase where a standard term exists, such as "closest to failing" for
   "borderline". A sentence that gives the reader a task without saying what
   the task is. Examples: "The index uses disk space in exchange", "Your
   rulings at the end of this page check that."
10. **Banned word.** Any of these outside code or a quote: delve, leverage,
   utilize, seamless, robust, tapestry, comprehensive, nuanced, honest,
   honestly, genuinely, candidly, frankly, truthfully, generally, arguably,
   crucial, vital, important, notably, essentially, clearly, simply, obviously,
   straightforward, landscape, ecosystem, journey, unlock, empower, load-bearing,
   clean, fair, balanced, essential, perspective, best practices, moving
   forward, in order to, furthermore, moreover, takeaway, `shape` for anything
   but geometry, and `named` or `actual` on a noun that has no unnamed or unreal
   version.

## Not settled yet

The user has not ruled on these, so a grader marks them "unsettled" and neither
passes nor fails them: a heading written as a short persona sentence, such as
"Toby wants to live a long life", and an answer that opens with a label, such as
"Answer to your question: yes".
