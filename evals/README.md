# Evals

Run the deterministic gates before and after any change to a skill, the operating guide, or a hook:

```bash
python3 evals/run.py gates
```

Green means no gate regressed, and red names what failed against `baselines/gates.json`.

## Gates and model suites

- **Gates** run without a model and exit 1 when a metric gets worse. Record an intentional improvement with `python3 evals/run.py record`.
- **Model suites** prompt a subagent to write prose or review code, so they record a distribution across multiple samples (`Five samples of the voice suite on identical inputs scored 1, 1, 4, 4, and 11`).

## Gates

| Gate | Catches |
|---|---|
| validator errors | a banned word, a broken sync, a skill naming the guide by path, a description with a skill name split across a line wrap |
| warning counts by class | a new foil, a sentence over the ceiling, a buried lead, a missing skip clause, a cross-skill sentence collision, a coined term |
| body tokens per skill | a skill body that grew more than 10 percent |
| co-load tokens per routing group | a routing group that grew more than 5 percent |
| lost rules | a sentence deleted from `skills/` with no reworded survivor |
| validator fixtures | a check in `validate-skills.py` that stopped failing on a seeded error |
| stop hook fixtures | the voice hook missing a seeded break, or firing on a clean reply |
| instruction sync | a synced copy of the guide drifting from `base/toby.md` |

Pass `--slow` to run the install smoke test in a temporary `HOME` directory.

The lost-rules gate compares the current prose sentences in `skills/` against `baselines/rules.txt`. When a rewording or deletion is intentional, update the snapshot with `python3 scripts/rule-inventory.py > evals/baselines/rules.txt` followed by `python3 evals/run.py record`.

## Checking prose by hand

`scripts/voice-check.py` runs the pattern checks against a file, directory, or stdin:

- `FIX` findings break a rule with no judgment call and make the checker exit 1.
- `DECIDE` findings flag likely breaks for the writer to verify and never fail the run.
- `READ` lists the 18 rules that regex patterns can't check.

`tests/test-voice-recall.py` runs the checker across `evals/gold/*.jsonl` and reports how many bad rows trigger `FIX` or `DECIDE`, while failing if any non-heldout `"good"` row triggers `FIX`. `evals/gold/heldout.jsonl` tests literal uses of trigger words to measure precision.

## Token budget

`scripts/token-budget.py` prints the token cost of the resident operating guide, each loaded skill body, and its reference files.

## Model suites

```bash
python3 evals/run.py list
python3 evals/run.py prompt voice        # hand this to a subagent, once per sample
python3 evals/run.py compare voice evals/results/voice-*.md
```

`compare` prints both distributions and reports a difference only when the sample ranges don't overlap.

| Suite | What it measures | Scored by | Minimum samples |
|---|---|---|---|
| `triggering` | which skills fire across 25 positive and 7 over-triggering prompts | `evals/run.py compare triggering` | 2 |
| `voice` | banned words, foils, sentence length, and clause welds in six outputs | `scripts/score-voice.py` | 5 |
| `content` | slogans, claim headings, deck titles, contributor rules, and six chat turns | `scripts/voice-check.py`, then `content-judge` | 5 |
| `content-judge` | distracting sentences across `content` and `voice` outputs | a person reading the judge output | 1 |
| `holdout` | six outputs on a product, incident, and chat session no rule was tuned against | a blind `holdout-judge` run | 5 |
| `holdout-judge` | distracting sentences across blinded `holdout` outputs | a person with the key outside the repo | 1 |
| `review` | whether code review catches seeded defects in the required format | a person against `suites/review.md` | 1 |
| `feature-dev` | whether `toby-build` sizes a copy edit and a multi-screen feature accurately | a person against `suites/feature-dev.md` | 1 |
| `learning` | whether `toby-learning` teaches a beginner in short interactive turns | a person against `suites/learning.md` | 1 |
| `explain` | whether `toby-explain` answers first, cites evidence, and stays concise | a person against `suites/explain.md` | 1 |

## Layout

```text
evals/
  run.py             the runner
  suites/            the evaluation tasks, one file per suite
  fixtures/          inputs handed to subagents
  gold/              labeled good and bad sentences for voice recall and precision
  rubric/            pass and fail criteria for human and LLM graders
  baselines/         recorded gate metrics and baseline runs
  results/           scratch outputs from a run, ignored by git
  boundaries.md      skill routing ownership and skip-clause coverage
  grading.md         before-and-after summary for triggering and code review
```
