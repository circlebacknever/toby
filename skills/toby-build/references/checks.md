# Catalogs

## Don't build — seven entries

When one of these ships anyway, state the entry and the criterion that allowed it.

- **The one-caller config option** is a setting, hook, or extension point that exactly one call site reads. A later slice removes a slice flag. This option stays in the code with a default. Its value never changes from the default, so the setting adds a code path that nobody uses.
- **The wrapper over one instance** is a new module, layer, or adapter in front of a single implementation. Extend the interface you already have, as toby-swd-interfaces describes, and wait for a second implementation. The second implementation shows you what the two have in common. A module with two or more callers passes this entry. So does a module the design pass approved because it hides a lot behind a small interface, such as a storage layout or an external API.
- **Handling for a ruled-out condition** is error handling for a state that the types or an earlier check already exclude.
- **The adjacent feature, and the adjacent bug** are a feature the request implies but does not ask for, and a defect you found while working on the request. Changes made "while I was in there" turn a two-file diff into a nine-file diff. List each as a follow-up and stop. The one exception is the cleanup of a single flaw that the Existing code section of toby-swd-strategy allows. That section allows a small local cleanup inside a file a criterion already mentions, reported on its own line.
- **The uninvited migration** is a migration, rename, or reorganization that no criterion asked for. It appears unrequested in somebody else's review, so the reviewer has to decide whether to trust it. A refactor stated in the plan's design block and approved with the plan passes this entry.
- **Unmeasured optimization** is performance work with no measurement behind it. Without a starting measurement, a claim such as 40% faster has no recorded number to compare against.
- **The dependency nobody approved** is a new dependency added without approval. Adding it makes a decision for the user about their lockfile, build, and security review.

## Red flags — eight entries

- **A check that never ran the changed lines** is a criterion reported met by a command that never reached the changed lines, or a test that nobody has seen fail.
- **Unreachable code** means the unit tests pass, but the route was never registered.
- **An unchecked caller or symbol** means a signature changed and nobody checked all its callers. This entry also covers a call to an external symbol when nobody opened its installed source or cited an existing call site.
- **A criterion or design decision changed without asking** is a criterion that came to cover less during long work because nobody reread it, or a design decision made without asking because asking felt slow.
- **Code ahead of its plan** is an edit written before the step covering it was approved. It also covers a step that ran differently from its approved wording with no edit to the plan.
- **The placeholder in a production path** is a TODO, a hardcoded return in place of real work, an unimplemented branch, a swallowed error, or a fixture the runtime reads.
- **Partial work reported whole** is a multi-slice feature handed over as done, with the remaining work moved to a closing note that begins "the rest is just wiring".
- **An untraced file** is a file in the diff that no criterion and no reported cleanup accounts for. This entry also covers an assumption stated mid-run but missing from the handoff.
