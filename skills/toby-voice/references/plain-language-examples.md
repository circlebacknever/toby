# Plain language, before and after

This file gives before-and-after pairs for the rules in `plain-language.md`.

## Before and after

### Sentence length

Keep most sentences to 25 words or fewer, or 20 words in a step the reader runs.

- Before (34 words): "To remove the cover assembly, first remove the four screws that attach the cover to the housing, and then, after taking the cover off the housing, remove the packing and throw it away."
- After: "Remove the four screws holding the cover to the housing. Lift the cover off. Discard the packing."

### Meaning over brevity

Keep every word that adds meaning, and don't drop facts to make a sentence shorter.

- Before: "Fixed. Tests green. Shipped."
- After: "The retry loop was swallowing the timeout. I fixed the handler, and the four failing tests now pass. The fix isn't deployed yet."

### Nouns after pronouns

- Before: "The migration touches the session table and the audit log. This is the risky part."
- After: "The migration touches the session table and the audit log. The audit-log write is the risky part."

### One name per thing

Pick the repo's own identifier and keep using it, because a synonym on second mention reads as a second object.

- Before: "`SessionStore` caches the token. The session cache expires it after an hour, so the credential holder needs a refresh."
- After: "`SessionStore` caches the token. `SessionStore` expires it after an hour, so the caller needs a refresh."

### Verbs for actions

- Before: "The handler performs a validation of the payload and then does the initialization of the worker pool."
- After: "The handler validates the payload, then initializes the worker pool."

### Noun stacks

When four or more nouns sit together, the reader has to guess which noun describes which.

- Before: "runway light connection resistance calibration"
- After: "calibration of the resistance in the runway light connection"
- Before: "user session token refresh failure rate"
- After: "how often refreshing a user session token fails"

### Explicit relations

Use a word such as `because`, `so`, or `but` that says how two clauses connect, and never join clauses with a semicolon or an em dash.

- Before: "The cache never invalidates — the TTL is set at construction."
- After: "The cache never invalidates, because the TTL is set at construction."
- Before: "Don't run the seed script; it truncates first."
- After: "Don't run the seed script, because it truncates the table first."

### Condition first

- Before: "Clear the cache if the build fails."
- After: "If the build fails, clear the cache."

### Prohibitions with consequences

- Before: "Don't call this from a request handler."
- After: "Don't call this from a request handler. It blocks for up to 30 seconds and exhausts the connection pool."

### Numbered steps

- Before: "Loading the fixtures while running the migration causes the seed to race the schema change."
- After: "1. Wait for the migration to finish.\n2. Load the fixtures, so the seed doesn't race the schema change."

### Banned words recast

When a banned word doesn't have a plain replacement, rewrite the sentence so the meaning is direct.

- Banned-word swap: "Cloze the word that carries the learning."
- Recast: "Blank out the word the learner must supply."
- Banned-word swap: "This is the load-bearing assumption of the design."
- Recast: "The design fails if this assumption is wrong."

### Cutting filler words

- Before: "This is basically just a fairly simple caching layer that essentially sits in front of the database."
- After: "This is a caching layer in front of the database."

### Active actors

- Before: "The column is dropped and the index is rebuilt during the migration."
- After: "The migration drops the column and rebuilds the index."
- Still right: "The file was deleted before the run started." (The person who deleted the file is unknown.)

### Standard words

Ask whether a reader could look the word up in a dictionary and find your meaning.

- Before: "Teaching prose is a first-read surface." → After: "The learner reads every sentence once."
- Before: "a component prop surface" → After: "a component's props"
- Before: "a hook's return shape" → After: "a hook's return type"
- Before: "the shape of a signature" → After: "what a signature exposes"
- Before: "Narrow the blast radius." → After: "Show the reader the smallest part of the code that could cause the failure."

### Whole sentences

These "Before" lines came from an overview where the words were plain and the sentences were short, yet the prose failed the Whole and Literal tests:

- Before: "A multi agent framework platform" → After: "Backplane is an extensible multi-agent platform."
- Before: "Users talk to agents. Agents read, call tools, and pause for people." → After: "Users instruct agents, and agents call tools and wait for human feedback."
- Before: "Two libraries carry the framework." → After: "The platform consists of a UI toolkit that all agents share and a runtime for building agents."
- Before: "A plugin is data. The framework compiles it." → After: "Developers define new agents as plugins."
- Before: "No plugin imports an engine. No framework file names a plugin." → After: delete both sentences, because a reader of an overview wouldn't assume a plugin imports an engine.

The first example is a fragment with no verb, the second and fourth chop one idea into slogan fragments, and the third uses `carry` as a metaphor.

### Literal verbs

- Before: "The rule lives in `AGENTS.md`." → After: "The rule is in `AGENTS.md`."
- Before: "This finding rests on reading the diff." → After: "I found this issue by reading the diff, and I didn't run the handler."
- Before: "When the cache is down, the request falls through to `load()`." → After: "When the cache is down, the request calls `load()` directly."
- Before: "Every lever feeds a formula." → After: "Every setting changes a number in a formula."
- Before: "Complexity creeps into the handler." → After: "Each new flag adds a branch to the handler."

### Positive form

- Before: "A stampede under peak load is not uncommon." → After: "A stampede under peak load is common."
- Before: "Guard: none." → After: "`api/webhooks.ts` doesn't have a check that stops a duplicate webhook from running twice."
- Before: "One file causes this failure. `scripts/test-install.sh` fails because `~/.claude/skills/toby-voice/SKILL.md` has a hand edit." → After: "`scripts/test-install.sh` fails because `~/.claude/skills/toby-voice/SKILL.md` has a hand edit the repo doesn't have."
- Before: "Follow these steps to add one." → After: delete the sentence, because the numbered steps come next.

### Job and source

- Before: "Yes, for your own text. Your CLAUDE.md already has the Toby marker block." → After: "Your text outside the Toby markers is safe, because the installer replaces only the text between them."
- Before: "The export query takes four seconds because the `orders.created_at` index is missing." (Untimed.) → After: "The export query is slow on the staging data. I haven't timed it or checked the indexes on `orders`."
- Before: "Stop searching the repo, because the cause is outside it." → After: "The cause is a hand edit in `~/.claude/skills/toby-voice/SKILL.md`, which is outside the repo."
- Before: "Each of the 6 failures would have succeeded on a retry or paged the on-call engineer." → After: "On the queue service, a job that fails its third retry pages the on-call engineer."

### Headings

A section heading is one to three words that name the topic, while a claim belongs in the body as a sentence.

- Before: "Uniformity is the failure" → After: "Varied replies"
- Before: "Geometry never carries a panel alone" → After: "Geometry placement"

### Modifier placement

Put each describing phrase next to the action it modifies, and name the actor after an opening `-ing` phrase.

- Before: "Check every prose file written this turn in two steps, without being asked." → After: "Even when the user doesn't ask, check every prose file you wrote during this turn."
- Before: "Read every sentence against the READ list after handling the findings." → After: "After you handle the findings, read every sentence against the READ list."
