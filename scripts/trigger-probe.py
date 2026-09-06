#!/usr/bin/env python3
"""Print the routing surface a host tool sees: skill name plus description.

That is the entire input to a load decision, so the trigger evals run against
this and nothing else.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

INCLUDE = [
    "toby-swd-strategy", "toby-swd-modules", "toby-swd-interfaces",
    "toby-swd-complexity", "toby-swd-clarity", "toby-swd-testing",
    "toby-swd-docs", "toby-swd-environment", "toby-swd-experiment",
    "toby-feature-dev", "toby-code-review", "toby-simplify-code",
    # The invoke-only pair. A routing surface that omits them cannot catch them
    # firing, which is the one thing the eval has to prove about them.
    "toby-game", "toby-squall",
    # Both answer questions a working session raises, so a routing surface
    # without them cannot show which one a real learning moment reaches.
    "toby-learning", "toby-explain",
]


def main() -> int:
    for name in INCLUDE:
        path = REPO_ROOT / "skills" / name / "SKILL.md"
        desc = validate.description_text(path.read_text())
        print(f"### {name}\n{desc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
