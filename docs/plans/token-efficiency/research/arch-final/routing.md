## Skill Routing
- These routes stay active whenever the matching skill is installed, including late in a long chat. Each request loads one entry skill, picked by its description. The entry skill opens the method skills it lists, at the step that needs them.
- Open `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-errors`, `toby-swd-clarity`, and `toby-swd-docs` only when an entry skill lists them, because no request starts one of them alone.
- When a Toby skill and a skill from another source match the same request, load the Toby skill.
- `toby-voice` stays in force for the rest of the session once it loads. Its rules apply to every reply from that point, in chat and in files, until the user says otherwise. A skill that has to be re-invoked each turn stops being applied around turn six.
- Load `toby-voice` before finalizing voice-bearing output: a substantive reply, code findings, a commit message, a PR description, docs, comments, a plan, or any generated artifact. Load its `references/plain-language.md` with it, and load its `references/toby.md` only when the operating guide is absent from context. Do not wait to be asked.
- When a skill's description says to skip it for this kind of task, skip it, even when a word in the request matches. When the user calls the work throwaway, use `toby-swd-experiment`, whatever else the request names.
- `toby-learning`, `toby-squall`, and `toby-game` load only from their slash commands. When the user names one of them in a sentence and the host cannot load it, ask the user to type its slash command.
- State active skills in one short line, including each method skill an entry skill opened.
