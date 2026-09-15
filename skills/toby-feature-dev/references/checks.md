# Catalogs

toby-feature-dev checks work against the don't-build catalog and the red-flag list. Use the don't-build catalog while scope is still being fixed. Check finished work against the red-flag list before the handoff. SKILL.md covers when each fires and what the report has to say. This file defines the entries and their names, so a handoff can cite one in three words and a reader can come look it up.

## Don't build — seven entries

Each stays out unless a criterion names it and that criterion's Source line quotes the user or the ticket. Never write a criterion to allow one of these, because the catalog is there to prevent that. When one ships anyway, name the entry and the criterion that allowed it.

- **The one-caller config option** is a setting, hook, or extension point that exactly one call site reads. A slice flag ships with the slice that deletes it, but this option ships with a default. Its value is `true` today and stays `true` until the repo is archived.
- **The wrapper over one instance** is a new module, layer, or adapter in front of a single implementation. Widen the interface you already have per toby-swd-interfaces and wait for a second instance, because a second instance shows you the pattern.
- **Handling for a ruled-out condition** is error handling for a state that the types or an earlier check already exclude. A catch block that has never caught anything does no more than a comment would, but it still costs time at runtime.
- **The adjacent feature, and the adjacent bug** are the thing the request implies and the defect you found on the way to it. Changes made "while I was in there" turn a two-file diff into a nine-file diff. Name each as a follow-up and stop. The one exception is toby-swd-strategy's reactive pass. It allows a small local cleanup inside a file a criterion already named, reported on its own line.
- **The uninvited migration** is a migration, rename, or reorganization that no criterion asked for. It appears unrequested in somebody else's review, so the reviewer has to decide whether to trust it.
- **Faster than nothing** is performance work with no measurement behind it. Without a starting measurement, a claim such as 40% faster has no recorded number to compare against.
- **The dependency nobody approved** is a new dependency added without approval. Adding it makes a decision for the user about their lockfile, build, and security review.

## Red flags — eight entries

Check the finished work against all eight before writing the handoff. Every one that fired goes in the handoff at file:line under its entry name, including the ones fixed on the spot.

- **The check that never entered the file** is a criterion reported met by a command that never reached the changed lines, or a test that has only ever passed.
- **Code nothing reaches** means the unit tests are green, but the route was never registered.
- **The unvisited call site** means a signature changed and nobody swept its callers. It also covers an external symbol called with no installed source opened and no existing call site cited.
- **The third-hour criterion** is a criterion that got smaller during a time when it was not reread, or a design decision made silently because asking felt slow.
- **Code ahead of its plan** is an edit written before the step covering it was approved. It also covers a step that ran differently from its approved wording with no edit to the plan.
- **The placeholder in a production path** is a TODO, a hardcoded return in place of real work, an unimplemented branch, a swallowed error, or a fixture the runtime reads.
- **Partial work reported whole** is a multi-slice feature handed over as done, with the remaining work moved to a closing note that begins "the rest is just wiring".
- **Nothing accounts for it** is a file in the diff that traces to no criterion and no reported cleanup. It also covers a user-quoted behavior with no record entry, a record entry no test quotes, and an assumption stated mid-run but missing from the handoff.

## Process failure modes — cited from the body

- **Layer cut.** A layer cut is a slice named for a layer, when it should be named for what a person can do. "The data layer" fails the slice conditions twice. Its only demo is a passing test suite. The thing the user asked for needs three more diffs. Re-cut to an entry point a user reaches.
- **Stop inflation.** Stop inflation is a checkpoint at every slice boundary, whether or not a decision is waiting there. Six stops on a six-slice feature give the user nothing to decide at most of them. At a boundary with no open question, write three lines and continue.
- **Plan ceremony.** Plan ceremony is a plan file written for a four-line change. For one-slice tactical work, keep the criteria list in chat.
