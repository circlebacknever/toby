# Toby Artifact copy

Load this file when writing substantive copy for a Toby Artifact Style artifact: headings, paragraphs, captions, callouts, button text, and microcopy. Toby's global voice rules control register. This file covers evidence, units, claim structure, and artifact-copy discipline.

## The four tests

Every sentence must pass the first three tests. The fourth test is applied afterward, and a sentence that fails it is cut.

### 1. Cite test
Every claim, number, or comparison links to a source, a measurement, or a mechanism.

- Pass: "Median p95 latency dropped from 312 ms to 184 ms after the cache layer merged (commit 4f8c2a)."
- Fail: "Performance improved significantly."

### 2. Negation test
Write the negation of the claim. If nobody would write that negation, the original claim is empty.

- Fail: "The method is fast, reliable, and well-designed." Negation: "The method is slow, fragile, and arbitrary." Nobody writes that negation, so the original is empty.
- Pass: "The method runs in O(n log n) for n ≤ 10⁶." The negation is a real claim someone could dispute.

### 3. Substitution test
Replace the subject with an unrelated noun. If the sentence still makes sense, it does not describe its subject.

- Fail: "This dashboard unlocks new possibilities." Substitute: "This stapler unlocks new possibilities." The sentence still makes sense, so the original is meaningless.
- Pass: "This dashboard shows alerts where p95 exceeds 200 ms." Substituting "stapler" makes the sentence nonsense, so the original is meaningful.

### 4. Reader-skim cut
Apply this cut after the first three tests pass. If a reader who already knows the material can skip the sentence and lose nothing, cut the sentence. Do not restate the obvious.

---

## Sentence structure

Do not invent contrasts, because `It's not X, it's Y` is filler whenever nobody claimed X. Write the positive form.

A comparison of two options that both exist counts as content. A comparison table, a rejected-alternative callout, and a "chose A over B because C" caption all name a real option, so they ship. The operating guide states the full rule.

---

## Where the word list lives

The operating guide contains the one banned-word list, with the replacement for each entry. It is always loaded, so the list is already in context. This file does not add or repeat any entry from that list.

---

## Patterns to remove wherever they appear

### Adjective stacks describing the work
`powerful` `intuitive` `seamless` `beautifully simple` `elegant` `game-changing` `delightful` `polished` `refined` `robust` `modern` `sleek`

### Throat-clearing openers
`in today's fast-paced world` `we all know` `let's dive in` `it's no secret` `at the end of the day` `when it comes to`

### Self-praise of the writing
`cleanly` `clearly` `honestly` `no fluff` `in plain English` `just the facts` `simply put` `in a nutshell`

The reader can judge the writing. Praising the writing puts a claim about the evidence in place of the evidence.

### Reader-state assertions
`you'll love` `you'll wonder how you ever` `you'll be amazed` `you'll find that`

### Vague magnitude
`a lot of` `many` `huge` `massive` `tons of` `plenty of` `quite a few`

Replace each one with a number or a range, or delete it.

### Hype suffixes
`the right way` `done right` `in a beautiful way` `that just works` `made simple` `reimagined`

### Inflated verbs
`unlock` `transform` `supercharge` `revolutionize` `harness` `empower` `elevate` `accelerate` `streamline`

### Mission-stating
`on a mission to` `dedicated to` `passionate about` `committed to` `devoted to`

---

## Qualification rules

Match the qualifier to what is known about the claim. Don't hedge a known claim or strip a qualifier from an uncertain one.

- **Known** → state the claim plainly, with no hedge.
- **Approximate or bounded** → state the approximation or bound, such as "~150 ms", "between 0.4 and 0.6", or "lower bound of 12".
- **Uncertain by amount** → pair the value with an interval, such as `0.73 ± 0.08, 95% CI` or `42 ± 3 ms (n=120)`.
- **Unknown or open** → say so in a sentence, such as "Nobody has measured the cold-start time."

---

## Hard rules

**Slide and chart titles state the claim.** Write the title as a plain, descriptive sentence, and use the body to explain, qualify, or show the work. "Cache reduces p95 by 41%" passes as a title, and "Performance" fails. A section heading in a document is a one- or two-word label, such as "Casing", or a phrase that says what the section covers. Neither one is a slogan, so leave out mirrored phrasing, clever claims, and any subtitle that restates the title.

