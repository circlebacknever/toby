#!/usr/bin/env python3
"""Prepare isolated agent tasks and grade their executable report behavior."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
CASES = Path(__file__).resolve().parent / "execution_cases"
GRADER = Path(__file__).resolve().with_name("execution_grader.py")
CASE_DIRECTORIES = {"build": "build", "bug-fix": "bug_fix"}


def prepare(case: str, skills_source: Path, parent: Path) -> dict[str, str]:
    """Copy one baseline and one skill snapshot into a new temporary workspace."""
    guide = skills_source / "base" / "toby.md"
    skills = skills_source / "skills"
    if not guide.is_file() or not skills.is_dir():
        raise ValueError("skills source must contain base/toby.md and skills/")
    workspace = Path(tempfile.mkdtemp(prefix=f"toby-{case}-", dir=parent)).resolve()
    shutil.copytree(CASES / "common", workspace, dirs_exist_ok=True)
    shutil.copytree(CASES / CASE_DIRECTORIES[case], workspace, dirs_exist_ok=True)
    shutil.copyfile(guide, workspace / "AGENTS.md")
    shutil.copytree(skills, workspace / ".toby-skills",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (workspace / ".execution-case").write_text(case + "\n")
    return {"case": case, "workspace": str(workspace), "prompt": str(workspace / "TASK.md")}


def grade(case: str, workspace: Path) -> int:
    """Run checks outside the candidate workspace against its actual behavior."""
    marker = workspace / ".execution-case"
    if not marker.is_file() or marker.read_text().strip() != case:
        raise ValueError("workspace doesn't match the requested execution case")
    result = subprocess.run(
        [sys.executable, str(GRADER), str(workspace.resolve())],
        cwd=workspace, timeout=30,
    )
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("prepare", help="create a fresh fixture and skill snapshot")
    create.add_argument("case", choices=CASE_DIRECTORIES)
    create.add_argument("--skills-source", type=Path, default=ROOT)
    create.add_argument("--parent", type=Path, default=Path("/private/tmp"))
    check = commands.add_parser("grade", help="run independent behavioral and diagnostic checks")
    check.add_argument("case", choices=CASE_DIRECTORIES)
    check.add_argument("workspace", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            print(json.dumps(prepare(args.case, args.skills_source.resolve(), args.parent.resolve())))
            return 0
        return grade(args.case, args.workspace.resolve())
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, f"{exc}\n")


if __name__ == "__main__":
    sys.exit(main())
