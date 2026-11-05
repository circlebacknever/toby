# Execution cases

These cases check whether fresh agents build and repair executable behavior with useful diagnostics.

## Prepare

```sh
python3 evals/execution.py prepare build
python3 evals/execution.py prepare bug-fix
```

Each command creates an isolated directory under `/private/tmp` and prints its workspace and `TASK.md` paths as JSON.
Give a fresh agent that workspace and task. The agent reads the copied guide and skills in the workspace.
The task approves fixture edits and focused checks, so the agent can finish without approval stops.
The workspace doesn't contain the independent grader or a completed repair.

Use the same fixture with another skill revision:

```sh
python3 evals/execution.py prepare build --skills-source /absolute/path/to/skill-snapshot
```

The source directory must contain `base/toby.md` and `skills/`.
Use independent fresh sessions for each revision. Don't give them findings, completed repairs, or grader output before they finish.
Record their final replies, checks, and resulting diffs separately from the prepared workspace.

## Grade

```sh
python3 evals/execution.py grade build /private/tmp/toby-build-EXAMPLE
python3 evals/execution.py grade bug-fix /private/tmp/toby-bug-fix-EXAMPLE
```

The grader runs outside the candidate workspace in a separate Python process.
It invokes the domain operation, API function, and command function with controlled provider responses.
It checks successful archiving, invalid states, repeated requests, provider failure, retry, and preserved error causes.
It also parses the JSON actually emitted by the logger and checks request context, report context, outcome, duration, safe error type, and redaction.
Removing the logger fails those checks even when the archive behavior passes.
Changing candidate tests can't change the independent checks.

Read the resulting diff to judge whether entry points delegate state rules to the domain module and whether the explanation teaches normal use and retry behavior.
The executable grade doesn't establish module depth or explanation quality.
An agent must run the checks before its changes and after them. A grader pass alone doesn't establish that it followed that work loop.

Run the focused checks for this runner with `python3 -m unittest evals/test_execution.py -v`.
These checks prove the initial fixtures fail, a complete repair passes, and removed diagnostics still fail.
Prepared workspaces remain available for review until their owner removes them.
