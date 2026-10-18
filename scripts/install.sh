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
TOOL_SET=0
DRY_RUN=0
FORCE=0
OUTPUT_STYLE=0
HOOKS=0
WRITE_SETTINGS=0
LINK=0
STATUS=0
UNINSTALL=0

# Skills that were renamed or removed. An install deletes these folders from
# each host's skills folder, so a host never lists the old name beside the new name.
RETIRED_SKILLS=(toby-feature-dev toby-simplify-code toby-swd-complexity toby-squall)

usage() {
  printf 'Usage: %s [--tool codex|claude|copilot|github|kiro|all] [--link] [--output-style] [--hooks] [--write-settings] [--status] [--uninstall] [--dry-run] [--force]\n' "$0"
  printf '       github is an alias for copilot (GitHub Copilot CLI, ~/.copilot).\n'
  printf '       Pass comma-separated names to target multiple tools (--tool claude,codex).\n'
  printf '       When --tool is omitted, the installer targets tools whose home folder exists.\n'
  printf '\n'
  printf '  --link            Symlink skill folders and the Claude output style to this\n'
  printf '                    checkout so git pull updates them in place.\n'
  printf '  --hooks           Claude Code only. Install the two voice hooks to\n'
  printf '                    ~/.claude/toby/hooks. When passed without --tool, skips\n'
  printf '                    skill and instruction installation.\n'
  printf '  --write-settings  Claude Code only. Back up ~/.claude/settings.json to\n'
  printf '                    settings.json.bak and merge the voice hook entries.\n'
  printf '  --status          Report whether each tool is installed and in sync with\n'
  printf '                    this checkout. Exits 1 when an installed file differs.\n'
  printf '  --uninstall       Remove Toby skills, hooks, output style, and instruction\n'
  printf '                    marker blocks while keeping surrounding user notes.\n'
  printf '  --force           Replace modified Toby skill directories, and append the\n'
  printf '                    Toby block to instruction files that have no marker block.\n'
  printf '  --output-style    Claude Code only. Install the writing rules as an output\n'
  printf '                    style, and install the shorter CLAUDE.md that leaves them\n'
  printf '                    out. Costs about 200 tokens more than the default, and\n'
  printf '                    puts the rules in the system prompt. You must then turn\n'
  printf '                    the style on: /config, Output style, Toby. Without that\n'
  printf '                    step the voice rules are not loaded at all.\n'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      TOOL_SET=1
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
    --write-settings)
      WRITE_SETTINGS=1
      HOOKS=1
      shift
      ;;
    --link)
      LINK=1
      shift
      ;;
    --status)
      STATUS=1
      shift
      ;;
    --uninstall)
      UNINSTALL=1
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

ALL_TOOLS=(codex claude copilot kiro)

tool_home() {
  case "$1" in
    codex)   printf '%s\n' "${CODEX_HOME:-$HOME/.codex}" ;;
    claude)  printf '%s\n' "$HOME/.claude" ;;
    copilot) printf '%s\n' "$HOME/.copilot" ;;
    kiro)    printf '%s\n' "$HOME/.kiro" ;;
  esac
}

tool_skills_dir() {
  printf '%s/skills\n' "$(tool_home "$1")"
}

tool_instruction_source() {
  case "$1" in
    codex)   printf '%s\n' "$ROOT/AGENTS.md" ;;
    claude)
      if [[ "$OUTPUT_STYLE" -eq 1 ]]; then
        printf '%s\n' "$ROOT/instructions/claude/CLAUDE-floor.md"
      else
        printf '%s\n' "$ROOT/instructions/claude/CLAUDE.md"
      fi
      ;;
    copilot) printf '%s\n' "$ROOT/instructions/copilot/copilot-instructions.md" ;;
    kiro)    printf '%s\n' "$ROOT/instructions/kiro/toby-instructions.md" ;;
  esac
}

