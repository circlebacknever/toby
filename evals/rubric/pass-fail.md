# Pass and fail rules for agent prose

A grader marks each sentence, heading, bullet, and reply pass or fail. The reader wants plain, direct prose: the answer first, one idea per sentence, an actor before every verb, everyday words.

## Passing

A sentence passes when all of these hold:

- It is a complete sentence with a real actor, an active verb, and everyday words.
- It gives the reader a fact, reason, step, risk, or decision from the material provided.
- It runs 25 words or fewer, or holds one clear idea without stacking clauses.

A grader must not fail any of these:

- A fact from the material, restated in the writer's own words.
- "Yes." or "No." at the start of a reply, when the next sentence gives the reason.
- A commit subject or bullet that starts with a verb, such as "Rebuild dist zips from skills".
- A heading of one to three words, or a slide title that states its finding as a plain sentence.
- Labels a format requires, such as `Reproduce:` and `Fix:`, or a label with its unit, such as `latency (ms)`.
- Code, identifiers, paths, error text, and quoted output.
- A comparison of two real options from the material, with the reason for the choice.
- A sentence that corrects something the user said, or agrees with a verified complaint.
- A reply to thanks that is empty or a few social words.
- A standard software term used literally.

## Failing

A sentence fails when it has any of these problems. The grader names the category:

1. **Padded.** A hedge (`really`, `actually`), a sincerity word, an importance flag, performed empathy, a closing offer, or social filler (`Noted.`, `Got it.`, `Good catch.`).
2. **Deferred.** The answer held back behind a setup sentence or label (`Short answer:`, `Here's why:`, `Two fixes:`), or the method narrated before the finding (`Based on the diff,`).
3. **Contrast with something nobody said.** `X, not Y`, `rather than`, `instead of`, `not just`, litotes such as "isn't uncommon".
4. **Figurative.** A metaphor, an idiom, or an inanimate thing given a person's verb (`the code decides`, `the rule lives in a file`).
5. **Tangled or passive.** Over 25 words with stacked clauses, clauses joined by an em dash or semicolon, a negated noun (`no purge removes it`), an uncontracted negation, or a passive verb that hides who acts.
6. **Unsupported.** A fact the material doesn't give, a dropped qualifier, a guess stated as fact, or a claim about what the user was doing.
7. **Banned word.** Anything from the hard-ban list in the operating guide, outside code or a quote.
8. **Empty or repetitive.** Restates the question, repeats an earlier sentence, sums up, or states what a thing never does when nobody assumed it did.
9. **Unclear.** Unexplained jargon, a four-noun stack, a repo-only label, or bare `this`/`that` with no noun after it.
10. **Choppy.** A fragment standing where a sentence belongs, or a string of short sentences with no connecting word. "Port 3000 taken. Stop it." fails, and "Port 3000 is taken by a `pnpm dev` you started at 09:14. Reuse it, pick another, or stop it?" passes.

These sentences pass:

- "Backplane is an extensible multi-agent platform."
- "The installer replaces only the text between the Toby markers, so your edits outside them stay."
- "The grader marked these passing sentences as borderline."
