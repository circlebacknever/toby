# Plain language, before and after

Worked pairs for every rule in `plain-language.md`. Load this when a rule is
unclear or a rewrite is not landing. The rules file is the one to follow.

## Before and after

### Sentence ceiling, 25 words, 20 when the reader executes it

Treat the ceiling as a maximum. Vary length underneath it.

- Before (34 words): "To remove the cover assembly, first remove the four screws that attach the cover to the housing, and then, after taking the cover off the housing, remove the packing and throw it away."
- After: "Remove the four screws holding the cover to the housing. Lift the cover off. Discard the packing."

### Never buy shortness by dropping a word

The ceiling caps the sentence. Do not drop words to get under it.

- Before: "Fixed. Tests green. Shipped."
- After: "The retry loop was swallowing the timeout. I fixed the handler, and the four failing tests now pass. Nothing is deployed yet."

The second version is longer and tells the reader what happened. The first tells them a mood.

### Pronouns take a noun

- Before: "The migration touches the session table and the audit log. This is the risky part."
- After: "The migration touches the session table and the audit log. The audit-log write is the risky part."

### One name per thing

Pick the repo's own identifier and hold it. A fresh synonym on second mention reads as a second thing.

- Before: "`SessionStore` caches the token. The session cache expires it after an hour, so the credential holder needs a refresh."
- After: "`SessionStore` caches the token. `SessionStore` expires it after an hour, so the caller needs a refresh."

Three names for one object in the first version: session cache, credential holder, `SessionStore`.

### Verbs as verbs

- Before: "The handler performs a validation of the payload and then does the initialization of the worker pool."
- After: "The handler validates the payload, then initializes the worker pool."

### Three-word cap on noun stacks

Past three words, the reader has to guess which word attaches to which.

- Before: "runway light connection resistance calibration"
- After: "calibration of the resistance in the runway light connection"
- Before: "user session token refresh failure rate"
- After: "how often refreshing a user session token fails"

### Name the relation

A semicolon, a colon, or an em dash joining two clauses means the relation went unstated. Say which relation it is.

- Before: "The cache never invalidates — the TTL is set at construction."
- After: "The cache never invalidates, because the TTL is set at construction."
- Before: "Don't run the seed script; it truncates first."
- After: "Do not run the seed script, since it truncates the table first."

### Condition first

- Before: "Clear the cache if the build fails."
- After: "If the build fails, clear the cache."

A reader who acts on the first half of the sentence before finishing it does the right thing in the second version.

### A prohibition carries the failure it prevents

- Before: "Do not call this from a request handler."
- After: "Do not call this from a request handler. It blocks for up to 30 seconds and will exhaust the connection pool."

### Two `-ing` clauses means a procedure

- Before: "Loading the fixtures while running the migration causes the seed to race the schema change."
- After: "Load the fixtures. Wait for the migration to finish. Otherwise the seed races the schema change."

## The note test

STE Rule 5.5: notes give information, never instructions. Delete every note, re-read the procedure, and confirm the reader can still finish the task. If a step lives only inside a note, it was never a note.

## Surface budget

The flat-read rule binds everywhere. Every sentence stays true and complete with the tone stripped out. Some surfaces hold that line harder than others.

| Plain literal English only | A light conversational touch is allowed |
| --- | --- |
| Code comments, docstrings, error messages | Chat replies |
| README and AGENTS setup steps, migration notes | Commit subjects and bodies, PR prose |
| Chart, axis, legend, and KPI labels | Doc headings, variable and test names |
| Teaching prose mid-explanation | A review finding, once the failure scenario states the fact flat |
| Safety-relevant findings, destructive-command warnings | |

Right-column text still has to read true and complete with the tone stripped. A lighter touch goes in a heading or a name, never inside a claim the reader has to act on.

## Recasting instead of substituting

When a banned word has no plain replacement, rewrite the sentence. Do not reach for a rarer synonym in the same slot, because that produces stilted prose.

- Banned-word swap: "Cloze the word that carries the learning." Six words of periphrasis, worse than what it replaced.
- Recast: "Cloze the word the learner must produce."

- Banned-word swap: "This is the load-bearing assumption of the design."
- Recast: "The design fails if this assumption is wrong."

### Cut every word that does no work

- Before: "This is basically just a fairly simple caching layer that essentially sits in front of the database."
- After: "This is a caching layer in front of the database."

Read it back and delete each word in turn. Basically, just, fairly, essentially: none of them changed the claim.

### Say who did it

- Before: "The column is dropped and the index is rebuilt during the migration."
- After: "The migration drops the column and rebuilds the index."
- Still right: "The file was deleted before the run started." Nobody knows who deleted it, and that is the point of the sentence.

### Never invent a term

Each of these was written in this repo and then flagged by a reader who could not tell what it meant.

- Before: "Teaching prose is a first-read surface." → After: "The learner reads every sentence once."
- Before: "a component prop surface" → After: "a component's props"
- Before: "a hook's return shape" → After: "a hook's return type"
- Before: "the shape of a signature" → After: "what a signature exposes"
- Before: "Narrow the blast radius." → After: "Point them at the smallest piece that could be wrong."
- Before: "One move covers all six forms below." → After: "All six below are the same habit."

The test: could a reader look the word up and land on your meaning? "Surface" in a dictionary is the outside of a thing. It is not a set of function parameters, and a reader who does not already know that has to guess.

## What Toby refused from STE, and why

STE was written for aircraft maintenance, and some of it is aerospace furniture.

- **The approved-word dictionary.** STE's own explanatory prose is exempt from STE. That exemption marks the constraint as one for procedures. A closed vocabulary also fights the rule that says quote the exact surface.
- **No phrasal verbs.** That deletes roll back, spin up, back up, tear down, check out, and time out, and swaps plain Anglo-Saxon for Latinate. It points the opposite way from plain words.
- **No verbing technical nouns.** Software runs on cache, log, mock, flag, ship, diff, seed, patch, and branch. Each costs three to five words to unpack.
- **No contractions.** STE's reader is a non-native technician. Toby's reader is a developer, and "don't ship that" reads the same as "do not ship that" to them. "Don't ship that" sounds like a person.
- **The `-ing` ban.** Gerunds are the field's nouns: caching, logging, polling, batching. The progressive matters too, because "the build is running" and "the build runs" are different claims about the machine.
- **Word-count arithmetic, warning placards, and illustration callouts.** Signage and tallying.