tool_instruction_target() {
  local home
  home="$(tool_home "$1")"
  case "$1" in
    codex)   printf '%s/AGENTS.md\n' "$home" ;;
    claude)  printf '%s/CLAUDE.md\n' "$home" ;;
    copilot) printf '%s/copilot-instructions.md\n' "$home" ;;
    kiro)    printf '%s/steering/toby-instructions.md\n' "$home" ;;
  esac
}

tool_instruction_mode() {
  case "$1" in
    kiro) printf 'dedicated\n' ;;
    *)    printf 'merge\n' ;;
  esac
}

SELECTED_TOOLS=()

add_selected_tool() {
  local item="$1" existing
  for existing in "${SELECTED_TOOLS[@]:-}"; do
    [[ "$existing" == "$item" ]] && return
  done
  SELECTED_TOOLS+=("$item")
}

if [[ "$TOOL_SET" -eq 1 ]]; then
  IFS=',' read -ra RAW_TOOLS <<<"$TOOL"
  for raw in "${RAW_TOOLS[@]}"; do
    case "$raw" in
      github)
        add_selected_tool "copilot"
        ;;
      all)
        for candidate in "${ALL_TOOLS[@]}"; do
          add_selected_tool "$candidate"
        done
        ;;
      codex|claude|copilot|kiro)
        add_selected_tool "$raw"
        ;;
      *)
        usage >&2
        exit 2
        ;;
    esac
  done
elif [[ "$STATUS" -eq 1 || "$UNINSTALL" -eq 1 ]]; then
  SELECTED_TOOLS=("${ALL_TOOLS[@]}")
elif [[ "$HOOKS" -eq 1 && "$OUTPUT_STYLE" -eq 0 && "$LINK" -eq 0 ]]; then
  SELECTED_TOOLS=()
elif [[ "$OUTPUT_STYLE" -eq 1 ]]; then
  SELECTED_TOOLS=(claude)
else
  for candidate in "${ALL_TOOLS[@]}"; do
    if [[ -d "$(tool_home "$candidate")" ]]; then
      add_selected_tool "$candidate"
    fi
  done
  if [[ "${#SELECTED_TOOLS[@]}" -eq 0 ]]; then
    SELECTED_TOOLS=("${ALL_TOOLS[@]}")
  fi
fi

tool_selected() {
  local needle="$1" item
  for item in "${SELECTED_TOOLS[@]:-}"; do
    [[ "$item" == "$needle" ]] && return 0
  done
  return 1
}

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

write_skill_manifest() {
  local dest="$1"
  local manifest
  manifest="$(dirname "$dest")/.toby-manifest"
  python3 - "$dest" "$manifest" <<'PY'
import hashlib
import sys
from pathlib import Path

dest = Path(sys.argv[1])
manifest = Path(sys.argv[2])
rows = []
if dest.is_dir():
    for skill in sorted(dest.glob("toby-*")):
        if not skill.is_dir() or skill.is_symlink():
            continue
        digest = hashlib.sha256()
        for path in sorted(skill.rglob("*")):
            if path.is_file() and ".DS_Store" not in path.parts and "__pycache__" not in path.parts:
                rel = path.relative_to(skill).as_posix().encode()
                digest.update(rel + b"\0" + path.read_bytes() + b"\0")
        rows.append(f"{skill.name}\t{digest.hexdigest()}")
manifest.write_text("\n".join(rows) + ("\n" if rows else ""))
PY
}

