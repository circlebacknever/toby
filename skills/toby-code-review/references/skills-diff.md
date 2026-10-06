# Skills and config diffs

A change to a `SKILL.md`, an operating guide, a hook, or an agent config changes every later run. Reading it as prose misses those effects, so ask these three questions.

- **Does this rule contradict another skill?** Quote both, at path:line. Two skills stating opposite rules is a finding whichever one is right.
- **Does a description edit change what fires?** A widened trigger noun makes the agent load a skill on tasks it should skip. A narrowed trigger noun stops the agent from loading the skill on tasks that need it. Give a task that now loads a different skill.
- **Did a rule vanish while text moved?** A diff that moves text between files looks tidy. Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent, and report any unmatched deletion at its old path:line.
