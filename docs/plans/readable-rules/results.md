# Results of the readable-rules change

The rule changes removed internal labels from Toby's reports and cut vague "It" and "That" openers. They did not bring back Claude's default habits, apart from one voice regression that a revert fixed. No validated readability judge measured clarity, so the side-by-side samples below are the evidence for you to judge.

## What changed

- `base/toby.md` and its synced copies now say these things:
  - Understanding on the first read ranks above brevity, but it never allows a recap.
  - Internal labels such as test ids and rule numbers get explained or left out.
  - "Because" marks only a cause, and "so" marks only a result.
  - A sentence holds at most one "which" clause.
  - A colon may introduce a list of three or more items.
  - A sentence may open with "It" only when one earlier noun fits.
  - The grammar-jargon rule names, such as "negated actor", are now plain sentences.
- Every skill file was cold-read by a separate agent and rewritten in plain words. Three more agents then compared all 435 reworded sentences against the originals. They found 19 places where a rule had narrowed or widened, and I restored all 19.
- The checker no longer flags a list of "If" cases as mirrored bullets. It flags "Noted", "Got it", and "Understood" as reply openers. Its advice no longer says only "split it".
- The judge rubric now passes two facts about one process joined by "and". It adds three fail categories: a false "because" or "so", an unclear "It" or "That", and an unexplained internal label.
- `toby-plain` is a new skill that only you can start, with `/toby-plain`.

## How it was measured

Sonnet 5.5 wrote every output, and Opus 5.5 judged them blind. The before arm read the rules at commit `838cc04`. A third arm wrote with no Toby rules at all.

| Suite | Before | After | No rules |
| --- | --- | --- | --- |
| holdout (README, incident, options, review, changelog, chat) | 12 | 12 | 3 |
| report (final report, review summary, "what does that mean?") | 12 | 12 | 3 |
| voice (six short replies) | 6 | 6, then 6 more after the revert | 0 |
| explain (four questions) | 3 | 3 | 0 |

The plan fixed two judges in advance and tested each one before any writer ran.

- The defaults judge looks only for Claude's default habits. It caught 88 percent of the user-flagged bad sentences and passed 80 percent of the good ones on a held-out set, so it was used.
- The readability judge read cold and flagged sentences it could not follow. It caught only 3 of the 8 sentences you said you could not follow, so the plan dropped it. The test was weak too, because those sentences were confusing in their original context and read fine alone.

## Results

### Internal labels and vague openers

These counts come from the before-arm checker, so both arms are measured the same way.

| Count per file | Before | After |
| --- | --- | --- |
| Internal labels in the report suite, such as `F1`, `P1`, `g2`, `B3`, `A1` | 16 in 12 files | 0 in 12 files |
| Sentences opening with a bare It, This, That, or So, holdout suite | 5.9 | 1.8 |
| Same, report suite | 1.3 | 0.8 |
| Sentences over 25 words, report suite | 1.6 | 0.1 |
| Words per output, report suite | 327 | 300 |
| Dashes, semicolons, and "X, not Y" foils, all suites | 0.1 | 0 |

Every file in both arms states the ticket number `PAY-212`. The label count leaves it out because a reader would know it.

### Claude's default habits

These are fails per file from the defaults judge. A difference counts only when the 90 percent bootstrap interval excludes zero.

| Suite | Before | After | Interval (after minus before) | Verdict |
| --- | --- | --- | --- | --- |
| holdout, pass 1 | 4.50 | 3.75 | -1.67 to 0.17 | no difference shown |
| holdout, pass 2 | 4.58 | 3.67 | -2.00 to 0.08 | no difference shown |
| report, pass 1 | 1.58 | 1.25 | -1.08 to 0.42 | no difference shown |
| report, pass 2 | 2.17 | 1.17 | -1.83 to -0.17 | fewer fails after |
| explain | 4.00 | 3.33 | -2.00 to 0.67 | no difference shown |
| voice, first after arm | 2.00 | 4.00 | 0.33 to 3.50 | regression |
| voice, after the revert | 2.50 | 2.83 | -0.67 to 1.50 | no difference shown |

The no-rules arm averaged 9.0 fails per holdout file, about twice the Toby arms, so the judge can tell the defaults apart.

### The voice regression and the revert

The first after arm wrote runs of short, unconnected sentences, such as "CI runs in UTC. The test fails on CI about one run in nine. It passes locally every time." Two of my changes caused it:

- I rewrote the connector sentence in the Whole test so it described connectors and stopped telling writers to use one.
- I added advice to split long sentences.