# Return 0 when the installed skill folder matches a symlink to the repo skill,
# matches the repo skill contents, matches blobs in git history, or matches
# the digest recorded in .toby-manifest.
skill_is_unmodified() {
  local repo_skill="$1"
  local target="$2"
  local manifest="$3"

  if [[ -L "$target" ]]; then
    [[ "$(readlink "$target")" == "$repo_skill" ]]
    return
  fi
  if [[ ! -d "$target" ]]; then
    return 1
  fi
  if diff -r -x .DS_Store -x __pycache__ "$repo_skill" "$target" >/dev/null 2>&1; then
    return 0
  fi
  python3 - "$ROOT" "$target" "$manifest" <<'PY'
import hashlib
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
target = Path(sys.argv[2])
manifest = Path(sys.argv[3])

files = [
    path
    for path in sorted(target.rglob("*"))
    if path.is_file() and ".DS_Store" not in path.parts and "__pycache__" not in path.parts
]
if not files:
    raise SystemExit(1)

if manifest.is_file():
    recorded = {}
    for line in manifest.read_text().splitlines():
        if "\t" in line:
            name, digest = line.split("\t", 1)
            recorded[name] = digest.strip()
    expected = recorded.get(target.name)
    if expected:
        digest = hashlib.sha256()
        for path in files:
            rel = path.relative_to(target).as_posix().encode()
            digest.update(rel + b"\0" + path.read_bytes() + b"\0")
        if digest.hexdigest() == expected:
            raise SystemExit(0)

if (root / ".git").exists():
    hashed = subprocess.run(
        ["git", "-C", str(root), "hash-object", *[str(f) for f in files]],
        capture_output=True,
        text=True,
    )
    if hashed.returncode == 0:
        checked = subprocess.run(
            ["git", "-C", str(root), "cat-file", "--batch-check"],
            input=hashed.stdout,
            capture_output=True,
            text=True,
        )
        if checked.returncode == 0 and all(
            line.split()[1] == "blob" for line in checked.stdout.splitlines() if line.strip()
        ):
            raise SystemExit(0)

raise SystemExit(1)
PY
}

install_skills() {
  local dest="$1"
  run mkdir -p "$dest"

  local retired
  for retired in "${RETIRED_SKILLS[@]}"; do
    if [[ -e "$dest/$retired" || -L "$dest/$retired" ]]; then
      run rm -rf "$dest/$retired"
    fi
  done

  local skill
  for skill in "$ROOT"/skills/toby-*; do
    [[ -d "$skill" ]] || continue
    local name
    name="$(basename "$skill")"
    local target="$dest/$name"

    if [[ -e "$target" || -L "$target" ]]; then
      run rm -rf "$target"
    fi
    if [[ "$LINK" -eq 1 ]]; then
      run ln -s "$skill" "$target"
    else
      run cp -R "$skill" "$target"
      # Finder drops .DS_Store into any folder it opens, and Python can leave
      # __pycache__ behind. Keep both out of the install.
      run find "$target" \( -name .DS_Store -o -name __pycache__ \) -prune -exec rm -rf {} +
    fi
  done

  if [[ "$DRY_RUN" -eq 0 && "$LINK" -eq 0 ]]; then
    write_skill_manifest "$dest"
  fi
}

merge_claude_settings() {
  local kit="$1"
  local settings="$HOME/.claude/settings.json"
  run mkdir -p "$(dirname "$settings")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] merge voice hooks into %s\n' "$settings"
    return
  fi
  python3 - "$settings" "$kit" <<'PY'
import json
import shutil
import sys
from pathlib import Path

settings_path = Path(sys.argv[1])
kit = sys.argv[2]

if settings_path.exists():
    shutil.copy2(settings_path, settings_path.with_suffix(".json.bak"))
    data = json.loads(settings_path.read_text())
else:
    data = {}

hooks = data.setdefault("hooks", {})
write_cmd = f"python3 {kit}/hooks/voice-write-check.py"
stop_cmd = f"python3 {kit}/hooks/voice-stop-check.py"

post_list = hooks.setdefault("PostToolUse", [])
if not any(
    isinstance(entry, dict)
    and any(h.get("command") == write_cmd for h in entry.get("hooks", []) if isinstance(h, dict))
    for entry in post_list
):
    post_list.append(
        {
            "matcher": "Write|Edit",
            "hooks": [{"type": "command", "command": write_cmd}],
        }
    )

stop_list = hooks.setdefault("Stop", [])
if not any(
    isinstance(entry, dict)
    and any(h.get("command") == stop_cmd for h in entry.get("hooks", []) if isinstance(h, dict))
    for entry in stop_list
):
    stop_list.append(
        {
            "hooks": [{"type": "command", "command": stop_cmd}],
        }
    )

settings_path.write_text(json.dumps(data, indent=2) + "\n")
PY
}

