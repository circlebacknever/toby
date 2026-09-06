# Catalogs

Two lists toby-feature-dev checks work against. The don't-build catalog runs while scope is still being fixed. The red-flag list runs against finished work, before the handoff. SKILL.md owns when each fires and what the report has to say. This file owns the entries and their names, so a handoff can cite one in three words and a reader can come look it up.

## Don't build — seven shapes

Each stays out unless a criterion names it and that criterion's Source line quotes the user or the ticket. Never write a criterion to license one of these, which is what the catalog exists to stop. When one ships anyway, name the entry and the criterion that carried it.

- **The one-caller config option** — a setting, hook, or extension point exactly one call site reads. A slice flag ships with the slice that deletes it. This one ships with a default. It is set to `true` today and it will be set to `true` when the repo is archived.
- **The wrapper over one instance** — a new module, layer, or adapter standing in front of a single implementation. The second instance is what tells you the shape. Widen the surface you already have per toby-swd-interfaces and wait for it.
- **Handling for a ruled-out condition** — error handling for a state the types or an earlier check already exclude. A catch block that has never caught anything is a comment with a runtime cost.
- **The adjacent feature, and the adjacent bug** — the thing the request implies, and the defect you found on the way to it. "While I was in there" is how a two-file diff becomes a nine-file diff. Name each as a follow-up and stop. The one exception is toby-swd-strategy's reactive pass: a small local cleanup inside a file a criterion already named, reported on its own line.
- **The uninvited migration** — a migration, rename, or reorganization no criterion asked for. It arrives as free work in somebody else's review, and they have to decide whether to trust it.
- **Faster than nothing** — performance work with no measurement behind it. It is now 40% faster than a number nobody wrote down.
- **The dependency nobody approved** — that is a decision about their lockfile, their build, and their security review.

## Red flags — eight entries

Check the finished work against all eight before writing the handoff. Every one that fired goes in the handoff at file:line under its entry name, including the ones fixed on the spot.

- **The check that never entered the file** — a criterion reported met by a command that never reached the changed lines. Or a test that has only ever passed.
- **Code nothing reaches** — the unit tests are green. The route was never registered.
- **The unvisited call site** — a signature changed and its callers were never swept. Or an external symbol called with no installed source opened and no existing call site cited.
- **The third-hour criterion** — the one that got smaller while nobody was rereading it. Or a design decision made silently because asking felt slow.
- **Code ahead of its plan** — an edit written before the step covering it was approved, or a step that ran differently from its approved wording with no edit to the plan.
- **The placeholder in a production path** — a TODO, a hardcoded return standing in for real work, an unimplemented branch, a swallowed error, a fixture the runtime reads.
- **Partial work reported whole** — a multi-slice feature handed over as done, with the remainder demoted to a closing note that begins "the rest is just wiring".
- **Nothing accounts for it** — a file in the diff tracing to no criterion and no reported cleanup, a user-quoted behavior with no record entry, a record entry no test quotes, or an assumption stated mid-run and missing from the handoff.

## Process failure modes — cited from the body

- **Layer cut.** A slice named for a layer, when it should be named for what a person can do. "The data layer" fails the slice bar twice: its only demo is a passing test suite, and the thing the user asked for is three diffs out. Re-cut to a seam a user reaches.
- **Stop inflation.** A checkpoint at every slice boundary regardless of whether a decision is waiting there. Six stops on a six-slice feature is the skill running for its own benefit. A boundary with no open question gets three lines and keeps moving.
- **Plan ceremony.** A plan file written for a four-line change. One-slice tactical work keeps the criteria list in chat.
