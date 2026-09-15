# Plain language, before and after

This file gives worked pairs for every rule in `plain-language.md`. Load this file
when a rule is unclear or a rewrite is not working. The rules file is the one to follow.

## Before and after

### Sentence length limit of 25 words, or 20 when the reader follows the sentence as a step

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

### Verbs as verbs

- Before: "The handler performs a validation of the payload and then does the initialization of the worker pool."
- After: "The handler validates the payload, then initializes the worker pool."

### Three-word cap on noun stacks

Past three words, the reader has to guess which word modifies which.

- Before: "runway light connection resistance calibration"
- After: "calibration of the resistance in the runway light connection"
- Before: "user session token refresh failure rate"
- After: "how often refreshing a user session token fails"

### State the relation

A semicolon, a colon, or an em dash joining two clauses means the relation went unstated. Say which relation it is.

- Before: "The cache never invalidates — the TTL is set at construction."
- After: "The cache never invalidates, because the TTL is set at construction."
- Before: "Don't run the seed script; it truncates first."
- After: "Do not run the seed script, since it truncates the table first."

### Condition first

- Before: "Clear the cache if the build fails."
- After: "If the build fails, clear the cache."

A reader who acts on the first half of the sentence before finishing it does the right thing in the second version.

### A prohibition states the failure it prevents

- Before: "Do not call this from a request handler."
- After: "Do not call this from a request handler. It blocks for up to 30 seconds and will exhaust the connection pool."

### Two `-ing` clauses means a procedure

- Before: "Loading the fixtures while running the migration causes the seed to race the schema change."
- After: "Load the fixtures. Wait for the migration to finish. Otherwise the seed races the schema change."

## The note test

STE Rule 5.5 says that notes give information and do not give instructions. Delete every note, re-read the procedure, and confirm the reader can still finish the task. If a step appears only inside a note, that text is an instruction, so it is a step.

## Where tone is allowed

Every sentence in every kind of output must stay true and complete when the tone is removed. The rule applies more strictly to some kinds of output than to others.

| Plain literal English only | A light conversational touch is allowed |
| --- | --- |
| Code comments, docstrings, error messages | Chat replies |
| README and AGENTS setup steps, migration notes | Commit subjects and bodies, PR prose |
| Chart, axis, legend, and KPI labels | Variable and test names |
| Doc headings and slide titles | A review finding, once the failure scenario states the fact plainly |
| Teaching prose mid-explanation | |
| Safety-relevant findings, destructive-command warnings | |

Right-column text still has to read true and complete when the tone is removed. Put conversational wording in a name, and never in a heading or inside a claim the reader has to act on.

## Rewriting around a banned word

When a banned word has no plain replacement, rewrite the sentence. Do not put a rarer synonym in the same place in the sentence, because that produces stilted prose.

- Banned-word swap: "Cloze the word that carries the learning." The swap uses six words to say something indirectly, so it reads worse than the word it replaced.
- Recast: "Cloze the word the learner must produce."

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
- Before: "Narrow the blast radius." → After: "Point them at the smallest piece that could be wrong."
- Before: "One move covers all six forms below." → After: "All six below are the same habit."

The test is whether a reader could look the word up and find your meaning. "Surface" in a dictionary is the outside of a thing. It is not a set of function parameters, so a reader who does not already know that usage has to guess.

### Whole, connected sentences

An agent wrote each "Before" sentence below in a platform overview. Every one passed the checker, because the words were plain and the sentences were short.

- Before: "A multi agent framework platform"
- After: "Backplane is an extensible multi-agent platform."
- Before: "Users talk to agents. Agents read, call tools, and pause for people."
- After: "Users instruct agents, and agents perform complex actions and wait for human feedback."
- Before: "Two libraries carry the framework."
- After: "The platform consists of a shared generative UI toolkit and features that make it easy to build agents."
- Before: "A plugin is data. The framework compiles it."
- After: "New agents are created as plugins."
- Before: "No plugin imports an engine. No framework file names a plugin."
- After: delete both sentences. They list what the code does not do, but a reader of an overview would not assume it did.

The first before is a label with no verb. The second and fourth are runs of short sentences with no connector. The third uses `carry`, a verb for lifting, for a framework. The fifth is a mirrored pair.

### Literal verbs and real actors

- Before: "The rule lives in `AGENTS.md`."
- After: "The rule is in `AGENTS.md`."
- Before: "This finding rests on reading the diff."
- After: "I found this by reading the diff, and I did not run the handler."
- Before: "When the cache is down, the request falls through to `load()`."
- After: "When the cache is down, the request calls `load()` directly."
- Before: "Every lever feeds a formula."
- After: "Every lever changes a number in a formula."
- Before: "Complexity creeps into the handler."
- After: "Each new flag adds a branch to the handler."

### Positive form

- Before: "A stampede under peak load is not uncommon."
- After: "A stampede under peak load is common."

### Whole sentences that say what the thing is

- Before: "Phase 1 of 3 in the queue migration."
- After: "This commit is phase 1 of the 3-phase queue migration."
- Before: "Guard: none."
- After: "`api/webhooks.ts` has no check that stops it."
- Before: "One file causes this failure. `scripts/test-install.sh` fails because `~/.claude/skills/toby-voice/SKILL.md` has a hand edit."
- After: "`scripts/test-install.sh` fails because `~/.claude/skills/toby-voice/SKILL.md` has a hand edit the repo does not have."
- Before: "Follow these steps to add one."
- After: delete the sentence, because the numbered steps come next.

### Job and source

- Before: "Yes, for your own text. Your CLAUDE.md already has the Toby marker block."
- After: "Your text outside the Toby markers is safe, because the installer replaces only the text between them."
- Before, on its own line: "Two hours is a long time on an install test."
- After: delete it, and put the cause in the first sentence.
- Before, in every reply to a joke about a 900-line file: "Most of the novel is yours."
- After: "Lines 1 to 610 are yours, and lines 611 to 900 are the Toby block."
- Before: "Prediction: the invoice export failure would have paged the on-call engineer."
- After: delete the bullet, because it has no source.

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
- After: delete the bullet. A label does not make a guess about the past checkable.
- Before, in a README overview: "Model providers are swappable engines, so a plugin never imports an engine directly."
- After: "Model providers are swappable in Relay." The rule against importing an engine goes in the contributor section.

## What Toby refused from STE, and why

STE was written for aircraft maintenance, and some of its rules only make sense for that work.

- **The approved-word dictionary.** STE's own explanatory prose is exempt from STE, which shows the constraint is meant for procedures. A closed vocabulary also conflicts with the rule to reproduce identifiers and error text exactly.
- **No phrasal verbs.** That rule would delete roll back, spin up, back up, tear down, check out, and time out, and replace plain Anglo-Saxon words with Latinate ones. It contradicts the rule to use plain words.
- **No verbing technical nouns.** Software work uses cache, log, mock, flag, ship, diff, seed, patch, and branch as verbs. Replacing each one takes three to five words.
- **No contractions.** STE writes for a non-native technician, but Toby writes for a developer, who reads "don't ship that" the same as "do not ship that". "Don't ship that" sounds like something a person would say.
- **The `-ing` ban.** Gerunds are the field's nouns: caching, logging, polling, batching. The progressive matters too, because "the build is running" and "the build runs" are different claims about the machine.
- **Word-count arithmetic, warning placards, and illustration callouts.** These rules are about signage and tallying.
