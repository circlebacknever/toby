#!/usr/bin/env bash
# `sh scripts/install.sh` runs this file under a shell that lacks [[ and
# pipefail, so start again under bash.
# On macOS, sh is bash in POSIX mode, which sets BASH_VERSION too.
case "${BASH_VERSION:-}:${SHELLOPTS:-}" in
  :*|*posix*) exec bash "$0" "$@" ;;
esac
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="all"
DRY_RUN=0
FORCE=0
OUTPUT_STYLE=0
HOOKS=0

usage() {
  printf 'Usage: %s [--tool codex|claude|copilot|github|kiro|all] [--output-style] [--dry-run] [--force]\n' "$0"
  printf '       github is an alias for copilot (GitHub Copilot CLI, ~/.copilot).\n'
  printf '\n'
  printf '  --hooks         Claude Code only. Install the two voice hooks to\n'
  printf '                  ~/.claude/toby/hooks, then print the settings.json block\n'
  printf '                  to paste. Does not edit settings.json itself.\n'
  printf '  --force         Replace Toby skill directories that already exist, and\n'
  printf '                  add the Toby block to instruction files that have none.\n'
  printf '  --output-style  Claude Code only. Install the writing rules as an output\n'
  printf '                  style, and install the shorter CLAUDE.md that leaves them\n'
  printf '                  out. Costs about 200 tokens more than the default, and\n'
  printf '                  puts the rules in the system prompt. You must then turn\n'
  printf '                  the style on: /config, Output style, Toby. Without that\n'
  printf '                  step the voice rules are not loaded at all.\n'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --output-style)
      OUTPUT_STYLE=1
      shift
      ;;
    --hooks)
      HOOKS=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

case "$TOOL" in
  github)
    TOOL="copilot"
    ;;
  codex|claude|copilot|kiro|all) ;;
  *)
    usage >&2
    exit 2
    ;;
esac

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] %q' "$1"
    shift
    for arg in "$@"; do
      printf ' %q' "$arg"
    done
    printf '\n'
  else
    "$@"
  fi
}

install_skills() {
  local dest="$1"
  run mkdir -p "$dest"

  local skill
  for skill in "$ROOT"/skills/toby-*; do
    [[ -d "$skill" ]] || continue
    local name
    name="$(basename "$skill")"
    local target="$dest/$name"

    if [[ -e "$target" ]]; then
      run rm -rf "$target"
    fi
    run cp -R "$skill" "$target"
    # Finder drops .DS_Store into any folder it opens, and Python can leave
    # __pycache__ behind. Keep both out of the install.
    run find "$target" \( -name .DS_Store -o -name __pycache__ \) -prune -exec rm -rf {} +
  done
}

install_hooks() {
  # The hooks only. The write hook runs the checker from the installed
  # toby-voice skill, so the checker is not copied here.
  local kit="$HOME/.claude/toby"
  local checker="$HOME/.claude/skills/toby-voice/scripts/voice-check.py"
  run mkdir -p "$kit/hooks"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] install the voice hooks to %s/hooks\n' "$kit"
    return
  fi
  run cp "$ROOT/hooks/voice-stop-check.py" "$kit/hooks/"
  run cp "$ROOT/hooks/voice-write-check.py" "$kit/hooks/"

  printf '\nvoice hooks installed to %s/hooks\n' "$kit"
  if [[ ! -f "$checker" ]]; then
    printf 'The write hook needs %s.\n' "$checker"
    printf 'Run this installer with --tool claude to install it.\n'
  fi
  printf '\n'
  printf 'To run the hooks as well, add this to %s/.claude/settings.json:\n\n' "$HOME"
  cat <<JSON
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit", "hooks": [
        { "type": "command", "command": "python3 $kit/hooks/voice-write-check.py" } ] }
    ],
    "Stop": [
      { "hooks": [
        { "type": "command", "command": "python3 $kit/hooks/voice-stop-check.py" } ] }
    ]
  }
}
JSON
  printf '\nThis installer does not edit settings.json. Paste the block yourself,\n'
  printf 'merging it with any hooks already there.\n\n'
}

install_output_style() {
  # Claude Code only. The style goes into the system prompt, which is why the
  # voice rules go here as well as in CLAUDE.md.
  local target="$HOME/.claude/output-styles/toby.md"
  run mkdir -p "$(dirname "$target")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] install Toby output style to %s\n' "$target"
    return
  fi
  run cp "$ROOT/output-styles/toby.md" "$target"
  printf '\noutput style installed, and CLAUDE.md now leaves the writing rules out.\n'
  printf 'Turn the style on before you write anything:\n'
  printf '  /config, then Output style, then Toby\n'
  printf 'Until you do, the voice rules are not loaded.\n\n'
}

