# Toby

Toby's work habits, packed so they ride along to more than one machine. Clone, install, and the local assistants pick up the same vibe, caution around commands, and quiet opinions about whitespace.

Small suitcase. Toby travels light.

## What you get

- Toby's operating rules from `base/toby.md`: machine safety, work loop, skill routing, verification posture, and voice.
- Skills, tucked into each tool's skill folder.
- An always-on instruction file per tool.
- A `toby-voice` skill for explicit voice repair.
- A validator that catches drift before it ships.

## Supported tools

| Tool | Skills go to | Instructions go to |
| --- | --- | --- |
| Codex | `~/.codex/skills/toby-*` | `~/.codex/AGENTS.md` |
| Claude Code | `~/.claude/skills/toby-*` | `~/.claude/CLAUDE.md` |
| GitHub Copilot CLI | `~/.copilot/skills/toby-*` | `~/.copilot/copilot-instructions.md` |
| Kiro | `~/.kiro/skills/toby-*` | `~/.kiro/steering/toby-instructions.md` |

Kiro reads steering with `inclusion: always`. Everyone else gets a marked instruction block in their tool file.

`github` and `copilot` point at the same target (`~/.copilot/`). Repo-level `.github/` for the cloud agent lives in each repo, so the installer leaves it alone.

## Quick start

```sh
git clone https://github.com/circlebacknever/toby
cd toby
scripts/install.sh --dry-run --tool all   # look
scripts/install.sh --tool all             # leap
scripts/install.sh --force.               # fall
```

One tool at a time:

```sh
scripts/install.sh --tool codex
scripts/install.sh --tool claude
scripts/install.sh --tool github   # alias for copilot
scripts/install.sh --tool kiro
```

## Toby is careful

The installer edits one marked block and leaves the rest of the file alone:

```md
<!-- BEGIN TOBY INSTRUCTIONS -->
...
<!-- END TOBY INSTRUCTIONS -->
```

Block already there? Only the block changes. No block? The installer waits for `--force` before it adds anything. Same deal for skill folders: an existing `toby-*` stays put unless you `--force` it.

## What's in Toby's box

- `base/toby.md` - Toby's operating guide. Source of truth.
- `AGENTS.md` - Codex's copy of it.
- `instructions/` - always-on files for Claude Code, Copilot, and Kiro.
- `skills/toby-*` - the skills.
- `scripts/install.sh` - the installer.
- `scripts/validate-skills.py` - the validator.
- `evals/` - the regression suite. `evals/README.md` says how to run it and how to add a case.

The operating guide owns safety, work loop, skill routing, verification posture, and voice. Skills own task method. Toby keeps the boundary visible, since mixed guidance turns into paperwork with hinges.

A skill points at the guide by calling it "the operating guide" and never by a filename. `base/toby.md` is a path in this repo and nowhere else after install, and the installed name is `CLAUDE.md` on one tool, `AGENTS.md` on another, `copilot-instructions.md` on a third. The guide loads on every turn, so the name is all a skill needs. The validator fails on `base/toby.md` inside `skills/`. It does not police the `AGENTS.md` spelling, because `toby-swd-docs` uses that filename for the module doc in the user's own repo.

## Skills

The first five workflow skills are adapted from Anthropic skills. Toby kept the workflow, rewrote the instructions, and packaged them as `toby-*` names:

- `toby-code-review` - tight findings for diffs and PRs.
- `toby-explain` - explain a decision while the work keeps moving.
- `toby-feature-dev` - ship a small change with evidence.
- `toby-learning` - teach through your own contributions.
- `toby-simplify-code` - tighten code, keep behavior.

The rest of the standalone skills are Toby-specific:

- `toby-squall` - turn one example of a problem into a map of potential solutions.
- `toby-artifact-style` - apply the artifact design system.
- `toby-voice` - fix output that wandered off voice.
- `toby-game` - build and tune a playable thing.

The `toby-swd-*` set is the engineering method, one skill per habit:

The SWD skills come from Toby reading two books people usually argue about in separate rooms: John Ousterhout's *A Philosophy of Software Design* and Robert C. Martin's *Clean Code*. He treated both as source material, then chose the parts he trusts when he's touching real code.

Ousterhout gives him the structure vote. `toby-swd-strategy`, `toby-swd-modules`, and `toby-swd-interfaces` care about design before tactical code. They favor deep modules, smaller caller burden, interface comments, and contracts written before bodies. Martin contributes the local habits Toby still wants: names, readable flow, behavior tests, and small functions when the split earns its keep. Refactoring comes after the boundary is sound. When a local habit creates shallow interfaces, hides a contract, or lets tests steer design into a cul-de-sac, Toby picks the boundary rule. Settle the floor plan before the desk drawer.

- `toby-swd-environment` - treat the user's machine like a guest would: look around and ask before touching processes, ports, or data.
- `toby-swd-strategy` - weigh how today's change constrains every change after it, so the codebase stays easy to work in.
- `toby-swd-modules` - decide where code lives so each module hides its own mess and callers stay light.
- `toby-swd-interfaces` - design the contract a caller sees, keeping it small for the work it does.
- `toby-swd-testing` - write tests that pin behavior and catch regressions without freezing the implementation in place.
- `toby-swd-complexity` - keep error handling and performance work deliberate, so complexity doesn't pile up unnoticed.
- `toby-swd-clarity` - name things well and keep code obvious on read, since reading happens far more than writing.
- `toby-swd-docs` - keep the why and the who-it's-for in `AGENTS.md` and `README.md`, where the code can't say it.
- `toby-swd-experiment` - spike mode: move fast to learn first, save the durable build for later.

## Toby wants to live

Before you push:

```sh
python3 evals/run.py gates
scripts/install.sh --dry-run --tool all
git diff --check
```

`evals/run.py gates` runs the validator and then compares this tree against the
numbers in `evals/baselines/gates.json`: warnings by kind, body tokens per
skill, co-load tokens per routing group, and the list of rules that have left
the repo. It goes red when any of them gets worse. When the change is meant to
move one, `evals/run.py record` writes the new number down, and that is the step
that makes an improvement stick.

`tests/test-gates.py` seeds a regression against each gate and checks it goes
red, so a gate cannot quietly lose the ability to fail. The evals that need a
model to write something live beside these and never gate, because five samples
of the voice suite on identical inputs scored 1, 1, 4, 4, and 11.

Full install test that never touches your real home:

```sh
scripts/test-install.sh
```

It installs into a throwaway `HOME`, then checks what landed. Skill counts come from the repo rather than a constant, so adding a skill cannot leave the test quietly red. Every installed skill is compared byte-for-byte against `skills/`, and every instruction block is compared against `base/toby.md`.

It also tests the two promises above. A re-install without `--force` must refuse, text around a marker block must survive, and a file with no marker block must come back untouched. The temp dirs clear on the way out.

## A small heads-up

This installs Toby's taste, which is a generous word for preferences he can't stop having. Rewrite `base/toby.md`, and it turns into yours.