install_hooks() {
  # The hooks only. The write hook runs the checker from the installed
  # toby-voice skill, so the checker is not copied here.
  local kit="$HOME/.claude/toby"
  local checker="$HOME/.claude/skills/toby-voice/scripts/voice-check.py"
  run mkdir -p "$kit/hooks"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] install the voice hooks to %s/hooks\n' "$kit"
    if [[ "$WRITE_SETTINGS" -eq 1 ]]; then
      merge_claude_settings "$kit"
    fi
    return
  fi
  run cp "$ROOT/hooks/voice-stop-check.py" "$kit/hooks/"
  run cp "$ROOT/hooks/voice-write-check.py" "$kit/hooks/"

  printf '\nvoice hooks installed to %s/hooks\n' "$kit"
  if [[ ! -f "$checker" ]]; then
    printf 'The write hook needs %s.\n' "$checker"
    printf 'Run this installer with --tool claude to install it.\n'
  fi
  if [[ "$WRITE_SETTINGS" -eq 1 ]]; then
    merge_claude_settings "$kit"
    printf 'Updated %s/.claude/settings.json (backup at settings.json.bak).\n\n' "$HOME"
    return
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
  printf '\nPass --hooks --write-settings to merge this block automatically,\n'
  printf 'or paste it into settings.json yourself.\n\n'
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
  if [[ -e "$target" || -L "$target" ]]; then
    run rm -f "$target"
  fi
  if [[ "$LINK" -eq 1 ]]; then
    run ln -s "$ROOT/output-styles/toby.md" "$target"
  else
    run cp "$ROOT/output-styles/toby.md" "$target"
  fi
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

install_tool() {
  local tool="$1"
  install_skills "$(tool_skills_dir "$tool")"
  install_instruction_file "$(tool_instruction_source "$tool")" "$(tool_instruction_target "$tool")" "$(tool_instruction_mode "$tool")"
  if [[ "$tool" == "claude" ]]; then
    if [[ "$OUTPUT_STYLE" -eq 1 ]]; then
      install_output_style
    elif [[ -e "$HOME/.claude/output-styles/toby.md" || -L "$HOME/.claude/output-styles/toby.md" ]]; then
      run rm -f "$HOME/.claude/output-styles/toby.md"
      printf 'Removed %s so Claude Code does not load the writing rules twice.\n' "$HOME/.claude/output-styles/toby.md"
      printf 'If Output style is still set to Toby in /config, switch it back to Default.\n'
    fi
  fi
}

