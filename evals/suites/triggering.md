# Trigger scenarios

This suite has 32 prompts. Each names the skill that should load and the skills that must
not. A skill that fires when it should not costs 100 percent of its tokens, so
the seven probes at the end count as much as the positives.

The runner shows an agent the listing that `scripts/trigger-probe.py` prints
for Claude Code, Codex, and Copilot, and asks which skills it would load. That
listing has the 11 entry skills: `toby-build`, `toby-bug-fix`, `toby-optimize`,
`toby-refactor`, `toby-swd-testing`, `toby-code-review`, `toby-explain`,
`toby-swd-experiment`, `toby-swd-environment`, `toby-voice`, and
`toby-artifact-style`. The six method skills and the three invoke-only skills
are hidden there, so a hidden skill in a Forbidden line can fire only in the
Kiro listing, which shows all 20. The agent sees only the descriptions, because
a host tool reads only the descriptions when it picks a skill.

P1 to P4 and N1 to N7 are the earlier prompts with new directives. P5 to P25
are rows 12 to 32 of the request map in
`docs/plans/token-efficiency/research/skill-architecture.md`.

## Positive probes

### P1 — repository method with a cache and an error path
> Add a `getAccountBalance(userId)` method to `AccountRepository`. It should read
> from the Redis cache first, fall back to Postgres, and return null when the
> account is missing.

```
Required: toby-build
Forbidden: toby-optimize, toby-refactor, toby-swd-experiment, toby-swd-environment, toby-swd-docs, toby-game, toby-squall
```

Should load: `toby-build`, which opens `toby-swd-interfaces`, `toby-swd-errors`, and `toby-swd-testing`.
Should not load: `toby-optimize`. Its description skips new behavior that includes a cache.

### P2 — split a module
> `src/billing/invoice.ts` is 1,400 lines and handles invoice generation, PDF
> rendering, and the dunning emails. Split it.

```
Required: toby-refactor
Forbidden: toby-build, toby-swd-experiment, toby-swd-modules, toby-game, toby-squall
```

Should load: `toby-refactor`, which opens strategy, modules, and docs.
Should not load: `toby-build`. Its description skips work where behavior stays the same.

### P3 — feature request
> Build the CSV export for the reports page. Users pick a date range and get a
> download.

```
Required: toby-build
Forbidden: toby-refactor, toby-code-review, toby-swd-testing, toby-game, toby-squall
```

Should load: `toby-build`, and the method skills it opens per step.
Should not load: `toby-swd-testing`. Its description skips work that changes production code.

### P4 — migration and a seed script
> Run the pending migration against my local database and re-seed it.

```
Required: toby-swd-environment
Forbidden: toby-build, toby-swd-strategy, toby-swd-modules, toby-swd-interfaces, toby-swd-testing, toby-game, toby-squall
```

Should load: `toby-swd-environment`.
Should not load: anything else. No other entry description lists a migration.

### P5 — tidy control flow and rename
> Tidy the confusing control flow in `parseArgs` and rename its variables.

```
Required: toby-refactor
Forbidden: toby-code-review, toby-build, toby-swd-clarity
```

Should load: `toby-refactor`, which opens clarity and its `comments.md`.
Should not load: `toby-code-review`, which skips a request to change code.

### P6 — refactor rules into one function
> Refactor the checkout service so the discount rules are in one function.

```
Required: toby-refactor
Forbidden: toby-build, toby-swd-strategy, toby-swd-modules
```

Should load: `toby-refactor`, which opens strategy and modules.
Should not load: `toby-build`, which skips work where behavior stays the same.

### P7 — de-duplicate two helpers
> De-duplicate the two date-formatting helpers into one shared module.

```
Required: toby-refactor
Forbidden: toby-build, toby-swd-modules
```

Should load: `toby-refactor`.
Should not load: anything else. No other entry description lists de-duplicate.

### P8 — simplify dead error handling
> Simplify the error handling in `upload.ts`, because half the catch blocks can
> never run.

```
Required: toby-refactor
Forbidden: toby-swd-errors, toby-bug-fix, toby-build
```

