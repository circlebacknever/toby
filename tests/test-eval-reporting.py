#!/usr/bin/env python3
"""Check that eval commands distinguish syntax checks from reader understanding."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvalReportingTests(unittest.TestCase):
    def command(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", *arguments], cwd=ROOT, text=True,
            capture_output=True, timeout=20,
        )

    def test_corporate_wording_doesnt_receive_a_readability_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text(
                "The system improves operational efficiency through centralized workflow management.\n"
            )
            result = self.command("scripts/score-voice.py", str(draft))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("defect score 0", result.stdout)
        self.assertIn("syntax checks passed", result.stdout)
        self.assertNotIn("\n  clear\n", result.stdout)

    def test_explanation_judge_requires_source_facts(self):
        result = self.command("evals/run.py", "prompt", "readability-judge")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--facts", result.stderr)

    def test_explanation_judge_compares_understanding_with_facts(self):
        with tempfile.TemporaryDirectory() as directory:
            facts = Path(directory) / "facts.md"
            facts.write_text("A failed upload retries three times.\n")
            result = self.command(
                "evals/run.py", "prompt", "readability-judge", "--facts", str(facts)
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(facts), result.stdout)
        self.assertIn("Misread:", result.stdout)

    def test_isolated_sentence_check_is_explicit(self):
        result = self.command(
            "evals/run.py", "prompt", "readability-judge", "--sentences"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("Misread:", result.stdout)


if __name__ == "__main__":
    unittest.main()
