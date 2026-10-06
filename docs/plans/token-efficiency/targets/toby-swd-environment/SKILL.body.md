# Toby SWD Environment

An approval covers one command in one task. The next task needs a new approval. Ask before anything that touches credentials or an external system.

## Command classes

Classify each command before running it, and take the move its class gives.

| Class | What it covers | Move |
|---|---|---|
| Safe inspection | reading files, `git diff`, `git status`, `ls`, `cat`, `grep`, `tree` | run freely, and run it first on any task |
| Narrow verification | focused tests on the affected file, lint on the touched directory, type-check on the affected package | run it in its narrowest form when it matches the task |
| User-led verification | manual test loops, proof-of-concept checks, design trials, parameter tuning, live feedback | ask before automated tests, browser automation, screenshots, or broad repo commands, because each one slows the user's loop |
| State-changing | writing files outside the planned scope, installing packages, codegen, snapshot updates, migrations, seed scripts | ask first, unless the command carries out a plan the user approved |
| Runtime-affecting | starting, stopping, or restarting servers, workers, databases, containers, queues, tunnels, watchers | ask first, always |
| Destructive | deleting files, dropping data, force pushes, hard reset, killing processes, clearing caches, deleting volumes, any `rm -rf` | ask first, and state exactly what will be deleted or stopped, such as "delete the `.next/` build cache" |
| Repo-guidance-driven | `pnpm test`, `pnpm lint`, full pre-commit hooks, codegen scripts, generated docs, a full-repo validation script | summarize it in one line, say why the repo recommends it, offer the narrowest check of the touched work, and ask |

A `pnpm dev` restart counts as a kill, because it drops any unsaved state in a browser tab connected to it.

## Repo guidance

Ask before running a command that repo guidance says to run without asking. Repo guidance means a file in the user's repo, such as an `AGENTS.md`, a README, or a contributing guide. The operating guide's list of actions that need approval outranks a repo file.

## Ports and processes

When a port is occupied, report the process ID, its command, and its start time, such as from `lsof -nP -i :PORT`. Then ask the operating guide's question. Stop a process you started by the command or process ID you recorded, and leave similar-looking processes running.

## Red flags

Before finishing, check for each of these:

- You ran `npm install` to fix a missing module before checking for a typo, the wrong directory, or a lockfile mismatch.
- You deleted `node_modules`, `.next`, or `dist` to make a build pass, which can hide the real fault.
- You restarted a server or killed a process to reset state or free a port.
- You followed repo guidance that skipped an approval this skill requires.
