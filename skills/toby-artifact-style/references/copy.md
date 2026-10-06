# Toby Artifact copy

This file gives an example for each copy test, the qualifier rules, and the rules for marketing layouts.

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

A comparison of two options that both exist counts as content. Keep a comparison table, a rejected-alternative callout, or a "chose A over B because C" caption, because each refers to a real option.

Marketing adjectives, inflated verbs, mission statements, and vague amounts such as `a lot of` fail the cite, negation, or substitution test. Replace each with a number, a mechanism, or a measurement.

---

## Qualification rules

Match the qualifier to what is known about the claim. Don't hedge a known claim or strip a qualifier from an uncertain one.

- **Known** → state the claim plainly, with no hedge.
- **Approximate or bounded** → state the approximation or bound, such as "~150 ms", "between 0.4 and 0.6", or "lower bound of 12".
- **Uncertain by amount** → pair the value with an interval, such as `0.73 ± 0.08, 95% CI` or `42 ± 3 ms (n=120)`.
- **Unknown or open** → say so in a sentence, such as "Nobody has measured the cold-start time."

---

## Hard rules

**A subtitle never restates the title.** Leave mirrored phrasing and clever claims out of titles and headings.

**A decision is a whole sentence that states the action and its reason.** "Approve the controlled release, because both meters stayed inside the watch band." A button label can be the verb alone, such as Approve or Hold.

**Do not use first or second person in artifact copy**, except in a note that says a judgment depends on taste, such as "This looks wrong to me, because it resembles the cache-coherence bug from M-03."

**Do not use exclamation points.**

---

## Marketing layouts

Layouts with a hero, feature cards, and a CTA are allowed, but the copy inside them must not be promotional.

- **Hero headline:** state what the thing does. "This tool models p95 latency under burst load." passes. "Built for performance you'll love" fails.
- **Feature card:** give a concrete behavior and the measurement that backs it. "In a test at 10⁴ events per second, the monitor detected a threshold breach within 50 ms."
- **CTA verb:** state the next step. "Read the derivation." "Open the worked example." "Run the benchmark." Never write `Get started.` or `Start your journey.`
- Testimonials, social-proof counts, and "as seen in" rows are not allowed unless the artifact exists to show those sources.

---

## Worked example: revising a paragraph

### Before
> Our powerful new dashboard delivers blazing-fast insights at scale, empowering you to unlock the full potential of your data. Built on a robust, modern stack, it's the dashboard you've always wanted.

The paragraph fails all four tests, because it uses an adjective stack, inflated verbs, a reader-state assertion, vague magnitude, and mission-stating.

### After
> The dashboard shows an alert when p95 latency stays above 200 ms for 60 seconds. It samples latency once per second. The data comes from production traces for the last 30 days, about 2.6 million requests.

The revision states the mechanism, threshold, sampling rate, source, and sample size. Every value has a unit. Its slide title would state the claim: "The dashboard alerts when p95 latency passes 200 ms."
