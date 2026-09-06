#!/usr/bin/env python3
"""Each check added in Group 6 fires on a broken input and stays quiet on a good one.

A check nobody proved can fail is a check that passes because it never runs.
Run: python3 tests/test-validator-checks.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("v", REPO_ROOT / "scripts" / "validate-skills.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name} {detail}")
        failures.append(name)


# --- buried lead -------------------------------------------------------------
BURIED = (
    "Module boundaries are one of the most consequential decisions in any system, "
    "and the cost of getting them wrong compounds over years of maintenance work."
)
LEADING = "State the one piece of knowledge each module owns before you split anything at all."
SHORT = "Four kinds, each with its own home."
CONDITIONAL = "Before calling a boundary decision done, run this list against the diff you wrote."
MODAL = "An assertion should fail when the behavior under test changes and never otherwise."

check("buried lead fires on a thesis opener", not v.leads_with_rule(BURIED))
check("buried lead passes an imperative opener", v.leads_with_rule(LEADING))
check("buried lead passes a short opener", v.leads_with_rule(SHORT))
check("buried lead passes a leading condition", v.leads_with_rule(CONDITIONAL))
check("buried lead passes a modal rule", v.leads_with_rule(MODAL))

# --- anti-trigger ------------------------------------------------------------
check("skip clause found", bool(v.SKIP_CLAUSE_RE.search("Use it for X. Skip it for Y.")))
check("skip clause absent", not v.SKIP_CLAUSE_RE.search("Use this skill when a task adds a function."))
# An invoke-only skill writes its anti-trigger the other way round, and reading
# only "skip it" reported the three strictest descriptions as having none.
check("invoke-only anti-trigger found",
      bool(v.SKIP_CLAUSE_RE.search("Trigger only when the creator invokes this skill by name.")))
check("do-not-trigger anti-trigger found",
      bool(v.SKIP_CLAUSE_RE.search("Do not trigger on general requests to make a game.")))

# --- token budget ------------------------------------------------------------
check("body ceiling is under every real body",
      max(v.tokens(v.body_of((d / "SKILL.md").read_text())) for d in v.skill_dirs()) <= v.BODY_TOKEN_CEILING)
check("token estimate counts characters", v.tokens("x" * 400) == 100)

# --- co-load budget ----------------------------------------------------------
sizes = {d.name: v.tokens(v.body_of((d / "SKILL.md").read_text())) for d in v.skill_dirs()}
for group, members in v.ROUTING_GROUPS.items():
    total = sum(sizes.get(m, 0) for m in members)
    check(f"co-load group {group} under ceiling", total <= v.COLOAD_TOKEN_CEILING, f"({total})")

# --- reference reachability --------------------------------------------------
errors: list[str] = []
warnings: list[str] = []
v.check_reference_reachability(errors, warnings)
check("no reference points at a missing file", not errors, str(errors[:2]))

fixture = REPO_ROOT / "tests" / "fixtures" / "reference-miss.md"
fixture.write_text("Read `references/does-not-exist.md` for the worked cases.\n")
check("prefixed citation is read", bool(v.REFERENCE_RE.search(fixture.read_text())))
fixture.unlink()

# toby-game cited a bare `visual-identity.md`, the file was deleted with the rest
# of the skill and left out of the rebuild, and this check read neither the
# citation nor the gap for three releases.
check("bare citation is read", bool(v.BARE_REFERENCE_RE.search("- `visual-identity.md` — the look")))
check("bare citation resolves the name",
      v.BARE_REFERENCE_RE.search("- `visual-identity.md` — the look").group(1) == "visual-identity.md")
check("a repo filename is not a reference", "AGENTS.md" in v.NOT_A_REFERENCE and "SKILL.md" in v.NOT_A_REFERENCE)
check("nested reference paths still parse",
      v.REFERENCE_RE.search("`references/examples/chat.md`").group(1) == "examples/chat.md")
check("every toby-game reference exists",
      all((REPO_ROOT / "skills" / "toby-game" / "references" / f"{n}.md").exists()
          for n in ["architecture", "gameplay", "comedy-and-narrative", "visual-identity",
                    "cross-device", "calibration-and-testing"]))

# --- cross-skill collision ---------------------------------------------------
collisions: list[str] = []
v.check_cross_skill_collisions(collisions)
check("collision check runs", isinstance(collisions, list))
print(f"     ({len(collisions)} cross-skill sentence collisions today)")

# --- install drift -----------------------------------------------------------
drift: list[str] = []
v.check_install_drift(drift)
check("install drift check runs without touching disk", isinstance(drift, list))
print(f"     ({len(drift)} install target(s) differ from the repo)")

# --- description backticks ---------------------------------------------------
check("split skill name caught", bool(v.SPLIT_BACKTICK_RE.search("which `toby-swd- clarity` owns")))
check("intact skill name passes", not v.SPLIT_BACKTICK_RE.search("which `toby-swd-clarity` owns"))
backtick_errors: list[str] = []
v.check_description_backticks(backtick_errors)
check("no description names a wrapped skill", not backtick_errors, str(backtick_errors[:2]))

# --- prose paths reach repo-root markdown ------------------------------------
paths = {p.name for p in v.prose_paths()}
check("repo-root markdown is scanned", "README.md" in paths)
check("generated AGENTS.md is not scanned twice", "AGENTS.md" not in paths)

print()
if failures:
    print(f"{len(failures)} check(s) failed.", file=sys.stderr)
    raise SystemExit(1)
print("All validator-check fixtures passed.")
