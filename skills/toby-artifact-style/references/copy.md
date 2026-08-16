# Toby Artifact copy

Load this file when writing substantive copy for a Toby Artifact Style artifact: headings, paragraphs, captions, callouts, button text, and microcopy. Global Toby voice controls register. This file controls evidence, units, claim structure, and artifact-copy discipline.

## The four tests

The first three are pass-tests. Every sentence must pass all three. The fourth is a cut-test applied afterward.

### 1. Cite test
Every claim, number, or comparison links to a source, a measurement, or a mechanism.

- Pass: "Median p95 latency dropped from 312 ms to 184 ms after the cache layer landed (commit 4f8c2a)."
- Fail: "Performance improved significantly."

### 2. Negation test
Flip the claim. If the negation is something nobody would write, the original says nothing.

- Fail: "The method is fast, reliable, and well-designed." Negation: "The method is slow, fragile, and arbitrary." Nobody writes that negation → the original is empty.
- Pass: "The method runs in O(n log n) for n ≤ 10⁶." The negation is a real claim someone could dispute.

### 3. Substitution test
Replace the subject with an unrelated noun. If the sentence still works, it isn't about anything.

- Fail: "This dashboard unlocks new possibilities." Substitute: "This stapler unlocks new possibilities." Still works → meaningless.
- Pass: "This dashboard surfaces alerts where p95 exceeds 200 ms." Substitute "stapler" — breaks immediately → meaningful.

### 4. Reader-skim cut
Applied after the first three pass. A reader who already knows the material skims past with nothing lost, so the sentence comes out. Do not restate the obvious.

---

## Sentence structure

Do not invent foils. `It's not X, it's Y` is filler whenever nobody claimed X. Write the positive form.

Comparing two options that both exist is content. A comparison table, a rejected-alternative callout, and a "chose A over B because C" caption all name a real option, so they ship. `base/toby.md` carries the full rule.

---

## Where the word list lives

`base/toby.md` carries the one banned-word list, with the replacement move for each entry. This file adds none and repeats none.

---

## Patterns to remove on sight

### Adjective stacks describing the work
`powerful` `intuitive` `seamless` `beautifully simple` `elegant` `game-changing` `delightful` `polished` `refined` `robust` `modern` `sleek`

### Throat-clearing openers
`in today's fast-paced world` `we all know` `let's dive in` `it's no secret` `at the end of the day` `when it comes to`

### Self-praise of the writing
`cleanly` `clearly` `honestly` `no fluff` `in plain English` `just the facts` `simply put` `in a nutshell`

The reader can see whether the writing holds up. Saying so replaces the evidence with a claim about the evidence.

### Reader-state assertions
`you'll love` `you'll wonder how you ever` `you'll be amazed` `you'll find that`

### Vague magnitude
`a lot of` `many` `huge` `massive` `tons of` `plenty of` `quite a few`

Replace with a number, a range, or omit.

### Hype suffixes
`the right way` `done right` `in a beautiful way` `that just works` `made simple` `reimagined`

### Inflated verbs
`unlock` `transform` `supercharge` `revolutionize` `harness` `empower` `elevate` `accelerate` `streamline`

### Mission-stating
`on a mission to` `dedicated to` `passionate about` `committed to` `devoted to`

---

## Qualification rules

Match the qualifier to the epistemic state. Don't hedge a known claim or strip a qualifier from an uncertain one.

- **Known** → state plainly, no hedge.
- **Approximate or bounded** → state the approximation or bound. "~150 ms", "between 0.4 and 0.6", "lower bound of 12".
- **Uncertain by amount** → pair value with interval. `0.73 ± 0.08, 95% CI`. `42 ± 3 ms (n=120)`.
- **Unknown or open** → say so. "Unknown." "Not measured." "Open question."

---

## Hard rules

**Headings carry the claim.** State the conclusion in the heading. The body explains, qualifies, or shows the work. "Cache reduces p95 by 41%" is a heading. "Performance" is not.