**Put each caveat next to the claim it qualifies.** Never put uncertainty in a footnote.

**Every value gets a unit.** A bare `312` is a defect, but `312 ms` is correct.

**State assumptions explicitly.** When a conclusion depends on an assumption, write the assumption as a sentence next to the conclusion, such as "This estimate assumes the traffic mix from May."

**The clarity rules apply most strictly to labels.** An axis title, a legend entry, a KPI caption, a table header, and a slide heading are each subject to the three-word cap on noun stacks. `user session token refresh failures` stacks five words, so it becomes `failed token refreshes`. When the stack cannot be shortened, name the relation with a preposition: `resistance at the light connection`.

**Use one name for each thing across the whole artifact.** A series called `p95 latency` in the chart is `p95 latency` in the legend, the caption, and the summary slide. A renamed series reads as a second series.

**A decision is a whole sentence that names the action and its reason.** "Approve the controlled release, because both meters stayed inside the watch band." A button label can be the verb alone, such as Approve or Hold.

**Do not use first person** (we, I, our). **Do not use second person** (you, your) in most reference contexts.

**Do not use emoji or exclamation points.**

---

## Casing

- Use UPPERCASE eyebrows (tracked +0.12em) for section labels.
- Use sentence case for headings and body, and never use Title Case.
- Write tokens in all-lowercase: `$toby-paper`, `--toby-ink`.
- Set values, IDs, and coordinates in mono: `312 ms`, `R-04.2`, `34.05° N`.

---

## Marketing layouts

Layouts with a hero, feature cards, and a CTA are allowed, but the copy inside them must not be promotional.

- **Hero headline:** state what the thing does. "This tool models p95 latency under burst load." passes. "Built for performance you'll love" fails.
- **Feature card:** give a concrete behavior and the measurement that backs it. "In a test at 10⁴ events per second, the monitor detected a threshold breach within 50 ms."
- **CTA verb:** name the next step. "Read the derivation." "Open the worked example." "Run the benchmark." Never write `Get started.` or `Start your journey.`
- Testimonials, social-proof counts, and "as seen in" rows are not allowed unless the artifact exists to show those sources.

---

## Toby voice boundary

The global voice rules apply to artifact copy. This reference adds artifact constraints: the claim in the slide or chart title, units on values, citations beside claims, and no marketing copy.

**Artifact copy stays evidence-led:**
- Numbers have units, claims cite a source or mechanism, and slide and chart titles state the conclusion.
- Use no marketing adjectives, throat-clearing, reader-state assertions, or invented contrasts.
- A reference deck that teaches a concept keeps a serious tone when the concept requires one.

**Where lighter phrasing is allowed:**
- **Identifiers can be long and specific.** `priceIncludingCheckoutFee` ships if that is what the field holds.
- **State what nobody understands yet.** "The drop appeared in three independent runs, but nobody knows the cause yet." gives the reader more than a confident theory.
- **State when a judgment is based on taste.** "This looks wrong to me, because it resembles the cache-coherence bug from M-03." is a valid note in an investigation artifact.
- **Keep lighter phrasing out of the data.** A slide heading can be a plain sentence. An axis label, a KPI value, and a legend entry show only the quantity the reader came for.

**The override.** When the user explicitly asks for a different register ("write this as a formal letter," "keep it strictly clinical"), follow that register.

---

## Worked example: revising a paragraph

### Before
> Our powerful new dashboard delivers blazing-fast insights at scale, empowering you to unlock the full potential of your data. Built on a robust, modern stack, it's the dashboard you've always wanted.

The paragraph fails all four tests, because it uses an adjective stack, inflated verbs, a reader-state assertion, vague magnitude, and mission-stating.

### After
> The dashboard shows an alert when p95 latency stays above 200 ms for 60 seconds. It samples latency once per second. The data comes from production traces for the last 30 days, about 2.6 million requests.

The revision names the mechanism, threshold, sampling rate, source, and sample size. Every value has a unit. Its slide title would state the claim: "The dashboard alerts when p95 latency passes 200 ms."