run_status() {
  local exit_code=0
  local candidate
  for candidate in "${SELECTED_TOOLS[@]:-}"; do
    local skills_dir instr_target instr_source
    skills_dir="$(tool_skills_dir "$candidate")"
    instr_target="$(tool_instruction_target "$candidate")"
    if [[ "$candidate" == "claude" && ( -f "$HOME/.claude/output-styles/toby.md" || -L "$HOME/.claude/output-styles/toby.md" ) ]]; then
      instr_source="$ROOT/instructions/claude/CLAUDE-floor.md"
    else
      instr_source="$(tool_instruction_source "$candidate")"
    fi
    if ! python3 - "$candidate" "$ROOT" "$skills_dir" "$instr_target" "$instr_source" "$HOME" <<'PY'
import re
import sys
from pathlib import Path

label, root, skills_dir, instr_target, instr_source, home = (
    sys.argv[1],
    Path(sys.argv[2]),
    Path(sys.argv[3]),
    Path(sys.argv[4]),
    Path(sys.argv[5]),
    Path(sys.argv[6]),
)

block_re = re.compile(
    r"<!-- BEGIN TOBY INSTRUCTIONS -->\n?(.*?)\n?<!-- END TOBY INSTRUCTIONS -->",
    re.S,
)

repo_skills = sorted(p for p in (root / "skills").glob("toby-*") if p.is_dir())
installed_any = skills_dir.exists() and any(skills_dir.glob("toby-*"))
has_marker = instr_target.is_file() and bool(block_re.search(instr_target.read_text()))

if not installed_any and not has_marker:
    print(f"{label}: not installed")
    raise SystemExit(0)

reasons = []
for repo_skill in repo_skills:
    inst = skills_dir / repo_skill.name
    if not inst.exists():
        reasons.append(f"{repo_skill.name} missing")
        continue
    repo_rels = {
        path.relative_to(repo_skill)
        for path in repo_skill.rglob("*")
        if path.is_file() and ".DS_Store" not in path.parts and "__pycache__" not in path.parts
    }
    inst_rels = {
        path.relative_to(inst)
        for path in inst.rglob("*")
        if path.is_file() and ".DS_Store" not in path.parts and "__pycache__" not in path.parts
    }
    if repo_rels != inst_rels or any(
        (inst / rel).read_bytes() != (repo_skill / rel).read_bytes() for rel in repo_rels
    ):
        reasons.append(f"{repo_skill.name} modified")

if not has_marker:
    reasons.append("instruction block missing")
else:
    expected = block_re.search(instr_source.read_text()).group(1).strip()
    actual = block_re.search(instr_target.read_text()).group(1).strip()
    if actual != expected:
        reasons.append("instruction block modified")

if label == "claude":
    style = home / ".claude" / "output-styles" / "toby.md"
    if style.exists() and style.read_text() != (root / "output-styles" / "toby.md").read_text():
        reasons.append("output style modified")
    hooks_dir = home / ".claude" / "toby" / "hooks"
    if hooks_dir.exists():
        for hook_name in ("voice-write-check.py", "voice-stop-check.py"):
            hook_file = hooks_dir / hook_name
            if not hook_file.is_file() or hook_file.read_bytes() != (root / "hooks" / hook_name).read_bytes():
                reasons.append(f"{hook_name} modified")

if reasons:
    print(f"{label}: out of sync ({', '.join(reasons[:5])})")
    raise SystemExit(1)

print(f"{label}: in sync")
PY
    then
      exit_code=1
    fi
  done
  exit "$exit_code"
}