Should load: `toby-refactor`, which opens errors.
Should not load: `toby-swd-errors`, which is hidden.

### P9 — snapshot update
> Update the Jest snapshots for the `Header` component.

```
Required: toby-swd-testing
Forbidden: toby-swd-environment, toby-build
```

Should load: `toby-swd-testing`, which opens environment before the update.
Should not load: `toby-swd-environment`, which skips a snapshot update.

### P10 — module README
> Update the billing module README after the split.

```
Required: toby-voice
Forbidden: toby-swd-docs, toby-refactor
```

Should load: `toby-voice`, which opens docs.
Should not load: `toby-swd-docs`, which is hidden.

### P11 — optional parameter on a public function
> Add an optional `timeout` parameter to the public `fetchReport()` in the SDK.

```
Required: toby-build
Forbidden: toby-swd-interfaces, toby-optimize, toby-refactor
```

Should load: `toby-build`, which opens interfaces, errors, testing, and docs.
Should not load: `toby-swd-interfaces`, which is hidden.

### P12 — new endpoint
> Add a `POST /invites` endpoint that emails the invitee.

```
Required: toby-build
Forbidden: toby-swd-interfaces, toby-swd-experiment
```

Should load: `toby-build`, which opens strategy, interfaces, errors, and testing.
Should not load: `toby-swd-interfaces`, which is hidden.

### P13 — start the dev server
> Start the dev server so I can try the new button by hand.

```
Required: toby-swd-environment
Forbidden: toby-swd-experiment, toby-build
```

Should load: `toby-swd-environment`.
Should not load: `toby-swd-experiment`, which skips starting a server alone.

### P14 — slide deck
> Make a five-slide deck on the Q3 outage.

```
Required: toby-artifact-style
Forbidden: toby-explain
Optional: toby-voice
```

Should load: `toby-artifact-style`. The guide's voice line may load `toby-voice` too.
Should not load: `toby-explain`, which skips a deck.

### P15 — explanation with a diagram
> Explain how a TCP handshake works, with a diagram.

```
Required: toby-artifact-style
Forbidden: toby-explain, toby-learning
```

Should load: `toby-artifact-style`.
Should not load: `toby-explain`, which skips a diagram.

### P16 — walk me through
> Walk me through how B-tree indexes work.

```
Required: toby-explain
Forbidden: toby-learning
```

Should load: `toby-explain`.
Should not load: `toby-learning`, which is hidden.

### P17 — move helpers into a shared package
> Move the date helpers into a shared package and export `formatDate`.

```
Required: toby-refactor
Forbidden: toby-swd-modules, toby-swd-interfaces, toby-build
```

Should load: `toby-refactor`, which opens strategy, modules, and interfaces.
Should not load: `toby-swd-modules` or `toby-swd-interfaces`, which are hidden.

### P18 — placement question
> Should the retry helper go in `http/client.ts` or in each sync job?

```
Required: toby-explain
Forbidden: toby-refactor, toby-swd-modules, toby-swd-errors
```

Should load: `toby-explain`, which opens modules for the placement note.
Should not load: `toby-refactor`, which needs a request to change code.

### P19 — commit message
> Write the commit message for this change.

```
Required: toby-voice
Forbidden: toby-code-review
```

Should load: `toby-voice`.
Should not load: anything else. No other entry description lists a commit message.

### P20 — wrong total
> The checkout total is one cent off for discounted orders. Fix it.

```
Required: toby-bug-fix
Forbidden: toby-build, toby-swd-testing
```

Should load: `toby-bug-fix`, which opens testing.
Should not load: `toby-build`, which skips wrong output.

### P21 — 500 on input
> The login page returns a 500 when the email has a plus sign. Fix it.

```
Required: toby-bug-fix
Forbidden: toby-build, toby-swd-errors
```

Should load: `toby-bug-fix`, which opens testing and errors.
Should not load: `toby-build`, which skips wrong output.

### P22 — why a test fails
> Why does the orders test fail since yesterday's merge?

```
Required: toby-explain
Forbidden: toby-bug-fix, toby-swd-testing
```

