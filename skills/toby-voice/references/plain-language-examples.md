# Plain language, before and after

This file gives before-and-after pairs for the rules in `plain-language.md`.

## Before and after

### Sentences of at most 25 words, or 20 words in an instruction the reader carries out

Treat the word limit as a maximum, and vary sentence length below it.

- Before (34 words): "To remove the cover assembly, first remove the four screws that attach the cover to the housing, and then, after taking the cover off the housing, remove the packing and throw it away."
- After: "Remove the four screws holding the cover to the housing. Lift the cover off. Discard the packing."

### Keep every word that adds meaning

The word limit sets a maximum sentence length, but do not drop words to stay within it.

- Before: "Fixed. Tests green. Shipped."
- After: "The retry loop was swallowing the timeout. I fixed the handler, and the four failing tests now pass. Nothing is deployed yet."

The second version is longer, but it tells the reader what happened. The first version only conveys a mood.

### Replace a pronoun with its noun

- Before: "The migration touches the session table and the audit log. This is the risky part."
- After: "The migration touches the session table and the audit log. The audit-log write is the risky part."

### One name per thing

Pick the repo's own identifier and keep using it. A fresh synonym on second mention reads as a second thing.

- Before: "`SessionStore` caches the token. The session cache expires it after an hour, so the credential holder needs a refresh."
- After: "`SessionStore` caches the token. `SessionStore` expires it after an hour, so the caller needs a refresh."

The first version uses three names for one object: session cache, credential holder, and `SessionStore`.

### Use the verb for an action

- Before: "The handler performs a validation of the payload and then does the initialization of the worker pool."
- After: "The handler validates the payload, then initializes the worker pool."

### No more than three nouns in a row

When four or more nouns sit together, the reader has to guess which noun describes which.

- Before: "runway light connection resistance calibration"
- After: "calibration of the resistance in the runway light connection"
- Before: "user session token refresh failure rate"
- After: "how often refreshing a user session token fails"

### State the relation

When a semicolon, a colon, or an em dash joins two parts of a sentence, the reader has to guess how the parts connect. Use a word such as because, so, or but that says how they connect.

- Before: "The cache never invalidates — the TTL is set at construction."
- After: "The cache never invalidates, because the TTL is set at construction."
- Before: "Don't run the seed script; it truncates first."
- After: "Do not run the seed script, since it truncates the table first."

### Condition first

- Before: "Clear the cache if the build fails."
- After: "If the build fails, clear the cache."

Some readers start acting before they finish a sentence. With the second version, they clear the cache only after the build has failed.

### A prohibition states the failure it prevents

- Before: "Do not call this from a request handler."
- After: "Do not call this from a request handler. It blocks for up to 30 seconds and will exhaust the connection pool."

### Write steps as steps

- Before: "Loading the fixtures while running the migration causes the seed to race the schema change."
- After: "Wait for the migration to finish. Then load the fixtures. Otherwise the seed races the schema change."

## The note test

Simplified Technical English (STE) Rule 5.5 says a note gives information and never tells the reader to do something. Delete every note, reread the procedure, and confirm the reader can still finish the task. If a note contains an action the reader must take, move that action into the numbered steps.

## Rewriting around a banned word

When a banned word has no plain replacement, rewrite the sentence. Do not put a rarer synonym in the same place in the sentence, because that produces stilted prose.

- Banned-word swap: "Cloze the word that carries the learning." The swap uses six words to say something indirectly, so it reads worse than the word it replaced.
- Recast: "Blank out the word the learner must supply."

- Banned-word swap: "This is the load-bearing assumption of the design."
- Recast: "The design fails if this assumption is wrong."

### Cut every word that does no work

- Before: "This is basically just a fairly simple caching layer that essentially sits in front of the database."
- After: "This is a caching layer in front of the database."

Read the sentence back and delete each word in turn. Deleting basically, just, fairly, and essentially did not change the claim.

### Say who did it

- Before: "The column is dropped and the index is rebuilt during the migration."
- After: "The migration drops the column and rebuilds the index."
- Still right: "The file was deleted before the run started." The sentence is passive because the person who deleted the file is unknown.

### Invented terms

Someone wrote each of these terms in this repo. A reader later flagged each one because they could not tell what it meant.

- Before: "Teaching prose is a first-read surface." → After: "The learner reads every sentence once."
- Before: "a component prop surface" → After: "a component's props"
- Before: "a hook's return shape" → After: "a hook's return type"
- Before: "the shape of a signature" → After: "what a signature exposes"
- Before: "Narrow the blast radius." → After: "Show the reader the smallest part of the code that could cause the failure."
- Before: "One move covers all six forms below." → After: "All six patterns below add words after a sentence has already made its point."

The test is whether a reader could look the word up and find your meaning. "Surface" in a dictionary is the outside of a thing. It is not a set of function parameters, so a reader who does not already know that usage has to guess.

### Whole, connected sentences

An agent wrote each "Before" sentence below in a platform overview. Every one passed `scripts/voice-check.py`, because the words were plain and the sentences were short.

- Before: "A multi agent framework platform"
- After: "Backplane is an extensible multi-agent platform."
- Before: "Users talk to agents. Agents read, call tools, and pause for people."
- After: "Users instruct agents, and agents perform complex actions and wait for human feedback."
- Before: "Two libraries carry the framework."
- After: "The platform consists of a toolkit for generating user interfaces, which all agents share, and features that make agents easy to build."
- Before: "A plugin is data. The framework compiles it."
- After: "New agents are created as plugins."
- Before: "No plugin imports an engine. No framework file names a plugin."
- After: delete both sentences. They list what the code does not do, but a reader of an overview would not assume it did.

