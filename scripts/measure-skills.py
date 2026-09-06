#!/usr/bin/env python3
"""Token counts per skill, plus the co-load total for a named group.

Tokens are len(text)/4. That estimate runs low on prose this dense with
backticks, so treat the numbers as a ruler and not as a measurement. It is the
same ruler before and after, which is what the plan needs it for.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"

# The routing groups that co-load in practice. base/toby.md Skill Routing sends
# a normal feature change into the first one.
ROUTING_GROUPS = {
    "feature-change": [
        "toby-swd-strategy",
        "toby-swd-modules",
        "toby-swd-interfaces",
        "toby-swd-complexity",
        "toby-swd-clarity",
        "toby-swd-testing",
        "toby-swd-docs",
    ],
    "review": ["toby-code-review", "toby-simplify-code"],
    "feature-dev": ["toby-feature-dev", "toby-swd-strategy", "toby-swd-testing"],
    "prose": ["toby-voice"],
}


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
    print("co-load totals by routing group (bodies only, no references opened):")
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