Should load: `toby-explain`.
Should not load: `toby-bug-fix` or `toby-swd-testing`, which skip a why question about a failing test.

### P23 — flaky test
> Fix the flaky checkout test.

```
Required: toby-swd-testing
Forbidden: toby-bug-fix
```

Should load: `toby-swd-testing`.
Should not load: `toby-bug-fix`, which skips a flaky test.

### P24 — slow page
> The orders page takes 4 seconds to load. Make it faster.

```
Required: toby-optimize
Forbidden: toby-build, toby-bug-fix
```

Should load: `toby-optimize`, which opens environment for the benchmark.
Should not load: `toby-build` or `toby-bug-fix`, which skip slow code.

### P25 — cache question
> Should we put Redis in front of the product lookup?

```
Required: toby-explain
Forbidden: toby-optimize, toby-build
```

Should load: `toby-explain`, which opens `toby-optimize` for the cost question.
Should not load: `toby-optimize`, which skips a speed question with no change asked for.

## Over-triggering probes

### N1 — pure rename
> Rename `usr` to `user` everywhere in `src/auth/session.ts`. No other change.

```
Required: toby-refactor
Forbidden: toby-build, toby-swd-testing, toby-swd-strategy, toby-swd-clarity, toby-game, toby-squall
```

Should load: `toby-refactor`, which opens clarity.
Should not load: `toby-build`, which skips work where behavior stays the same.

### N2 — working-tree review
> Review my changes.

```
Required: toby-code-review
Forbidden: toby-refactor, toby-build, toby-swd-strategy, toby-game, toby-squall
```

Should load: `toby-code-review`, which opens a method skill when a finding depends on it.
Should not load: `toby-refactor`, which skips a request for findings.

### N3 — parameter spike
> Try a few values for the retry backoff and tell me which one stops the
> timeouts. Throwaway.

```
Required: toby-swd-experiment
Forbidden: toby-swd-testing, toby-swd-errors, toby-optimize, toby-bug-fix, toby-build, toby-game, toby-squall
```

Should load: `toby-swd-experiment`.
Should not load: `toby-optimize` or `toby-bug-fix`, which skip a throwaway. The word "throwaway" decides the route over retries and timeouts.

### N4 — single-file edit following a local pattern
> Add a `phone` field to the `ContactForm` component, the same way `email` is
> done two lines up.

```
Forbidden: toby-build, toby-refactor, toby-swd-interfaces, toby-swd-strategy, toby-swd-modules, toby-game, toby-squall
```

Should load: nothing.
Should not load: `toby-build`, which skips a one-file pattern copy.

### N5 — a game, asked for plainly
> Build me a browser game where you run a traffic intersection and it gets
> harder every wave. Single HTML file is fine.

```
Optional: toby-build
Forbidden: toby-game, toby-swd-experiment, toby-artifact-style
```

Should load: `toby-build`, or nothing.
Should not load: `toby-game`, which is hidden and loads only from `/toby-game`. `toby-artifact-style` skips a game.

### N6 — brainstorming, asked for plainly
> Help me brainstorm names for this service. Let's explore a few directions.

```
Forbidden: toby-squall, toby-build, toby-swd-strategy, toby-voice
```

Should load: nothing.
Should not load: `toby-squall`, which is hidden. `toby-voice` takes wording help only for a text.

### N7 — asking for a clear explanation
> In one or two sentences, clearly and concisely: what's the actual difference
> between a mutex and a semaphore?

```
Required: toby-explain
Forbidden: toby-swd-clarity, toby-learning, toby-swd-errors, toby-refactor
```

Should load: `toby-explain`.
Should not load: `toby-swd-clarity`, which is hidden. The words "clearly and concisely" describe the answer wanted.

## Scoring

`python3 evals/run.py compare triggering <file>` scores each run against the
directive lines. A skill in a Required line that did not fire is a miss. A
skill in a Forbidden line that fired is a false fire. The main score is the
total of false fires and misses, because each one loads a skill the task does
not need or skips one it does. N5 and N6 test two invoke-only skills,
`toby-game` and `toby-squall`, and a single firing there breaks a stated rule.