**Caveats sit next to the claim they qualify.** Never push uncertainty into a footnote.

**Every value gets a unit.** `312` is a defect. `312 ms` is correct.

**State assumptions explicitly.** Use `Known:` / `Unknown:` / `Baseline assumes …` labels when the assumption is doing work.

**Labels get the clarity floor at its tightest.** An axis title, a legend entry, a KPI caption, a table header, and a slide heading each carry the three-word cap on noun stacks. `user session token refresh failures` stacks five words, so it becomes `failed token refreshes`. Where the stack will not compress, name the relation with a preposition: `resistance at the light connection`.

**One name per thing, held across the whole artifact.** A series called `p95 latency` in the chart is `p95 latency` in the legend, the caption, and the summary slide. A renamed series reads as a second series.

**Decisions are imperative and short.** "Approve controlled release." "Hold." "File." "Escalate."

**No first person** (we, I, our). **No second person** (you, your) in most reference contexts.

**No emoji. No exclamation points.**

---

## Casing

- UPPERCASE eyebrows (tracked +0.12em) for section labels.
- Sentence case for headings and body. Never Title Case.
- All-lowercase for tokens: `$toby-paper`, `--toby-ink`.
- Mono for values, IDs, coordinates: `312 ms`, `R-04.2`, `34.05° N`.

---

## Marketing-shaped layouts

Hero + feature cards + CTA shapes are allowed. The copy inside is not promotional.

- **Hero headline** = what the thing does. "Models p95 latency under burst load" passes. "Built for performance you'll love" fails.
- **Feature card** = a concrete behavior + the measurement that backs it. "Detects threshold breach within 50 ms. Tested at n = 10⁴ events/sec."
- **CTA verb** = the actual next step. "Read the derivation." "Open the worked example." "Run the benchmark." Never `Get started.` Never `Start your journey.`
- Testimonials, social-proof counts, and "as seen in" rows are out unless the artifact's purpose is to surface those sources.

---

## Toby voice boundary

Global Toby voice carries into artifact copy. This reference adds artifact constraints: claim in heading, units on values, citations beside claims, and no marketing copy.

**Artifact copy stays evidence-led:**
- Numbers carry units. Claims cite a source or mechanism. Headings state the conclusion.
- No marketing adjectives. No throat-clearing. No reader-state assertions. No invented foils.
- Reference decks teaching a concept stay sober when the concept needs sobriety.

**Where Toby voice has room:**
- **Dry humor can land when it exposes a detail.** A closing slide reading "Bound orbits are ellipses. The rest is detail." carries dry weight without breaking the frame.
- **Identifiers can be weird if they are accurate.** `revengeOfTheRetryLoop` ships if that is what the function does.
- **Admitted confusion is useful when labeled.** A caveat reading "Mechanism observed in three independent runs, cause unknown" beats a confident-sounding theory.
- **Taste calls need labels.** A note reading "Smells wrong, and it resembles the cache-coherence bug from M-03" is a valid signal in an investigation artifact.
- **The joke never goes in the number.** A slide heading can carry a line. An axis label, a KPI value, and a legend entry carry the quantity the reader came for.

**The override.** When the user explicitly asks for a different register ("write this as a formal letter," "no jokes here," "keep it strictly clinical"), follow that register.

---

## Worked example: revising a paragraph

### Before
> Our powerful new dashboard delivers blazing-fast insights at scale, empowering you to unlock the full potential of your data. Built on a robust, modern stack, it's the dashboard you've always wanted.

Fails all four tests. Adjective stack, inflated verbs, reader-state assertion, vague magnitude, mission-stating.

### After
> Dashboard surfaces alerts when p95 latency exceeds 200 ms over a 60-second window. Sampled at 1 Hz. Sources: production traces (last 30 days, n ≈ 2.6M requests).

Cites mechanism, threshold, sampling rate, source, sample size. Every value has a unit. Heading would be the claim: "Surfaces p95 breaches > 200 ms."
