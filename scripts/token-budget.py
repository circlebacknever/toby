#!/usr/bin/env python3
"""What a turn actually costs, by what fires.

Tokens are len(text)/4, the same ruler everywhere in this repo. It runs 5 to 15
percent low on prose this dense with backticks, so read the numbers against each
other and not as absolutes.

Three layers:
  resident   in front of every turn, whatever happens
  bodies     a SKILL.md that loaded because its description matched, or that
             an entry skill's body opened by path
  opened     a reference file the skill was told to open

A skill that fires when it should not costs its whole body, which is why
evals/suites/triggering.md counts as much as anything here.
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


# What fires together, drawn from the entry skills' method lists. A member is a
# skill name, whose SKILL.md body counts, or a reference path under skills/,
# which counts as an opened file.
SCENARIOS = {
    "a question, answered": ["toby-explain"],
    "a rename": ["toby-refactor", "toby-swd-clarity"],
    "a command or migration": ["toby-swd-environment"],
    "review my changes": ["toby-code-review"],
    "a throwaway spike": ["toby-swd-experiment"],
    "one method on a repository": ["toby-build", "toby-swd-interfaces", "toby-swd-errors", "toby-swd-testing"],
    "split a module": ["toby-refactor", "toby-swd-strategy", "toby-swd-modules", "toby-swd-docs"],
    "a feature, tactical": ["toby-build", "toby-swd-strategy", "toby-swd-testing"],
    "a feature, strategic": [
        "toby-build", "toby-build/references/strategic.md", "toby-swd-strategy", "toby-swd-modules",
        "toby-swd-interfaces", "toby-swd-errors", "toby-swd-testing", "toby-swd-docs",
    ],
    "a bug fix": ["toby-bug-fix", "toby-swd-testing"],
    "make it faster": ["toby-optimize", "toby-swd-environment"],
    "learning, invoked": ["toby-learning"],
    "a visual artifact": ["toby-artifact-style"],
}


def scenario_cost(members: list[str], parts: dict[str, dict[str, int]]) -> tuple[int, int]:
    """Return the body tokens and the opened-reference tokens for one scenario.

    A member with no folder or file prints a warning. Counting it as 0 would
    report a renamed skill as a saving.
    """
    bodies = opened = 0
    for member in members:
        if "/" in member:
            path = SKILLS / member
            if path.exists():
                opened += read(path)
            else:
                print(f"warning: {member} does not exist, so the scenario leaves it out", file=sys.stderr)
        elif member in parts:
            bodies += parts[member]["body"]
        else:
            print(f"warning: {member} has no folder in skills/, so the scenario leaves it out", file=sys.stderr)
    return bodies, opened


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
    print("WHEN A SKILL FIRES  (bodies, plus the reference files the scenario opens)")
    print(f"  {'scenario':32} {'bodies':>7} {'opened':>7} {'turn':>7}  as % of resident")
    base = guide + descriptions
    costs = {name: scenario_cost(members, parts) for name, members in SCENARIOS.items()}
    for name, (bodies, opened) in costs.items():
        loaded = bodies + opened
        print(f"  {name:32} {bodies:>7} {opened:>7} {base + loaded:>7}  {loaded / base * 100:>5.0f}%")
    print()
    print("VOICE, which loads on any prose turn")
    print(f"  toby-voice body                      {parts['toby-voice']['body']:>7}")
    print(f"  references/plain-language.md         {plain:>7}")
    print(f"  a prose turn adds                    {parts['toby-voice']['body'] + plain:>7}")
    print(f"  references/toby.md, fallback only    {voice_ref:>7}")
    print()
    print("THE EXPENSIVE ONES  (largest reference each skill can open)")
    ranked = sorted(parts.items(), key=lambda kv: -kv[1]["largest_reference"])[:5]
    for name, p in ranked:
        print(f"  {name:32} {p['largest_reference']:>7}   (tree {p['references']})")
    print()
    worst = max(bodies + opened for bodies, opened in costs.values())
    print(f"Worst modelled turn: {base + worst} resident and loaded, opened references included.")
    print(f"A skill firing wrongly costs its whole body. The largest is "
          f"{max(p['body'] for p in parts.values())}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
