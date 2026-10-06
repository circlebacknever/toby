#!/usr/bin/env python3
"""Token counts per skill, plus the co-load total for a named group.

Tokens are len(text)/4. That estimate runs low on prose this dense with
backticks, so treat the numbers as a ruler and not as a measurement. It is the
same ruler before and after, which is what the plan needs it for.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"

# The entry chains from validate-skills.py, so the two scripts measure the same
# groups against the same co-load ceiling.
_spec = importlib.util.spec_from_file_location("validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")
_validate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validate)
ROUTING_GROUPS = _validate.ROUTING_GROUPS


def tokens(text: str) -> int:
    return round(len(text) / 4)


def frontmatter_span(text: str) -> int:
    if not text.startswith("---\n"):
        return 0
    end = text.find("\n---", 4)
    return 0 if end < 0 else end + 4


def measure(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text()
    head = frontmatter_span(text)
    refs = sorted((skill_dir / "references").rglob("*.md")) if (skill_dir / "references").exists() else []
    return {
        "name": skill_dir.name,
        "body": tokens(text[head:]),
        "frontmatter": tokens(text[:head]),
        "references": tokens("".join(p.read_text() for p in refs)),
        "reference_files": len(refs),
    }


def main() -> int:
    rows = [measure(d) for d in sorted(SKILLS.iterdir()) if d.is_dir() and (d / "SKILL.md").exists()]
    by_name = {row["name"]: row for row in rows}

    if "--json" in sys.argv:
        print(json.dumps({"skills": rows}, indent=2))
        return 0

    print(f"{'skill':28} {'body':>7} {'front':>7} {'refs':>7} {'files':>6}")
    for row in rows:
        print(
            f"{row['name']:28} {row['body']:>7} {row['frontmatter']:>7} "
            f"{row['references']:>7} {row['reference_files']:>6}"
        )
    print()
    print(f"total body tokens: {sum(r['body'] for r in rows)}")
    print(f"total frontmatter tokens (always resident): {sum(r['frontmatter'] for r in rows)}")
    print()
    print(f"co-load totals by entry chain (bodies only, no references opened, ceiling {_validate.COLOAD_TOKEN_CEILING}):")
    for group, members in ROUTING_GROUPS.items():
        missing = [m for m in members if m not in by_name]
        total = sum(by_name[m]["body"] for m in members if m in by_name)
        note = f"  missing: {', '.join(missing)}" if missing else ""
        print(f"  {group:16} {total:>7}{note}")

    guide = (REPO_ROOT / "base" / "toby.md").read_text()
    print()
    print(f"operating guide: {tokens(guide)} tokens, resident every turn")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
