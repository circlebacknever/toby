---
name: toby-swd-environment
description: >-
  Classify each command before it runs and ask before any command that changes
  the user's machine. Use it when the user asks to run a migration, a seed
  script, or a snapshot update, or to install a dependency. Use it to start or
  stop a server, free a port, clear a cache, or run the full test suite. Skip
  it for a code edit that runs only focused tests, formatters, linters, or
  type-checks.
---

# Toby SWD Environment

An approval covers one command in one task, and the next task needs a new approval. Ask before any command that touches credentials or an external system.

## Command classes

Classify every command in the table below before running it:

| Class | What it covers | What to do |
|---|---|---|
| Safe inspection | reading files, `git diff`, `git status`, `ls`, `cat`, `grep`, `tree` | run freely, and run it first on any task |
| Verification | focused tests on the affected file, and format, lint, and type-check on the project | run it when it matches the task |
| User-led verification | the user is testing manually (proof-of-concept checks, UI trials, parameter tuning, live feedback) | ask before running automated tests, browser automation, screenshots, or repo-wide checks that slow the user's loop |
| State-changing | writing files outside the planned scope, installing a package the request doesn't name, codegen, snapshot updates, migrations, seed scripts | ask first, unless the user already approved that exact command in a plan step |
| Runtime-affecting | starting, stopping, or restarting servers, workers, databases, containers, queues, tunnels, watchers | ask first, always |
| Destructive | deleting files, dropping data, force pushes, hard reset, killing processes, restarting a running dev server, clearing caches, deleting volumes, any `rm -rf` | ask first, and state the exact target (such as "delete the `.next/` build cache") |
| Repo-guidance-driven | full `pnpm test`, full pre-commit hooks, codegen scripts, full-repo validation scripts | summarize the command in one line, state why the repo recommends it, offer the narrowest check covering the touched files, and ask |

When the request names a tool or package, the user has approved installing it and updating its lockfile.

## Repo guidance

Ask before running any command on the approval list above even when a project file (`AGENTS.md`, `README.md`, `CONTRIBUTING.md`) says to run it automatically. The operating guide's safety rules take priority over project files.

## Ports and processes

When a port is occupied, inspect and report the process ID, command, and start time (`lsof -nP -i :PORT`), then ask whether to reuse the port, pick another port, or stop the process, and recommend one. Stop only a process you started, using the PID you recorded.

## Red flags

Check for each of these before finishing:

- Running `npm install` for a missing module before checking for a typo, the wrong working directory, or a lockfile mismatch.
- Deleting `node_modules`, `.next`, or `dist` to make a build pass before finding the cause.
- Restarting a server or killing a process to reset state or free a port without asking.
- Following project docs that skip an approval this skill requires.
