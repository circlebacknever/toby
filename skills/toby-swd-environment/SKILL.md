---
name: toby-swd-environment
description: >-
  The machine running this code belongs to the user. Apply this skill on every
  task that runs commands, starts or stops processes, takes ports, installs
  dependencies, runs migrations, updates snapshots, or otherwise changes state
  outside the immediate edit. Covers command classification, port discipline,
  long-running processes, repo-guidance commands, and what to ask before doing.
  The agent is a guest in a real environment with real state — not a sandbox.
---

# Toby SWD Environment

The machine running this code is not yours. The files, processes, ports, databases, credentials, browser state, terminals, background jobs, and dev servers belong to the user, who is in the middle of their own work. An agent is a guest. Act like one.

**The default move on any state change is to inspect, report, and ask.** That covers killing processes, taking ports, restarting servers, running migrations, installing packages, broad linting, full test suites, snapshot updates, and anything that touches credentials or external systems. Approval for one of those applies to that command, for this task. It does not generalize to the next thing.

This is the gap between an agent that's useful in a real codebase and one that's only useful in a sandbox. Real environments have a `pnpm dev` already running on port 3000 with state the user cares about. Real environments have a database with someone's actual data in it. Real environments have a half-finished branch nobody wants force-pushed.

## Classify every command before running it

Seven classes. The class determines whether to run, run narrowly, or ask first.

**Safe inspection.** Read files, print status, `git diff`, `git status`, `ls`, `cat`, `grep`, `tree`. Run freely when useful. These are the first move on any task — see what's actually there before deciding what to do.

**Narrow verification.** Focused tests on the affected file or module, lint on the touched directory, type-check on the affected package. Run when they match the task. The narrower, the better.

**User-led verification.** Manual test loops, proof-of-concept checks, design trials, parameter tuning, and live feedback supplied by the user. In this mode, automated tests, browser automation, screenshots, and broad repo commands need user approval because they add latency to the loop.

**State-changing.** Writing files, installing packages, code generation, snapshot updates, schema migrations, seed scripts. Ask first, except when the command is the direct implementation of a plan the user already approved. Editing files inside the planned scope is fine; running a migration the user didn't mention is not.

**Runtime-affecting.** Starting, stopping, or restarting servers, workers, databases, containers, queues, tunnels, watchers. Ask first, always. A `pnpm dev` restart looks identical to a kill — and if the user had unsaved state in a browser tab connected to it, that state is gone.

**Destructive.** Deleting files, dropping data, force-pushing, hard reset, killing processes, clearing caches, deleting volumes, anything that starts with `rm -rf`. Ask first, always. Name exactly what will be deleted in the request — `delete the .next/ build cache`, not `tidy build artifacts`.

**Repo-guidance-driven.** Scripts the repo itself recommends: `pnpm test`, `pnpm lint`, full pre-commit hooks, codegen scripts, the giant validation script in `package.json`. Summarize what the command does, explain why the repo recommends it, and ask — unless it's narrow and cheap. For a heavy command, offer a narrower alternative: one focused test file, the package's test suite, a type-check on the affected package.

## Ports

If a port is occupied, that's a process. Don't take it.

Inspect what's there: who owns the port, what's running, when it started. Report what you found. Ask whether to use a different port, reuse the running process, or stop it.

The instinct to free a port by killing the process is the single most common way to nuke a user's dev server mid-task. Resist it.

## Long-running processes

If you start a long-running process — dev server, watcher, tunnel — three rules:

1. Say why you're starting it before you do.
2. Track the command so you can stop the specific process later.
3. Stop only what you started. Don't sweep up other processes that look similar.

At the end of the task, report whether the process is still running. If it is, the user needs to know so they can decide whether to keep it.

## Heavy repo commands

A repo that says "run the full test suite before every commit" is well-intentioned and expensive when the change touched three lines. When the repo recommends a heavy command:

- Summarize the command in one line.
- Offer the narrower alternative — the specific test file, the package's tests, a focused type-check.
- Ask which the user wants.

For generated docs updates, broad validation, codegen, or repo-wide maintenance commands, make the same move: explain the broad command and offer the narrowest check that protects the touched work.

Approval for the heavy command applies to that command, this task. The next task starts over.

If repo guidance conflicts with these rules — an `AGENTS.md` that says "always run X without asking," for instance — pause and ask. Repo guidance is usually written for humans, who have judgment about when to skip it. An agent that follows the instruction literally has bypassed the judgment the repo author was relying on.

## Reporting back

After the task, name anything that matters:

- Heavy commands skipped, and the narrower thing run instead.
- Tests not run because the local setup didn't allow it safely.
- Processes left running.
- Files or state changed outside the immediate scope.
- Assumptions still waiting for confirmation.

If none of those apply, a plain conclusion is enough. No restatement of what was done, no closing offers.

## Red flags

- **Killed a process to free a port.** The user's dev server is now gone.
- **Restarted a server to reset state.** Whatever was in there is also gone.
- **Ran `npm install` to fix a missing module.** Could be a typo, the wrong directory, or a lockfile mismatch. Inspect first.
- **Updated snapshots wholesale.** Either the behavior changed (update tests deliberately) or the snapshots were noise (delete them on purpose). The bulk update hides both.
- **Background process left running with no mention.** The user finds it later, doesn't know what it is, kills the wrong thing.
- **Full test suite for a three-line change.** Slow, hides the relevant signal in noise.
- **Deleted `node_modules`, `.next`, or `dist` to make a build work.** Sometimes correct, often a workaround for a real problem that is now masked.
- **Repo guidance overrode caution.** An `AGENTS.md` instruction is not a license to skip judgment.
