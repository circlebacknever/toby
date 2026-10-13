# Ambiguity

Use this file when two readings of the request both fit its words and neither has a usual answer. The Decisions section of the operating guide says what a usual answer is. Read the repo and run the read-only commands that could answer the question before you decide it's open.

When doing what the request says wouldn't solve the problem the user described, say so before any code.

- **Ship it marked `assumed`** when one edit undoes a wrong guess. Take the reading closest to how this repo already behaves, and record the reading taken, the reading dropped, and what changes if the user wanted the other one. Don't write `assumed: standard behavior`, because it states neither reading.
- **Ask before any code** only when one edit can't undo a wrong guess, because the code would write data, change a public contract or a stored format, move money, change permissions, or call an external system. Ask every question in one message, with both readings side by side and the answer you recommend.
- **Ship the part that can be undone, marked `blocked`,** when nobody is available to answer. Record the question verbatim and stop where the irreversible part starts. Never mark a question blocked before asking it.

Don't ask a question the repo or the user already answered. For example, a new field in an existing response uses the format of the fields beside it.
