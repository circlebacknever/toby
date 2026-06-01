#!/usr/bin/env bash
# Install the whole package into a throwaway HOME and check every target landed.
# Touches only a temp dir, which it removes on exit. Proves the package installs
# on a fresh machine without trusting prose.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPECTED_PER_TOOL=17
TMP_HOME="$(mktemp -d "${TMPDIR:-/tmp}/toby-install-test.XXXXXX")"
trap 'rm -rf "$TMP_HOME"' EXIT

HOME="$TMP_HOME" CODEX_HOME="$TMP_HOME/.codex" \
  "$ROOT/scripts/install.sh" --tool all --force >/dev/null

fail=0

check_count() {
  local label="$1" dir="$2"
  local count=0
  if [[ -d "$dir" ]]; then
    count="$(find "$dir" -name SKILL.md | wc -l | tr -d ' ')"
  fi
  if [[ "$count" -ne "$EXPECTED_PER_TOOL" ]]; then
    printf 'FAIL %-8s %s SKILL.md files (want %s) in %s\n' "$label" "$count" "$EXPECTED_PER_TOOL" "$dir"
    fail=1
  else
    printf 'ok   %-8s %s skills\n' "$label" "$count"
  fi
}

check_file() {
  local label="$1" path="$2"
  if [[ ! -f "$path" ]]; then
    printf 'FAIL %-8s missing instruction file %s\n' "$label" "$path"
    fail=1
    return
  fi

  if grep -q '<!-- BEGIN TOBY INSTRUCTIONS -->' "$path"; then
    printf 'ok   %-8s instruction marker present\n' "$label"
  else
    printf 'FAIL %-8s instruction marker missing in %s\n' "$label" "$path"
    fail=1
  fi
}

check_count codex   "$TMP_HOME/.codex/skills"
check_count claude  "$TMP_HOME/.claude/skills"
check_count copilot "$TMP_HOME/.copilot/skills"
check_count kiro    "$TMP_HOME/.kiro/skills"

check_file codex   "$TMP_HOME/.codex/AGENTS.md"
check_file claude  "$TMP_HOME/.claude/CLAUDE.md"
check_file copilot "$TMP_HOME/.copilot/copilot-instructions.md"
check_file kiro    "$TMP_HOME/.kiro/steering/toby-instructions.md"

kiro_steering="$TMP_HOME/.kiro/steering/toby-instructions.md"
if [[ -f "$kiro_steering" ]] && grep -q '^inclusion: always$' "$kiro_steering"; then
  printf 'ok   kiro     steering uses inclusion: always\n'
else
  printf 'FAIL kiro     steering missing inclusion: always\n'
  fail=1
fi

total="$(find "$TMP_HOME" -path '*/skills/toby-*/SKILL.md' | wc -l | tr -d ' ')"
if [[ "$total" -ne 68 ]]; then
  printf 'FAIL total    %s SKILL.md files across all tools (want 68)\n' "$total"
  fail=1
else
  printf 'ok   total    68 skill files across four tools\n'
fi

if [[ "$fail" -ne 0 ]]; then
  printf '\nInstall smoke test failed.\n' >&2
  exit 1
fi
printf '\nInstall smoke test passed.\n'
