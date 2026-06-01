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

The operating guide owns safety, work loop, skill routing, verification posture, and voice. Skills own task method. Toby keeps the boundary visible, since mixed guidance turns into paperwork with hinges.

## Skills

The first five workflow skills are adapted from Anthropic skills. Toby kept the workflow shape, rewrote the instructions, and packaged them as `toby-*` names:

- `toby-code-review` - tight findings for diffs and PRs.
- `toby-explain` - explain a decision while the work keeps moving.
- `toby-feature-dev` - ship a small change with evidence.
- `toby-learning` - teach through your own contributions.
- `toby-simplify-code` - tighten code, keep behavior.

The rest of the standalone skills are Toby-specific:

- `toby-squall` - turn one example of a problem into a map of potential solutions.
- `toby-artifact-style` - apply the artifact design system.
- `toby-voice` - fix output that wandered off voice.

The `toby-swd-*` set is the engineering method, one skill per habit:

The SWD skills come from Toby reading two books people usually argue about in separate rooms: John Ousterhout's *A Philosophy of Software Design* and Robert C. Martin's *Clean Code*. He treated both as source material, then chose the parts he trusts when he's touching real code.

Here is where Toby landed. Ousterhout gives him the structure vote. `toby-swd-strategy`, `toby-swd-modules`, and `toby-swd-interfaces` care about design before tactical code. They favor deep modules, smaller caller burden, interface comments, and contracts written before bodies. Martin contributes the local habits Toby still wants: names, readable flow, behavior tests, and small functions when the split earns its keep. Refactoring comes after the boundary is sound. When a local habit creates shallow interfaces, hides a contract, or lets tests steer design into a cul-de-sac, Toby picks the boundary rule. Floor plan before desk drawer.

- `toby-swd-environment` - treat the user's machine like a guest would: look around and ask before touching processes, ports, or data.
- `toby-swd-strategy` - weigh how today's change shapes every change after it, so the codebase stays easy to work in.
- `toby-swd-modules` - decide where code lives so each module hides its own mess and callers stay light.
- `toby-swd-interfaces` - shape the contract a caller sees, keeping it small for the work it does.
- `toby-swd-testing` - write tests that pin behavior and catch regressions without freezing the implementation in place.
- `toby-swd-complexity` - keep error handling and performance work deliberate, so complexity doesn't pile up unnoticed.
- `toby-swd-clarity` - name things well and keep code obvious on read, since reading happens far more than writing.
- `toby-swd-docs` - keep the why and the who-it's-for in `AGENTS.md` and `README.md`, where the code can't say it.
- `toby-swd-experiment` - spike mode: move fast to learn first, save the durable build for later.

## Toby wants to live

Before you push:

```sh
python3 scripts/validate-skills.py skills
scripts/install.sh --dry-run --tool all
git diff --check
```

Full install test that never touches your real home:

```sh
scripts/test-install.sh
```

It installs into a throwaway `HOME`, counts 17 skills per tool (68 total), checks the instruction files landed and Kiro kept `inclusion: always`, then clears the temp dir on the way out.

## A small heads-up

This installs Toby's taste, which is a generous word for preferences he can't stop having. Rewrite `base/toby.md`, and it turns into yours.
