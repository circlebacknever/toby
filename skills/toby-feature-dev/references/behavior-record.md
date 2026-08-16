# The behavior record

The record is the file that says what the software was asked to do, in sentences a reader can check against a test. SKILL.md owns when an entry fires and the check that runs before the handoff. This file owns the rest: what writes no entry, what an entry holds, the grep, retiring, and what happens when two branches write the same sentence.

## What writes no entry

A behavior you inferred or a default you picked is a design decision, and design decisions have other homes. A value or a unit goes in the interface comment toby-swd-clarity owns, and a cross-module or externally-forced constraint goes in AGENTS.md under toby-swd-docs.

These write nothing at all — refactors, renames, performance work, internal helpers, error paths, and diagnostic or developer-facing output. A bug fix writes no entry either. It edits the sentence it just falsified, in the same diff that fixes the code.

## Home

A prose file the repo already keeps for stated behavior — a spec directory, a decision-record tree. AGENTS.md and README.md are out, because toby-swd-docs puts one of each per module root, and behavior spanning roots would split. With nothing present, propose `docs/behavior.md` and get a yes before creating it. Open it with the preamble in `examples.md`, so the next reader knows what they hold before the first heading. Appends after that need no asking. Never backfill behavior this change doesn't touch.

## The entry

A heading holding the behavior in one sentence, plus who asked, quoted, and when.

- One sentence, trigger plus observable result, written at the public interface toby-swd-testing tests through.
- It names no function, no file, no internal state. Somebody who has never opened this repo can still tell whether the software does this.
- Two sentences means two behaviors. Split them.
- No IDs. The sentence is the identifier, and a sentence needing an ID to be findable was too vague to audit.
- The quote is the words that were used — the user's message or the ticket line — with the date they were said.

## The binding

The test description quotes the sentence verbatim: a docstring, an `it(...)` string, a `t.Run` name, whatever the harness reads. Verbatim means character for character, because the check is a fixed-string grep and a helpfully reworded sentence reads to it as a missing test.

## The check

Before the handoff, every heading appears verbatim in a test.

```sh
grep '^## ' docs/behavior.md | sed 's/^## //' | while read -r b; do
  git grep -qF -- "$b" '*test*' '*spec*' || echo "unproven: $b"
done
```

The path and the two globs are placeholders. Point them at the file this repo keeps and the directories its tests live in, then quote the command you ran.

A run with nothing to report prints nothing. Every line it does print is a sentence the product claims and no test defends. Either the behavior was stated and never proved, or the test was deleted and took the requirement with it. Both go in the handoff. A heading with a hit proves the sentence was pasted into a description. Whether the body asserts it is on you.

## Retiring

Move the entry under a trailing `## Retired` heading, with the date and why, in the diff that deletes the test. An entry above that heading is a live claim. An entry below it is a claim with an end date and a reason. Nothing gets deleted outright, because the sentence that stopped being true is the only surviving record of what somebody once wanted.

## Two branches, one sentence

The heading is the identifier, so there is nothing to allocate, increment, or collide on. Two branches that wrote the same sentence wrote the same behavior, and the merge conflict is the correct outcome. One of them is a duplicate, or the two sentences differ in a way somebody has to settle.

A filled record, its preamble, its bindings, and a retired entry are in `examples.md`.
