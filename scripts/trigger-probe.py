#!/usr/bin/env python3
"""Print the routing surface each host tool sees: skill name plus description.

That is the entire input to a load decision, so the trigger evals run against
this and nothing else. Hosts that hide a skill leave it out of their listing.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

# Claude Code and Copilot drop a skill with `disable-model-invocation: true`
# from the listing, and Codex drops one with `policy.allow_implicit_invocation:
# false` in `agents/openai.yaml`. Kiro reads neither field, so it lists every
# skill. The trigger eval reads the listing a host would show.
HOSTS = ["Claude Code", "Codex", "Copilot", "Kiro"]


def hidden_on(host: str, skill_dir: Path) -> bool:
    if host == "Kiro":
        return False
    text = (skill_dir / "SKILL.md").read_text()
    if host == "Codex":
        yaml_path = skill_dir / "agents" / "openai.yaml"
        return yaml_path.exists() and bool(validate.CODEX_HIDE_RE.search(yaml_path.read_text()))
    return validate.frontmatter(text).get("disable-model-invocation") == "true"


def listing(host: str) -> list[str]:
    return [d.name for d in validate.skill_dirs() if not hidden_on(host, d)]


def main() -> int:
    # Hosts that list the same skills share one section, so a reader sees each
    # distinct listing once.
    groups: dict[tuple[str, ...], list[str]] = {}
    for host in HOSTS:
        groups.setdefault(tuple(listing(host)), []).append(host)
    for names, hosts in groups.items():
        print(f"# {', '.join(hosts)}: {len(names)} skills\n")
        for name in names:
            path = REPO_ROOT / "skills" / name / "SKILL.md"
            desc = validate.description_text(path.read_text())
            print(f"### {name}\n{desc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
