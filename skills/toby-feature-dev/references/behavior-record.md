# The behavior record

The record is the file that says what the software was asked to do, in sentences a reader can check against a test. SKILL.md covers when an entry fires and the check that runs before the handoff. This file covers everything else. It covers the changes that write no entry, what an entry holds, the grep, retiring, and two branches that write the same sentence.

## What writes no entry

A behavior you inferred or a default you picked is a design decision. Design decisions are recorded in other places. A value or a unit goes in the interface comment that toby-swd-clarity covers. A cross-module or externally-forced constraint goes in AGENTS.md under toby-swd-docs.

Refactors, renames, performance work, internal helpers, error paths, and diagnostic or developer-facing output write no entry at all. A bug fix writes no entry either. It edits the sentence it just falsified, in the same diff that fixes the code.

## Home

The record goes in a prose file the repo already keeps for stated behavior, such as a spec directory or a decision-record tree. Do not use AGENTS.md or README.md. toby-swd-docs puts one of each per module root, so a behavior spanning two roots would be split across files.

When no such file exists, propose `docs/behavior.md` and get a yes before creating it. Open it with the preamble in `examples.md`, so the next reader knows what the file contains before the first heading. After that, append entries without asking. Never backfill behavior this change doesn't touch.

## The entry

An entry is a heading that states the behavior in one sentence, plus who asked, quoted, and when.

- The sentence gives the trigger and the observable result, written at the public interface toby-swd-testing tests through.
- It mentions no function, no file, no internal state. Somebody who has never opened this repo can still tell whether the software does what the sentence says.
- Two sentences means two behaviors, so split them.
- Give entries no IDs. The sentence is the identifier. A sentence that needs an ID to be found is too vague to audit.
- The quote gives the exact words from the user's message or the ticket line, with the date they were said.

## The binding

The test description quotes the sentence verbatim: a docstring, an `it(...)` string, a `t.Run` name, whatever the harness reads. Verbatim means character for character, because the check is a fixed-string grep. The grep treats a helpfully reworded sentence as a missing test.

## The check

Before the handoff, check that every heading appears verbatim in a test.

```sh
grep '^## ' docs/behavior.md | sed 's/^## //' | while read -r b; do
  git grep -qF -- "$b" '*test*' '*spec*' || echo "unproven: $b"
done
```

The path and the two globs are placeholders. Point them at the file this repo keeps and the directories containing its tests, then quote the command you ran.

A run with nothing to report prints nothing. Every line it does print is a stated behavior that has no test. Either the behavior was stated and never proved, or someone deleted the test and left the requirement with no check. Report both cases in the handoff. A heading with a hit proves only that the sentence was pasted into a description. You still have to check that the test body asserts it.

## Retiring

Move the entry under a trailing `## Retired` heading, with the date and why, in the diff that deletes the test. An entry above that heading is a current claim. An entry below it is a past claim with an end date and a reason. Do not delete an entry outright, because the sentence that stopped being true is the only remaining record of what somebody once wanted.

## Two branches, one sentence

The heading is the identifier, so there is nothing to allocate, increment, or collide on. Two branches that wrote the same sentence wrote the same behavior. The merge conflict between them is the correct outcome. One of them is a duplicate, or the two sentences differ in a way somebody has to settle.

A filled record, its preamble, its bindings, and a retired entry are in `examples.md`.
