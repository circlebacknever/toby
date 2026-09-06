# Trigger scenarios

Ten prompts. Each names the skills that should load and the skills that must
not. A skill that fires when it should not costs 100 percent of its tokens, so
the four probes at the end carry as much weight as the four positives.

The runner shows an agent the nine `toby-swd-*` descriptions plus
`toby-feature-dev`, `toby-code-review`, and `toby-simplify-code`, then asks
which it would load. Descriptions are the whole test surface, because that is
all a host tool sees before it decides.

## Positive probes

### P1 — repository method with a cache and an error path
> Add a `getAccountBalance(userId)` method to `AccountRepository`. It should read
> from the Redis cache first, fall back to Postgres, and return null when the
> account is missing.

```
Required: toby-swd-interfaces, toby-swd-complexity, toby-swd-testing
Forbidden: toby-swd-docs, toby-swd-experiment, toby-swd-environment, toby-game, toby-squall
```

Should load: `toby-swd-interfaces`, `toby-swd-complexity`, `toby-swd-testing`.
Should not load: `toby-swd-docs`, `toby-swd-experiment`, `toby-swd-environment`.
Owns the decision: interfaces. The callable surface is the thing being designed.

### P2 — split a module
> `src/billing/invoice.ts` is 1,400 lines and handles invoice generation, PDF
> rendering, and the dunning emails. Split it.

```
Required: toby-swd-modules, toby-swd-strategy, toby-swd-docs
Forbidden: toby-swd-experiment, toby-game, toby-squall
```

Should load: `toby-swd-modules`, `toby-swd-strategy`, `toby-swd-docs`.
Should not load: `toby-swd-experiment`, `toby-swd-clarity`.
Owns the decision: modules.

### P3 — feature request
> Build the CSV export for the reports page. Users pick a date range and get a
> download.

```
Required: toby-feature-dev
Forbidden: toby-simplify-code, toby-code-review, toby-game, toby-squall
```

Should load: `toby-feature-dev`, and whatever it routes to per step.
Should not load: `toby-simplify-code`, `toby-code-review`.
Owns the decision: feature-dev.

### P4 — migration and a seed script
> Run the pending migration against my local database and re-seed it.

```
Required: toby-swd-environment
Forbidden: toby-swd-strategy, toby-swd-modules, toby-swd-interfaces, toby-swd-testing, toby-game, toby-squall
```

Should load: `toby-swd-environment`.
Should not load: `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`,
`toby-swd-testing`.
Owns the decision: environment.

## Over-triggering probes

### N1 — pure rename
> Rename `usr` to `user` everywhere in `src/auth/session.ts`. No other change.

```
Required: toby-swd-clarity
Forbidden: toby-swd-strategy, toby-swd-testing, toby-swd-modules, toby-swd-interfaces, toby-feature-dev, toby-game, toby-squall
```

Should load: `toby-swd-clarity`.
Should not load: anything else. Strategy names this case in its own skip clause.

### N2 — working-tree review
> Review my changes.

```
Exactly one of: toby-code-review, toby-simplify-code
Forbidden: toby-swd-strategy, toby-feature-dev, toby-game, toby-squall
```

Should load: exactly one of `toby-code-review` or `toby-simplify-code`.
Should not load: both. They collide today and neither names the other.
Owns the decision: code-review, because "review" is the word in the prompt.

### N3 — parameter spike
> Try a few values for the retry backoff and tell me which one stops the
> timeouts. Throwaway.

```
Required: toby-swd-experiment
Forbidden: toby-swd-testing, toby-swd-strategy, toby-swd-complexity, toby-feature-dev, toby-game, toby-squall
```

Should load: `toby-swd-experiment`.
Should not load: `toby-swd-testing`, `toby-swd-strategy`, `toby-swd-complexity`.
Retries and timeouts are complexity nouns, and the throwaway frame outranks them.

### N4 — single-file edit following a local pattern
> Add a `phone` field to the `ContactForm` component, the same way `email` is
> done two lines up.

```
Optional: toby-swd-clarity
Forbidden: toby-feature-dev, toby-swd-interfaces, toby-swd-strategy, toby-swd-modules, toby-game, toby-squall
```

Should load: nothing, or `toby-swd-clarity` at most.
Should not load: `toby-feature-dev`, `toby-swd-interfaces`, `toby-swd-strategy`.
Feature-dev names this case in its own skip clause.

### N5 — a game, asked for plainly
> Build me a browser game where you run a traffic intersection and it gets
> harder every wave. Single HTML file is fine.

```
Optional: toby-feature-dev
Forbidden: toby-game, toby-swd-experiment, toby-artifact-style
```

Should load: `toby-feature-dev`, or nothing.
Should not load: `toby-game`. It fires only when the user names it or types
`/toby-game`, and this prompt names every noun in its description without
naming the skill.

### N6 — brainstorming, asked for plainly
> Help me brainstorm names for this service. Let's explore a few directions.

```
Forbidden: toby-squall, toby-feature-dev, toby-swd-strategy
```

Should load: nothing.
Should not load: `toby-squall`. Its description quotes this exact phrasing as a
case that must not fire it.

## Scoring

Per scenario: one point for every should-load skill that fired, minus one for
every should-not-load skill that fired. Eight scenarios, so the ceiling moves
with the expected sets. The number that matters is the total of false firings
across N1 to N6, because that is the co-load bill. N5 and N6 are the two
invoke-only skills. A single firing there is a defect. The other probes cost tokens, and these two break a stated rule.
