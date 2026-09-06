# Evals

Run this before and after any change to a skill, the operating guide, or a hook.

```bash
python3 evals/run.py gates
```

Green means nothing regressed. Red names what did, and every number it compares
against sits in `baselines/gates.json`.

## The two kinds of check, and why they are separate

**Gates** run with no model. They are deterministic, they gate, and they are the
only part safe to wire into CI. A gate that gets worse fails the run. A gate that
gets better is recorded on purpose with `evals/run.py record`, which is the step
that makes an improvement permanent.

**Model suites** need a subagent to write something, so they cannot gate. They
record a distribution and never a score. Five samples of the voice suite on
byte-identical inputs scored 1, 1, 4, 4, and 11. A single run of it proves
nothing, and two runs of it once produced a confident wrong answer that five
runs took back.

## Gates

| Gate | Catches |
|---|---|
| validator errors | a banned word, a broken sync, a skill naming the guide by path, a description with a skill name split across a line wrap |
| warning counts by class | a new foil, a sentence over the ceiling, a buried lead, a missing skip clause, a cross-skill sentence collision, a coined term |
| body tokens per skill | a body that grew more than 10 percent |
| co-load tokens per routing group | a group that grew more than 5 percent, which is what a task actually pays |
| lost rules | a sentence that left the repo with no reworded survivor |
| validator fixtures | a check in `validate-skills.py` that stopped being able to fail |
| stop hook fixtures | the voice hook missing a seeded break, or firing on a clean reply |
| instruction sync | a copy of the guide edited instead of `base/toby.md` |

`--slow` adds the install smoke test, which installs into a throwaway HOME.

The lost-rules gate compares against `baselines/rules.txt`, a snapshot of every
prose sentence in `skills/`. It reads zero accepted deletions today, because the
snapshot was retaken once the skill work landed. Re-take it with
`python3 scripts/rule-inventory.py > evals/baselines/rules.txt` followed by
`evals/run.py record`, and only after reading what the gate reported.

The gate holds a list, and not a count. A deletion arriving the same
week as a rewording keeps the count still and swaps the contents, so the
baseline is the sentences themselves. It also demands a complete match for a
sentence under eight content words: three common words landing in an unrelated
sentence clear a 60 percent overlap on their own, and "Mock external
dependencies at the system boundary" survived exactly that way while the rule
was gone.

## Model suites

```bash
python3 evals/run.py list
python3 evals/run.py prompt voice        # hand this to a subagent, once per sample
python3 evals/run.py compare voice evals/results/voice-*.md
```

`compare` prints both distributions and refuses to call a difference real when
the ranges overlap.

| Suite | What it measures | Scored by | Minimum samples |
|---|---|---|---|
| `triggering` | which skills a description makes fire, across four positive and six over-triggering prompts | `evals/run.py compare triggering` | 2 |
| `voice` | banned words, foils, sentence length, clause welds in four written outputs | `scripts/score-voice.py` | 5 |
| `review` | whether a review catches three seeded defects and reports them the way the skill specifies | a person, against `suites/review.md` | 1 |
| `feature-dev` | whether the process a request gets matches its size | a person, against `suites/feature-dev.md` | 1 |
| `learning` | whether a beginner gets taught in steps without a wall of text | a person, against `suites/learning.md` | 1 |
| `explain` | whether an answer is short, backed, and leads with the answer | a person, against `suites/explain.md` | 1 |

### Recorded results

`baselines/triggering.json` — seven false firings across the over-triggering
probes before Group 2, zero after, confirmed by a second run whose instructions
never mentioned skip clauses. This is the number that pass actually bought.

N5 and N6 cover `toby-game` and `toby-squall`, which fire only when the user
names them. Both stayed silent on a prompt carrying every trigger noun in their
descriptions. `check_invoke_only` in the validator holds the same rule from the
other side: each of them must state it in its description and carry a matching
invoke-only line in the guide's Skill Routing, and the guide may not route
either on conditions.

Each scenario carries a fenced block of directives — `Required`, `Forbidden`,
`Optional`, `Exactly one of` — and the runner scores against those. The agent
writing a run reports only what fired. It used to report its own totals while
being told not to read the expected sets, so it guessed them, and one run
counted a correct firing on N1 as a false fire.

