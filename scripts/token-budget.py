#!/usr/bin/env python3
"""What a turn actually costs, by what fires.

Tokens are len(text)/4, the same ruler everywhere in this repo. It runs 5 to 15
percent low on prose this dense with backticks, so read the numbers against each
other and not as absolutes.

Three layers:
  resident   in front of every turn, whatever happens
  bodies     a SKILL.md that loaded because its description matched
  opened     a reference file the skill was told to open

A skill that fires when it should not costs its whole body, which is why
evals/suites/triggering.md carries as much weight as anything here.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"


def tokens(text: str) -> int:
    return round(len(text) / 4)


def read(path: Path) -> int:
    return tokens(path.read_text()) if path.exists() else 0


def frontmatter_end(text: str) -> int:
    if not text.startswith("---\n"):
        return 0
    end = text.find("\n---", 4)
    return 0 if end < 0 else end + 4


def skill_parts() -> dict[str, dict[str, int]]:
    out = {}
    for d in sorted(SKILLS.iterdir()):
        md = d / "SKILL.md"
        if not md.is_dir() and md.exists():
            text = md.read_text()
            head = frontmatter_end(text)
            refs = sorted((d / "references").rglob("*.md")) if (d / "references").exists() else []
            out[d.name] = {
                "description": tokens(text[:head]),
                "body": tokens(text[head:]),
                "references": sum(tokens(p.read_text()) for p in refs),
                "largest_reference": max((tokens(p.read_text()) for p in refs), default=0),
            }
    return out


# What fires together, drawn from base/toby.md Skill Routing and the eval suite.
SCENARIOS = {
    "a question, answered": ["toby-explain"],
    "a rename": ["toby-swd-clarity"],
    "a command or migration": ["toby-swd-environment"],
    "review my changes": ["toby-code-review"],
    "a throwaway spike": ["toby-swd-experiment"],
    "one method on a repository": ["toby-swd-interfaces", "toby-swd-complexity", "toby-swd-testing"],
    "split a module": ["toby-swd-modules", "toby-swd-strategy", "toby-swd-docs"],
    "a feature, tactical": ["toby-feature-dev", "toby-swd-strategy", "toby-swd-testing"],
    "a feature, strategic": [
        "toby-feature-dev", "toby-swd-strategy", "toby-swd-modules", "toby-swd-interfaces",
        "toby-swd-complexity", "toby-swd-testing", "toby-swd-docs",
    ],
    "learning, invoked": ["toby-learning"],
    "a visual artifact": ["toby-artifact-style"],
}


def main() -> int:
    parts = skill_parts()
    guide = read(REPO_ROOT / "base" / "toby.md")
    style = read(REPO_ROOT / "output-styles" / "toby.md")
    floor = read(REPO_ROOT / "instructions" / "claude" / "CLAUDE-floor.md")
    descriptions = sum(p["description"] for p in parts.values())
    voice_ref = read(SKILLS / "toby-voice" / "references" / "toby.md")
    plain = read(SKILLS / "toby-voice" / "references" / "plain-language.md")

    every_file = sum(
        tokens(p.read_text(errors="ignore"))
        for p in REPO_ROOT.rglob("*.md")
        if ".git" not in p.parts
    )

    print("EVERYTHING ON DISK")
    print(f"  every markdown file in the repo      {every_file:>7}")
    print(f"  all skill bodies                     {sum(p['body'] for p in parts.values()):>7}")
    print(f"  all reference files                  {sum(p['references'] for p in parts.values()):>7}")
    print()
    print("RESIDENT, every turn, before any skill fires")
    print(f"  operating guide                      {guide:>7}")
    print(f"  {len(parts)} skill descriptions               {descriptions:>7}")
    print(f"  default layout total                 {guide + descriptions:>7}")
    print(f"  --output-style layout total          {style + floor + descriptions:>7}"
          f"   ({style + floor - guide:+} against default)")
    print()
    print("WHEN A SKILL FIRES  (bodies only, no reference opened)")
    print(f"  {'scenario':32} {'bodies':>7} {'turn':>7}  as % of resident")
    base = guide + descriptions
    for name, members in SCENARIOS.items():
        bodies = sum(parts[m]["body"] for m in members if m in parts)
        print(f"  {name:32} {bodies:>7} {base + bodies:>7}  {bodies / base * 100:>5.0f}%")
    print()
    print("VOICE, which loads on any prose turn")
    print(f"  toby-voice body                      {parts['toby-voice']['body']:>7}")
    print(f"  references/toby.md, the guide again  {voice_ref:>7}")
    print(f"  references/plain-language.md         {plain:>7}")
    print(f"  a prose turn adds                    {parts['toby-voice']['body'] + voice_ref + plain:>7}")
    print()
    print("THE EXPENSIVE ONES  (largest reference each skill can open)")
    ranked = sorted(parts.items(), key=lambda kv: -kv[1]["largest_reference"])[:5]
    for name, p in ranked:
        print(f"  {name:32} {p['largest_reference']:>7}   (tree {p['references']})")
    print()
    worst = max(sum(parts[m]["body"] for m in ms if m in parts) for ms in SCENARIOS.values())
    print(f"Worst modelled turn: {base + worst} resident and loaded, before a reference opens.")
    print(f"A skill firing wrongly costs its whole body. The largest is "
          f"{max(p['body'] for p in parts.values())}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