run_uninstall() {
  local candidate
  for candidate in "${SELECTED_TOOLS[@]:-}"; do
    local skills_dir home instr_target mode
    home="$(tool_home "$candidate")"
    skills_dir="$(tool_skills_dir "$candidate")"
    instr_target="$(tool_instruction_target "$candidate")"
    mode="$(tool_instruction_mode "$candidate")"

    if [[ -d "$skills_dir" ]]; then
      local installed_skill
      for installed_skill in "$skills_dir"/toby-*; do
        [[ -e "$installed_skill" || -L "$installed_skill" ]] || continue
        run rm -rf "$installed_skill"
      done
    fi
    if [[ -f "$home/.toby-manifest" ]]; then
      run rm -f "$home/.toby-manifest"
    fi
    if [[ -f "$instr_target" ]]; then
      if [[ "$DRY_RUN" -eq 1 ]]; then
        printf '[dry-run] remove Toby instruction block from %s\n' "$instr_target"
      else
        python3 - "$instr_target" "$mode" <<'PY'
import re
import sys
from pathlib import Path

target = Path(sys.argv[1])
mode = sys.argv[2]
text = target.read_text()
block_re = re.compile(
    r"\n?<!-- BEGIN TOBY INSTRUCTIONS -->\n?.*?\n?<!-- END TOBY INSTRUCTIONS -->\n?",
    re.S,
)
if not block_re.search(text):
    raise SystemExit(0)
if mode == "dedicated":
    target.unlink()
    raise SystemExit(0)
remaining = block_re.sub("\n", text).strip()
if remaining:
    target.write_text(remaining + "\n")
else:
    target.unlink()
PY
      fi
    fi
    if [[ "$candidate" == "claude" ]]; then
      if [[ -e "$HOME/.claude/output-styles/toby.md" || -L "$HOME/.claude/output-styles/toby.md" ]]; then
        run rm -f "$HOME/.claude/output-styles/toby.md"
      fi
      if [[ -d "$HOME/.claude/toby" ]]; then
        run rm -rf "$HOME/.claude/toby"
      fi
      if [[ -f "$HOME/.claude/settings.json" && "$DRY_RUN" -eq 0 ]]; then
        python3 - "$HOME/.claude/settings.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
try:
    data = json.loads(path.read_text())
except Exception:
    raise SystemExit(0)
hooks = data.get("hooks")
if not isinstance(hooks, dict):
    raise SystemExit(0)
for event in ("PostToolUse", "Stop"):
    entries = hooks.get(event)
    if not isinstance(entries, list):
        continue
    kept = []
    for entry in entries:
        if not isinstance(entry, dict):
            kept.append(entry)
            continue
        cmds = [
            h for h in entry.get("hooks", [])
            if not (isinstance(h, dict) and ("voice-write-check.py" in h.get("command", "") or "voice-stop-check.py" in h.get("command", "")))
        ]
        if cmds:
            entry = dict(entry)
            entry["hooks"] = cmds
            kept.append(entry)
    if kept:
        hooks[event] = kept
    else:
        hooks.pop(event, None)
if not hooks:
    data.pop("hooks", None)
path.write_text(json.dumps(data, indent=2) + "\n")
PY
      fi
    fi
  done
  printf 'Toby uninstall complete.\n'
  exit 0
}

if [[ "$STATUS" -eq 1 ]]; then
  run_status
fi

if [[ "$UNINSTALL" -eq 1 ]]; then
  run_uninstall
fi

# Check every target before writing anything. A refusal partway through an
# install leaves some tools updated and others stale, so report every conflict
# at once and stop while nothing has changed.
CONFLICTS=""

check_skills() {
  local dest="$1" skill target manifest
  manifest="$(dirname "$dest")/.toby-manifest"
  for skill in "$ROOT"/skills/toby-*; do
    [[ -d "$skill" ]] || continue
    target="$dest/$(basename "$skill")"
    if [[ -e "$target" || -L "$target" ]]; then
      if ! skill_is_unmodified "$skill" "$target" "$manifest"; then
        CONFLICTS+="  skill directory already exists: $target"$'\n'
      fi
    fi
  done
}

check_instructions() {
  local target="$1"
  if [[ -f "$target" ]] && ! grep -q '<!-- BEGIN TOBY INSTRUCTIONS -->' "$target"; then
    CONFLICTS+="  instruction file has no Toby marker block: $target"$'\n'
  fi
}

for candidate in "${ALL_TOOLS[@]}"; do
  if tool_selected "$candidate"; then
    check_skills "$(tool_skills_dir "$candidate")"
    check_instructions "$(tool_instruction_target "$candidate")"
  fi
done

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

for candidate in "${ALL_TOOLS[@]}"; do
  if tool_selected "$candidate"; then
    install_tool "$candidate"
  fi
done

if [[ "$HOOKS" -eq 1 ]]; then
  install_hooks
fi

if [[ "${#SELECTED_TOOLS[@]}" -eq 0 ]]; then
  printf 'Toby hooks install complete.\n'
elif [[ "$TOOL_SET" -eq 1 ]]; then
  printf 'Toby package install complete for --tool %s\n' "$TOOL"
else
  IFS=','
  printf 'Toby package install complete for --tool %s\n' "${SELECTED_TOOLS[*]}"
  unset IFS
fi
