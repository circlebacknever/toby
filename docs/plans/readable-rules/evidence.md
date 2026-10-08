# Evidence for the readable-rules plan

This file lists real sentences that the current rules made harder to read. It also lists the user's own complaints about replies they could not follow. Two read-only agents collected them on 2026-10-08. One searched `evals/results/` and `evals/baselines/runs/`, and the other searched the 18 session transcripts for this repo. Every quote below is exact. A "plain" line is the agent's proposed rewrite, and the user has not approved any of them.

## User complaints

These are the user's own words about replies they could not follow, with the cause the transcript agent found.

| User said | About | Likely cause |
| --- | --- | --- |
| "I read the message and didn't understand it because of the first 3 bullet points" (Oct 3) | a broken definition, a fragment, and picture words such as "sit on" and "lands" | homemade plain words standing in for standard math terms |
| "The frick does the last sentence mean? What am I supposed to check?" (Sep 15) | "Your rulings at the end of this page check that." | a vague `that` after a split, and a verb the subject cannot do |
| "with the code shown is bizzare" (Sep 15) | "With the code shown, this test fails in every timezone, ..." | a condition placed first |
| "woah 'the separate modes for interpretation subjects and for memorizing lists,' what was the deal for separate modes" (Oct 3) | an in-repo noun stack | internal terms |
| "Check every prose file written this turn in two steps, without being asked. ... confusing" (Sep 17) | a line in `base/toby.md` | two modifiers on one verb |
| "'Add no new facts' are you sure? That is difficult to understand" (Oct 8) | a line in `skills/toby-plain/SKILL.md` | words cut to compress the sentence |
| "Found a broad or risky action ... Need approval" (Sep 15) | the work-loop template | the template had no subject |
| "a big long message that is not straight forward or easy to understand at all" (Oct 8) | long-session reports | general |

The user also flagged these Claude defaults, which led to the current rules. A change must not bring them back.

> "Users talk to agents. Agents read, call tools, and pause for people." (clipped run)

> "A plugin is data. The framework compiles it." (slogan)

> "Two libraries carry the framework." (figurative verb)

> "Copy the shape, not the words" (foil), and the user called it infuriating.

> "it is a real tension, not a free addition" (foil)

> "five sentences wearing a hat" (metaphor)

> "During that day, `utilizationPct` reports the row as used up, and no purge removes it." (negated actor)

## Rule-bent sentences

Each heading states the rule that the agents found making the sentence harder to read. Each example is a blockquote, so the voice checker skips the quoted text.

### Sentence split to stay under 25 words

> "CI runs in UTC. That explains why it fails on CI about one run in nine and passes locally every time." (`evals/results/settle/voice-x01.md:2`)

> "Its memory use is 71 percent. It rises about 3 percentage points a week, so at that rate it reaches 100 percent in roughly 10 weeks." (`settle/holdout-x01.md:26`)

> "So no code outside the worker depends on the wrapper." (`settle/explain-x05.md:11`)

> "It confirms an install with conflicts stops all tools and writes nothing. It confirms a dry run lists the conflicts and exits 0. It confirms the write hook skips a lone stale checker." (transcript, Sep 15)

> "That puts the check on the page, which it currently skips." (transcript, Sep 25)

> "On the HEAD copy of `SKILL.md`, ... each get a FIX. It missed them for two reasons" (transcript, Oct 3). `It` means the checker, and the nearest noun is `SKILL.md`.

### Colon or semicolon removed

> "A design smell finding has four lines. They are the entry name from `references/smells.md`, the file:line, ..." (transcript, Sep 25). The earlier text read "four lines: the entry name, ...".

> "`user session token refresh failures` stacks five words, so it becomes `failed token refreshes`." (transcript, Aug 16). The original used a semicolon.

> After a hook flagged a 47-word sentence, the list "five seeded defects: a pass-through wrapper; ..." became "The first defect is a pass-through wrapper. The second is an interface method..." (transcript, Sep 25).

### A forced or false `because` or `so`

> "CI runs in UTC, so the test fails there about one run in nine." (`evals/results/g8/voice-g8-4.md:2`). The judge had failed "CI runs in UTC." for having no connector. The `so` claims UTC alone causes the one-in-nine rate, which nothing showed.

> "It is not finished yet, because 861 rows matched and 39 went to `review.csv`." (`settle/holdout-x01.md:69`)

> "My answer is the same, because the index on `orders(created_at)` is unused." (`settle/voice-x05.md:16`)

> "The gate test fails only because it flags the plan-location wording I replaced, so I am reading the behavior record files next." (transcript, Sep 25)

> "Nothing is committed, so 25 files are still uncommitted in the working tree." (transcript)

> "No file was shown in this chat, so I cannot cite a line, and this is the general reasoning." (`settle/explain-x01.md:3`)

### Stacked clauses

> "Every query filters on `tenant_id` first, which is why I called the index on `orders(created_at)` unused, and your reply gives no query that changes that." (`settle/voice-x03.md:18`)

> "The lost-rules gate failed on the old sentence, which is the intended rewording, so I recorded it, and all gates hold." (transcript, Oct 7)

> "Each await hands control back to the event loop, which runs `console.log("after run")` and resumes the loop when the timer resolves, so two iterations take 200 ms in total." (`settle/explain-x04.md:17`)

### Contradicting checks with no passing wording

> The rubric fails "Each status change inserts a row. The support page reads the rows in time order." as choppy, and the user agreed. The grader also failed the joined version as tangled, so no wording passed (transcript, Sep 15).

> The checker flags "Errors stopped at 14:47. No payment data was lost." as a clipped run, and it also flags two facts joined by `and`.

> The rubric passes "Five outputs per guide is a small sample, and Fable only has two." The checker's "two facts joined by and" pattern exists to flag that sentence.

> The checker flags sentences of 26 words and up, and the guide says under 25.

### Checker pressure

> The "mirrored bullets" flag turned the list "1. If I gave you a file, rewrite that file. 2. If I pasted some text, rewrite that text. 3. If I gave you nothing, rewrite your last reply." into one sentence (this session, Oct 8).

> The buried-lead check's 16-word floor turned "Talk to me like a friend who knows the subject and wants me to get it." into "Talk to me like a friend who knows the subject well." The point about wanting the reader to understand got lost (this session).

> The stop hook once counted a whole table as one 161-word sentence, and the agent rewrote the table as prose (transcript).

### Internal labels and homemade terms

> "b28, b29, and b30. Each is wrong because of what the user asked." (transcript)

> "The six shared explain A2 fails don't come from any task." (transcript, Oct 7)

> "Five of the 50 fail the same sentence, whose wording comes from the task, and the g1 judge passed that sentence." (transcript, Oct 7)

> "closest to failing" written for "borderline" (`evals/gold/labels.jsonl` r09)

> "Code nothing reaches" written for "unreachable code" (`evals/gold/repo-review.jsonl` rC25)

> "a line the rule never turns" written for an eigenvector (transcript, Oct 3)

### Boilerplate

> "I have not fixed it yet, so the fix is not verified." (`settle/voice-x07.md:2`)

> "The claim that removal is safe is therefore unverified for behavior." (`settle/explain-x04.md:25`)

## Where the evidence is weak

- Neither agent found the banned-word list producing an unreadable sentence in eval outputs, and the transcripts held three examples.
- Neither agent found the negated-actor rule producing a sentence the user could not follow.
- The transcript agent did not read the whole `3f6dd26f` and `ccfae6f7` transcripts.
