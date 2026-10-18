# Criteria

In strategic work, give each of the three parts below its own line. In tactical work, write all three on one line per criterion in chat. After an experiment, start from the behavior the user picked.

- **Observable**: what the user or caller sees at the entry point they use, such as a route, CLI command, screen, queue consumer, or exported function, including the action and starting state. When a reader could check the line only by reading the diff, rewrite or cut it.
- **Source**: the quoted sentence from the user or ticket, or the repo fact at `path:line` that requires it when the request doesn't mention that case. Mark a reading you inferred as `assumed`.
- **Check**: the command that shows the criterion holds, and the result that means it is unmet. When the check needs an approval-gated command, credential, external service, or device, mark the criterion `unverified` and state the blocker on the same line. In strategic work, run each Check that already exists before stop 1 and quote the output.

`references/examples.md` shows criteria written this way for four requests. Write criteria this way for two kinds of word in the request:

- A word that covers a set, such as `wherever`, `every`, or `all`, or a switch to a new tool. Search the repo for each member of the set and write one criterion for each.
- A quality, such as `organized` or `native`. Write a criterion that states what the quality means in this repo's files and modules, and mark it as your reading.

## Words

Use the words the schema, routes, and UI already use. Give a new product concept a plain name, and list that name in the plan so the user can change it.

## After coding starts

Once coding starts, you may widen a criterion and report the change at the next stop. To narrow or drop a criterion, give the reason and the new wording, and wait for approval before the next edit.
