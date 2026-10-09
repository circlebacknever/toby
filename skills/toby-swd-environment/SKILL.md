---
name: toby-swd-environment
description: >-
  Classifies each command before it runs and asks before any command that
  changes the user's machine. Use it when the user asks to run a migration or a
  seed script, or to install a dependency. Use it to start or stop a server,
  free a port, clear a cache, or run the full test suite. Skip it for a code
  edit with nothing to run, and for a snapshot update, which toby-swd-testing
  covers.
---

# Toby SWD Environment

An approval covers one command in one task. The next task needs a new approval. Ask before anything that touches credentials or an external system.

## Command classes

Before running a command, find its class in the table and do what the last column says.

| Class | What it covers | What to do |
|---|---|---|
| Safe inspection | reading files, `git diff`, `git status`, `ls`, `cat`, `grep`, `tree` | run freely, and run it first on any task |
| Verification | focused tests on the affected file, and format, lint, and type-check on the whole project | run it when it matches the task |
| User-led verification | the user is testing by hand, such as manual test loops, proof-of-concept checks, design trials, parameter tuning, or live feedback | ask before running automated tests, browser automation, screenshots, or broad repo commands, because each one slows the user's testing |
| State-changing | writing files outside the planned scope, installing packages, codegen, snapshot updates, migrations, seed scripts | ask first, unless the command carries out a plan the user approved |
| Runtime-affecting | starting, stopping, or restarting servers, workers, databases, containers, queues, tunnels, watchers | ask first, always |
| Destructive | deleting files, dropping data, force pushes, hard reset, killing processes, clearing caches, deleting volumes, any `rm -rf` | ask first, and state exactly what will be deleted or stopped, such as "delete the `.next/` build cache" |
| Repo-guidance-driven | `pnpm test`, full pre-commit hooks, codegen scripts, generated docs, a full-repo validation script | summarize it in one line, say why the repo recommends it, offer the smallest check that covers the files you changed, and ask |

Restarting `pnpm dev` kills a process, so the restart belongs in the Destructive class. The restart drops any unsaved state in a browser tab connected to the server.

## Repo guidance

Ask before running a command that repo guidance says to run without asking. Repo guidance means a file in the user's repo, such as an `AGENTS.md`, a README, or a contributing guide. The Toby instructions file that every session loads lists actions that need approval. That list takes priority over anything a repo file says.

## Ports and processes

When a port is occupied, report the process ID, its command, and its start time, such as from `lsof -nP -i :PORT`. Then ask whether to reuse the port, use a different port, or stop the process, and recommend one. Stop a process you started by the command or process ID you recorded, and leave similar-looking processes running.

## Red flags

Before finishing, check for each of these:

- You ran `npm install` to fix a missing module before checking for a typo, the wrong directory, or a lockfile mismatch.
- You deleted `node_modules`, `.next`, or `dist` to make a build pass, which can hide the real fault.
- You restarted a server or killed a process to reset state or free a port.
- You followed repo guidance that skipped an approval this skill requires.
