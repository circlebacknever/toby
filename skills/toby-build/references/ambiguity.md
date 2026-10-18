# Ambiguity

Use this file when two readings of the request fit its words and neither has a usual answer under the operating guide's Decisions section. Read the repo and run the read-only commands that could settle the question first.

When doing what the request says wouldn't solve the problem the user described, say so before writing code.

- **Ship it marked `assumed`** when one edit undoes a wrong guess. Take the reading closest to how this repo already behaves, and state the reading taken, the reading dropped, and what changes if the user wanted the other one.
- **Ask before any code** only when one edit can't undo a wrong guess because the code writes data, changes a public contract or stored format, moves money, changes permissions, or calls an external system. Ask every question in the first sentence of one message, give at most three options side by side, and recommend one.
- **Ship the reversible part, marked `blocked`,** when the user isn't available to answer after you asked. Record the question verbatim and stop where the irreversible work starts.
