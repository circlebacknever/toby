# Skills and config diffs

The Toby instructions file is the file every session loads. A change to it, to a `SKILL.md`, to a hook, or to an agent config changes every later session. A review that checks only the wording misses those behavior changes, so ask these three questions.

- **Does this rule contradict another skill?** Quote both, at path:line. Two skills stating opposite rules is a finding whichever one is right.
- **Does an edit to a skill's description change which skill the agent loads?** When the description names a broader kind of task, the agent loads the skill on tasks it should skip. When the description names a narrower kind of task, the agent stops loading the skill on tasks that need it. Give a task that now loads a different skill.
- **Did a rule vanish while text moved?** A reviewer can approve a diff that moves text between files without noticing a rule that was dropped. Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent. For each deleted rule that does not appear anywhere on the new side, report its old path:line.
