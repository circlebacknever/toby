# Evals

These checks measure package consistency, agent behavior, and whether a reader understands an explanation.

Run the deterministic gates before and after any change to a skill or the operating guide, with approval under the operating guide:

```bash
python3 evals/run.py gates
```

A pass means no package metric regressed against `baselines/gates.json`. It doesn't establish that an agent applies the design principles.

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
| instruction sync | a synced copy of the guide drifting from `base/toby.md` |

Pass `--slow` to run the install smoke test in a temporary `HOME` directory.

The lost-rules gate compares the current prose sentences in `skills/` against `baselines/rules.txt`. When a rewording or deletion is intentional, update the snapshot with `python3 scripts/rule-inventory.py > evals/baselines/rules.txt` followed by `python3 evals/run.py record`.

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
| `content` | slogans, claim headings, deck titles, contributor rules, and six chat turns | `content-judge` | 5 |
| `content-judge` | distracting sentences across `content` and `voice` outputs | a person reading the judge output | 1 |
| `holdout` | regressions in six outputs on a product, incident, and chat session | a blind `holdout-judge` run | 5 |
| `holdout-judge` | distracting sentences across blinded `holdout` outputs | a person with the key outside the repo | 1 |
| `review` | whether code review catches seeded defects in the required format | a person against `suites/review.md` | 1 |
| `feature-dev` | whether `toby-build` sizes a copy edit and a multi-screen feature accurately | a person against `suites/feature-dev.md` | 1 |
| `build-execution` | implemented behavior, domain boundaries, and emitted success and failure diagnostics | independent execution grader and a person reading the diff | 1 |
| `bug-fix-execution` | repaired behavior, regression evidence, and diagnostics for a repeat failure | independent execution grader and a person reading the diff | 1 |
| `review-execution` | reachable regressions across twelve categories and guarded changes that should pass | private before/after probes and a separate reader matching findings | 1 |
| `learning` | whether `toby-learning` teaches a beginner in short interactive turns | a person against `suites/learning.md` | 1 |
| `explain` | whether `toby-explain` answers first, cites evidence, and stays concise | a person against `suites/explain.md` | 1 |

## Executable tasks

Use [execution cases](suites/execution.md) for actual build and bug-fix runs.
Prepare an isolated workspace, give its task to a fresh agent, then run the independent grader after the agent finishes.
Use the same fixture and prompt for each skill revision, with a separate workspace and fresh session for each run.
Keep the expected findings and grading code outside the agent's supplied workspace.
Inspect the resulting diff for module boundaries and contracts because behavior tests don't establish design quality.

Use [review execution](suites/review-execution.md) for fresh code-review sessions.
Its private probes establish the failures independently. A separate reader checks each submitted finding's trigger, mechanism, consequence, and repair before scoring it.
Unsupported or duplicate findings lose points, and a real unseeded defect requires separate verification.

Keep a result from each run, including failures and false alarms. Report counts as observations from those cases.
A single successful task doesn't establish general reliability or an improvement over another revision.
Read the code and explanation too, and use repeated independent samples before making a broader claim.

## Reader checks

`scripts/score-voice.py` checks syntax patterns. A zero score doesn't establish meaning, accuracy, or useful explanation.
Use the comprehension judge with the source facts when changing explanations or documentation:

```sh
python3 evals/run.py prompt readability-judge --folder /absolute/path/to/outputs --out /absolute/path/to/review.md --facts /absolute/path/to/task.md
```

The judge first writes what it understood, then checks that understanding against the facts.
Use `--sentences` only for isolated sentence checks that don't assess the document's meaning.
All judges preserve humor. Check whether the engineering explanation is accurate and understandable independently of its jokes.

Token growth remains a package budget. Before accepting a shorter replacement or recording changed baselines, compare actual behavior on the affected execution cases.
Record deliberate rule replacements after reviewing their effects. Don't treat a lower token count or syntax score as proof of better engineering.

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