I reverted both and kept the new "because only for a cause" limit. The voice suite ran once more and came out level with the before arm. The holdout, report, and explain after arms were written before this revert, so their numbers come from the earlier wording.

## Side by side

Here is task 3 of the report suite, where the user asks "what does that mean?" after a message full of labels.

Before (`before/report-09.md`):

> I made an edit that worsened a style check, undid it, and the check is back where it started. The check runs without an AI model and counts style warnings by type. My earlier message called it the g2 gate.
>
> One warning type, which I called buried-lead, flags a section whose first sentence gives background before the rule. Its count rose from 10 to 11 after B3, my third edit to the skill files. I reverted B3 and re-ran the check, and every count matched its recorded level.
>
> Two warnings remain in A1, the first file I edited. They flag the word "shape", and both were there before I started.

After (`after/chat-09.md`):

> My third edit made the repo's style check report one more warning, so I undid the edit. The check runs with no AI model and counts style warnings by type. One type flags a section whose first sentence gives background before it states the rule. That count rose from 10 to 11 after my third edit to the skill files.
>
> After I undid the edit and ran the check again, every count was back to its recorded level. Two warnings that flag the word "shape" remain in the first file I edited. Both were there before I started.

Every output is in `evals/results/readable/before/`, `after/`, `after2/`, and `norules/`.

## Sentences the defaults judge failed

Before:
- "The limit sits behind the flag `RL_STRICT`, which is off by default." (figurative)
- "I found the cause of the flaky test." (deferred)
- "Your message adds no new fact, so my answer stays." (deferred)
- "They flag the word "shape"." (slogan)

After, including the voice rerun:
- "CI runs in UTC." (slogan)
- "The team agreed on two follow-ups." (deferred)
- "I can start on the write step now." (closing offer)
- "Your index usage statistics would settle it." (figurative)

These fails look like false positives:
- "Removed: the `--legacy-match` flag, which was deprecated in version 2.1." The task asked for a changelog, which uses that format.
- "**Fires when.** Every load of the admin dashboard, because the handler runs on every load." The review skill requires that label format.
- "Parsers must not make network calls." The task gave this fact word for word.

## Sentences the defaults judge passed

Before:
- "An alert fired at 14:09 and went to a Slack channel that was archived in July."
- "I moved rate limiting from the three route files into one middleware."

After:
- "That adds 7 ms at p95 to each page load in staging."
- "The limit is behind the flag `RL_STRICT`, which is off by default, so behavior stays the same until the flag is on."
- "A retry wrapper around the whole sync job will write duplicate rows, because the job is not idempotent."
- "Your reply adds no query or statistic that changes this."

## Costs

- Skill bodies grew because plain wording takes more words. `toby-game` grew from 753 to 1,028 tokens, `toby-artifact-style` from 2,929 to 3,374, and `toby-voice` from 840 to 1,008. The strategic build turn grew from 15,691 to 17,202 tokens. I recorded these increases in `evals/baselines/gates.json`, so the token gates pass again.
- Closing offers in the voice suite rose from 1 to 5 across six files after the revert. The before arm had the same habit, so the plan does not count it as a regression.

## Questions for you

1. The rewrite found contradictions that I left alone:
   - `toby-artifact-style` disagrees with itself on letter-spacing for big display text. It also calls a 4px line a "hairline" while its glossary defines a hairline as 1px. It disagrees on whether the end slide holds one sentence or a paragraph, and on when a chart needs a legend. Its focus ring is 2px in one place and a hairline in another.
   - `toby-game` says to compute the outcome first and then animate it, and also says never to roll the outcome and animate toward it. It also says to stay silent when nothing changes, and to post a news line every 25 to 40 seconds.
   - `toby-swd-interfaces/references/runtime-config.md` tells a module never to import the config module, and later says to use imported config values. `databases.md` there calls `UnitOfWork.isActive()`, but the interface it shows has only `run`.
2. `toby-optimize/references/databases.md` says 50 orders with 5 line items take 351 queries, but 1 + 50 + 250 is 301.
3. The rubric now passes "Each status change inserts a row, and the support page reads the rows in time order." You ruled the split version choppy, and before this change the rubric failed both versions.
4. The token growth listed under Costs can stay, or I can trim the largest skills back toward their old sizes.

## Not done or not verified

- Nothing is committed. The installed copies under `~/.claude` are unchanged. The hooks run from this checkout, so they already use the new checker.
- The holdout, report, and explain after arms used the wording from before the revert, and only the voice suite was rerun.
- Explain writers differed in whether they loaded `plain-language.md`, in both arms, which adds noise to that suite.
- Clarity itself has no validated measure. Read the samples and decide.
