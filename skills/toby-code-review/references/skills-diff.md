# Skills and config diffs

When a diff changes `AGENTS.md`, a `SKILL.md`, an agent hook (a command that runs on an agent event), or an agent config, check these three questions:

- **Does this rule contradict another skill?** Quote both at `path:line`. Two skills stating opposite rules is an issue whichever one is right.
- **Does an edit to a skill's description change which skill the agent loads?** A wider description makes the agent load the skill on tasks it should skip, and a narrower one makes the agent miss tasks that need it. Give a task that now loads a different skill.
- **Did a rule vanish while text moved?** Run `scripts/rule-inventory.py` against both sides, or the repo's equivalent. For each deleted rule that doesn't appear anywhere on the new side, report its old `path:line`.

Write each issue in the review's usual form, and put the two quotes, the task, or the old `path:line` in its Reproduce block.