install_instruction_file() {
  local source="$1"
  local target="$2"
  local mode="${3:-merge}"

  run mkdir -p "$(dirname "$target")"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    if [[ -f "$target" ]]; then
      printf '[dry-run] merge Toby instructions into %s\n' "$target"
    else
      printf '[dry-run] install Toby instructions to %s\n' "$target"
    fi
    return
  fi

  python3 - "$source" "$target" "$FORCE" "$mode" <<'PY'
from pathlib import Path
import re
import sys

source = Path(sys.argv[1])
target = Path(sys.argv[2])
force = sys.argv[3] == "1"
mode = sys.argv[4]

if mode not in {"merge", "dedicated"}:
    raise SystemExit(f"Unknown voice install mode: {mode}")

source_text = source.read_text()
block_re = re.compile(
    r"<!-- BEGIN TOBY INSTRUCTIONS -->\n?(.*?)\n?<!-- END TOBY INSTRUCTIONS -->",
    re.S,
)
match = block_re.search(source_text)
if not match:
    raise SystemExit(f"{source} has no Toby instruction marker block")
source_block = (
    "<!-- BEGIN TOBY INSTRUCTIONS -->\n"
    + match.group(1).strip()
    + "\n<!-- END TOBY INSTRUCTIONS -->"
)

if not target.exists():
    target.write_text(source_text)
    raise SystemExit(0)

target_text = target.read_text()
target_match = block_re.search(target_text)
if target_match:
    updated = target_text[: target_match.start()] + source_block + target_text[target_match.end() :]
    target.write_text(updated)
    raise SystemExit(0)

if not force:
    raise SystemExit(
        f"Refusing to change {target}; no Toby marker block found. Pass --force to append the Toby block."
    )

if mode == "dedicated":
    target.write_text(source_text)
else:
    sep = "" if target_text.endswith("\n") else "\n"
    target.write_text(target_text + sep + "\n" + source_block + "\n")
PY
}

install_codex() {
  local home="${CODEX_HOME:-$HOME/.codex}"
  install_skills "$home/skills"
  install_instruction_file "$ROOT/AGENTS.md" "$home/AGENTS.md" merge
}

install_claude() {
  install_skills "$HOME/.claude/skills"
  if [[ "$OUTPUT_STYLE" -eq 1 ]]; then
    # The style contains the writing rules, so CLAUDE.md leaves them out. Both
    # together would put the same 2,400 tokens in front of every turn twice.
    install_instruction_file "$ROOT/instructions/claude/CLAUDE-floor.md" "$HOME/.claude/CLAUDE.md" merge
    install_output_style
  else
    install_instruction_file "$ROOT/instructions/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md" merge
  fi
}

install_copilot() {
  install_skills "$HOME/.copilot/skills"
  install_instruction_file "$ROOT/instructions/copilot/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md" merge
}

install_kiro() {
  install_skills "$HOME/.kiro/skills"
  install_instruction_file "$ROOT/instructions/kiro/toby-instructions.md" "$HOME/.kiro/steering/toby-instructions.md" dedicated
}

tool_selected() {
  [[ "$TOOL" == "all" || "$TOOL" == "$1" ]]
}

# Check every target before writing anything. A refusal partway through an
# install leaves some tools updated and others stale, so report every conflict
# at once and stop while nothing has changed.
CONFLICTS=""

check_skills() {
  local dest="$1" skill target
  for skill in "$ROOT"/skills/toby-*; do
    [[ -d "$skill" ]] || continue
    target="$dest/$(basename "$skill")"
    if [[ -e "$target" ]]; then
      CONFLICTS+="  skill directory already exists: $target"$'\n'
    fi
  done
}

check_instructions() {
  local target="$1"
  if [[ -f "$target" ]] && ! grep -q '<!-- BEGIN TOBY INSTRUCTIONS -->' "$target"; then
    CONFLICTS+="  instruction file has no Toby marker block: $target"$'\n'
  fi
}

if tool_selected codex; then
  check_skills "${CODEX_HOME:-$HOME/.codex}/skills"
  check_instructions "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
fi
if tool_selected claude; then
  check_skills "$HOME/.claude/skills"
  check_instructions "$HOME/.claude/CLAUDE.md"
fi
if tool_selected copilot; then
  check_skills "$HOME/.copilot/skills"
  check_instructions "$HOME/.copilot/copilot-instructions.md"
fi
if tool_selected kiro; then
  check_skills "$HOME/.kiro/skills"
  check_instructions "$HOME/.kiro/steering/toby-instructions.md"
fi

if [[ -n "$CONFLICTS" && "$FORCE" -ne 1 ]]; then
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] A real run would stop before writing anything, because of these files:\n%s' "$CONFLICTS"
    printf '[dry-run] Pass --force to replace the skill directories and add the Toby block to those files.\n'
    exit 0
  fi
  printf 'Nothing was installed, because of these files:\n%s' "$CONFLICTS" >&2
  printf 'Pass --force to replace the skill directories and add the Toby block to those files.\n' >&2
  exit 1
fi

if [[ "$TOOL" == "all" || "$TOOL" == "codex" ]]; then
  install_codex
fi
if [[ "$TOOL" == "all" || "$TOOL" == "claude" ]]; then
  install_claude
fi
if [[ "$TOOL" == "all" || "$TOOL" == "copilot" ]]; then
  install_copilot
fi
if [[ "$TOOL" == "all" || "$TOOL" == "kiro" ]]; then
  install_kiro
fi

if [[ "$HOOKS" -eq 1 ]]; then
  install_hooks
fi

printf 'Toby package install complete for --tool %s\n' "$TOOL"
