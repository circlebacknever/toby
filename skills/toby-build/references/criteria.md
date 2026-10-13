# Criteria

Give each of the three parts below its own line. After an experiment, start from the behavior the user picked. When the request doesn't give a part, write it from what the request means and what the repo shows, and mark it as your reading.

- **Observable**: what the user or caller sees at the entry point they use, such as a route, a CLI command, a screen, a queue consumer, or an exported function. State the action and the starting state. When a reader could check the line only by reading the diff, rewrite it or cut it.
- **Source**: the user's sentence or ticket line the criterion came from, quoted, or the repo fact at path:line that requires it. A claim about the repo with no path:line is your own preference. Cite a repo fact only when the request says nothing about that behavior.
- **Check**: the command that shows the criterion holds, and the result that means it is unmet. When the check needs an approval-gated command, a credential, an external service, or a device, mark the criterion `unverified` and state the blocker on the same line. In strategic work, run each Check that already exists, such as a suite that must keep passing, before stop 1 and quote the output. A Check for new behavior gets its first run at the start of its plan group. A check you could have run and skipped leaves the criterion unmet.

`references/examples.md` has criteria written this way for four requests. For example, the criterion "cancelling someone else's order returns 404" can cite the ownership check at `api/orders.ts:31` as its Source.

Write criteria this way for two kinds of word in the request:

- A word that covers a set, such as wherever, every, or all, or a switch to a new tool. Search the repo for each member of the set, and write one criterion for each.
- A quality, such as organized or native. Write a criterion that states what the quality means in this repo's files and modules, and mark it as your reading.

## Words

Use the words the schema, the routes, and the UI already use. Give a new product concept a plain name, and list that name in the plan so the user can change it. Users and docs keep an invented product word after the code that introduced it is gone.

## After coding starts

Once coding starts, you may widen a criterion and mention the change in the next report. To narrow or drop a criterion, give the reason and the new wording, and wait for a yes before the next edit.
