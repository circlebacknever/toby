# Ambiguity

Use this file when two readings of the request would build different behavior. Pick the next step by what a wrong guess would cost.

When doing what the request says would not solve the problem the user described, say so before any code.

- **Ask before any code** when the code built from a wrong guess would write data, change a public contract or a stored format, or move money. Ask first also when that code would touch permissions, ship a user-visible string, call an external system, or cost more to undo than to make. Send one message with at most three questions, both readings side by side, and your recommendation.
- **Ship it marked `assumed`** when a wrong guess costs one edit to undo. Take the reading that matches how this repo already behaves, and record the reading taken, the reading dropped, and what changes if the user wanted the other one. Do not write `assumed: standard behavior`, because it states neither reading and leaves the question open.
- **Ship the part that can be undone, marked `blocked`,** when nobody is available to answer. Record the question verbatim and stop where the irreversible part starts. Never mark a question blocked before asking it.

Do not ask a question the repo or the user already answered. For example, a new field in an existing response uses the format of the fields beside it.