`baselines/voice.json` — four arms, none of them separated. Reference loaded:
1, 1, 4, 4, 11. No reference: 8, 8, 12, 4, 3. Writing-sections extract: 7, 9.
Extract plus Self Review: 5, 4. **The duplicated operating guide stays because
it is the status quo, and for no stronger reason.** Anyone reopening that
question needs a sharper instrument before more samples are worth buying.

`baselines/feature-dev.json` — a copy change and a seat-limit feature run
through the skill. The copy change came back tactical and handed straight back
under the skip clause. The seat limits came back strategic on two triggers at
once. The run also said the tactical row is still heavy for a one-line copy
change, which is why the sizing section now says to check the skip clause before
sizing anything.

`baselines/explain.json` — three runs of the same four questions. The evidence
rule held from the first run: every claim carried a path and a line, and "safe
to remove" came back as a guess with the missing test run named. The length rule
took two tries. Written as prose it moved nothing, and a 42-word sentence
survived. Written as three numbered limits with a word count in them, the
beginner question went from 108 words and two clause welds to 59 words and none.

`baselines/review.json` — the same seeded diff before and after the compliance
pass. The old skill caught the bug and bundled the two missing tests into one
line. The new one named each criterion as its own finding and caught a fourth
defect, and it routed a security bug to `toby-swd-interfaces`, which owns
nothing about it. The frame now says a bug needs no routing, so a later run
repeating that is a regression.

## The coined-term check

Rule 14 of `plain-language.md` says never invent a term, and this check holds it.
Every entry in `COINED_TERMS` was written in this repo and then flagged by a
reader who had to stop and work out what was meant. Each one is a real English
word, so the banned list and the sense-scoped list both pass it, and no other
check sees it.

`primitive` was tried and removed. It is a real term in graphics and in
programming, and every hit was correct usage. Add a term only after it has
confused a reader here.

## The figurative-frame check

A sentence cannot wear a hat. The check holds the guide's ban on invented
metaphor, and it catches the commonest form that ban takes here: an abstract
thing described as if it had a body or clothes.

Every frame in `FIGURATIVE_FRAMES` was written in this repo, and the fixtures in
`tests/test-validator-checks.py` quote four of them.

The list holds frames, not subjects, so a fresh metaphor built from a frame
nobody has used yet walks past it. A reader is the only check for that one.

`moving parts` was tried and left out. It is a dead metaphor, it is in the
dictionary, and the guide keeps established terms of art.

## The nine `shape` warnings that stay

`toby-artifact-style` names real geometry: a logo primitive, a decorative
triangle, the outline a drag coefficient belongs to. The sense-scoped rule bans
`shape` as an intensifier, and there the word names the thing itself. They stay as
warnings so the count catches a tenth one, which would be a new abstraction
and not another triangle.

## What the voice scorer cannot see

It counts banned words, invented foils, sentence length, and clause welds. It
does not read register. On the sample that scored 11, two flagged foils were
distinctions the writer needed: "per-account, where it was per-route-per-account"
describes a real behavior change. And the wording that reads as a stranger
wearing Toby's clothes passes every check in the file. A category noun stands
where a concrete one belongs, and `move`, `form`, and `frame` do the work
`habit` and `sentence` should do. That failure is found by reading, and the suite
does not find it.

## Adding a case

**A gate**, when the thing is deterministic: add the check to
`scripts/validate-skills.py`, add a fixture either side of it in
`tests/test-validator-checks.py`, add its warning kind to `warning_classes()` in
`run.py`, then `evals/run.py record`. Prove it fails before you record it.

**A model suite**, when the thing needs writing: add the cases to
`suites/<name>.md`, add an entry to `SUITES` in `run.py` with its prompt and its
minimum sample count, run it that many times, and record the distribution in
`baselines/<name>.json`. Set the minimum from the spread you measure, and not
from what is convenient.

## Layout

```
evals/
  run.py             the runner
  suites/            the cases, one file per suite
  fixtures/          inputs a suite feeds to a subagent
  baselines/         recorded numbers, and runs/ for the outputs behind them
  results/           scratch from a run, ignored by git
  boundaries.md      which skill owns which decision, behind the skip clauses
  grading.md         the before-and-after write-up for the Group 2 and 8 changes
```
