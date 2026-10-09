# Skills and config diffs

Every session loads the agent instructions file, such as `AGENTS.md`. A change to that file, to a `SKILL.md`, to an agent hook, or to an agent config changes every later session. An agent hook is a command that runs on an agent event, such as a file edit or a session start. A review that checks only the wording misses those behavior changes, so ask these three questions.

- **Does this rule contradict another skill?** Quote both, at path:line. Two skills stating opposite rules is an issue whichever one is right.
- **Does an edit to a skill's description change which skill the agent loads?** A wider description makes the agent load the skill on tasks it should skip, and a narrower one makes the agent miss tasks that need it. Give a task that now loads a different skill.
- **Did a rule vanish while text moved?** A reviewer can approve a diff that moves text between files without noticing a rule that was dropped. Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent. For each deleted rule that does not appear anywhere on the new side, report its old path:line.

Write each issue in the review's usual form, and put the two quotes, the task, or the old path:line in its Reproduce block.