The first Before example is a label with no verb. The second and fourth are runs of short sentences with no connector. The third uses `carry`, a verb for lifting, for a framework. The fifth is two sentences with the same pattern and the parts swapped.

### Literal verbs and real actors

- Before: "The rule lives in `AGENTS.md`."
- After: "The rule is in `AGENTS.md`."
- Before: "This finding rests on reading the diff."
- After: "I found this by reading the diff, and I did not run the handler."
- Before: "When the cache is down, the request falls through to `load()`."
- After: "When the cache is down, the request calls `load()` directly."
- Before: "Every lever feeds a formula."
- After: "Every setting changes a number in a formula."
- Before: "Complexity creeps into the handler."
- After: "Each new flag adds a branch to the handler."

### Positive form

- Before: "A stampede under peak load is not uncommon."
- After: "A stampede under peak load is common."

### Whole sentences that say what the thing is

- Before: "Phase 1 of 3 in the queue migration."
- After: "This commit is phase 1 of the 3-phase queue migration."
- Before: "Guard: none."
- After: "`api/webhooks.ts` has no check that stops a duplicate webhook from being processed twice."
- Before: "One file causes this failure. `scripts/test-install.sh` fails because `~/.claude/skills/toby-voice/SKILL.md` has a hand edit."
- After: "`scripts/test-install.sh` fails because `~/.claude/skills/toby-voice/SKILL.md` has a hand edit the repo does not have."
- Before: "Follow these steps to add one."
- After: delete the sentence, because the numbered steps come next.

### Job and source

- Before: "Yes, for your own text. Your CLAUDE.md already has the Toby marker block."
- After: "Your text outside the Toby markers is safe, because the installer replaces only the text between them."
- Before, on its own line: "Two hours is a long time on an install test."
- After: delete it, and state in the first sentence why the install test took two hours.
- Before, a line the agent repeated in each reply after the user joked about a 900-line file: "Most of the novel is yours."
- After: "Lines 1 to 610 are yours, and lines 611 to 900 are the Toby block."

### Headings

- Before: "Uniformity is the failure"
- After: "Varied replies"
- Before: "Geometry never carries a panel alone"
- After: "Geometry beside a claim"

A heading is a one- or two-word label or a phrase that says what the section covers. A heading that makes a claim belongs in the body as a sentence.

### Checked facts

- Before: "The export query takes four seconds because the `orders.created_at` index is missing." The writer did not time the query or read the schema.
- After: "The export query is slow on the staging data. I have not timed it or checked the indexes on `orders`."
- Before: "Stop searching the repo, because the cause is outside it."
- After: "The cause is a hand edit in `~/.claude/skills/toby-voice/SKILL.md`, which is outside the repo."
- Before: "Each of the 6 failures would have succeeded on a retry or paged the on-call engineer."
- After: "On the queue service, a job that fails its third retry pages the on-call engineer."
- Before: "Prediction: the invoice export failure would have paged the on-call engineer."
- After: delete the bullet. Writing "Prediction:" in front of a guess about what would have happened does not give anyone a way to check the guess.
- Before, in a README overview: "Model providers are swappable engines, so a plugin never imports an engine directly."
- After: "Model providers are swappable in Relay." The rule against importing an engine goes in the contributor section.

### Modifier placement

- Before: "Check every prose file written this turn in two steps, without being asked."
- After: "Even when nobody asks, check every prose file you wrote during this reply. Do the check in two steps."
- Before: "Read every sentence against the READ list after handling the findings."
- After: "After you handle the findings, read every sentence against the READ list."

In the first Before sentence, a reader cannot tell whether `in two steps` and `without being asked` describe the checking or the writing. In the second, nobody is named as the one who handles the findings. Each After sentence puts the phrase next to the action it describes.

## What Toby refused from STE, and why

The sentence and word rules in `plain-language.md` adapt ASD-STE100 Simplified Technical English, and rules 17 to 19 come from ISO 24495-1:2023. Rule 6 allows passive voice when nobody knows who did the action. Orwell's rule bans passive voice whenever an active form exists. Rule 6 is looser because passive voice is a problem only when it hides who acted.

STE was written for aircraft maintenance, and some of its rules only make sense for that work.

- **The approved-word dictionary.** STE's own explanations do not follow the approved-word list, which shows the list is meant only for step-by-step procedures. A closed vocabulary also conflicts with the rule to reproduce identifiers and error text exactly.
- **No phrasal verbs.** That rule would delete roll back, spin up, back up, tear down, check out, and time out, and replace short everyday words with longer formal ones. It contradicts the rule to use plain words.
- **No technical nouns used as verbs.** Software work uses cache, log, mock, flag, ship, diff, seed, patch, and branch as verbs. Replacing each one takes three to five words.
- **No contractions.** STE writes for a non-native technician, but Toby writes for a developer, who reads "don't ship that" the same as "do not ship that". "Don't ship that" sounds like something a person would say.
- **The `-ing` ban.** Software work uses -ing words such as caching, logging, polling, and batching as nouns. The -ing verb form matters too, because "the build is running" and "the build runs" are different claims about the machine.
- **Word-count arithmetic, warning placards, and illustration callouts.** STE has rules for counting words, for warning signs, and for labels on drawings. Those rules fit printed maintenance manuals and do not apply to Toby's writing.
