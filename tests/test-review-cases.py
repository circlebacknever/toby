#!/usr/bin/env python3
"""Check that review grading rejects missing evidence, duplicates, and incomplete judgments."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("review_cases", ROOT / "evals" / "review_cases.py")
review_cases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review_cases)


class GradingTests(unittest.TestCase):
    def setUp(self):
        self.gold = {"cases": [
            {"id": "amount", "path": "parcel/billing.py"},
            {"id": "tenant", "path": "parcel/orders.py"},
        ]}

    def finding(self, path="parcel/billing.py", body=None):
        body = body or ("For 199 cents, tax drops cents before multiplication, so the total is too low. "
                        "Round the tax after multiplication.")
        return {"path": path, "line": 5, "body": body}

    def decision(self, index=1, match="amount", quote="tax drops cents"):
        return {"finding": index, "match": match, "quote": quote,
                "reason": "The finding describes the same failure mechanism.",
                "evidence": {"trigger": "199 cents", "mechanism": "tax drops cents before multiplication",
                             "consequence": "total is too low", "repair": "Round the tax after multiplication"}}

    def test_missing_finding_fails_even_when_reported_finding_matches(self):
        result = review_cases.grade(
            {"findings": [self.finding()]},
            {"decisions": [self.decision()]}, self.gold)
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["false_negatives"], 1)
        self.assertFalse(result["pass"])

    def test_duplicate_finding_is_penalized(self):
        result = review_cases.grade(
            {"findings": [self.finding(), self.finding()]},
            {"decisions": [self.decision(), self.decision(2)]}, self.gold)
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["score"], -1)

    def test_unmatched_guarded_claim_is_false_positive(self):
        review = {"findings": [self.finding("parcel/admin.py", "SQL interpolates a user table.")]}
        judgment = {"decisions": [self.decision(match=None, quote="SQL interpolates")]}
        result = review_cases.grade(review, judgment, self.gold)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["true_positives"], 0)

    def test_every_finding_requires_its_own_judgment(self):
        with self.assertRaisesRegex(ValueError, "each finding exactly once"):
            review_cases.grade({"findings": [self.finding()]}, {"decisions": []}, self.gold)

    def test_missing_quote_and_invented_quote_are_rejected(self):
        for quote in ["", "An explanation the writer never gave"]:
            with self.subTest(quote=quote), self.assertRaisesRegex(ValueError, "exact finding quote"):
                review_cases.grade({"findings": [self.finding()]},
                                   {"decisions": [self.decision(quote=quote)]}, self.gold)

    def test_wrong_root_cause_file_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "different root-cause file"):
            review_cases.grade({"findings": [self.finding("parcel/orders.py")]},
                               {"decisions": [self.decision()]}, self.gold)

    def test_citation_outside_file_is_rejected(self):
        finding = self.finding()
        finding["line"] = 999
        with self.assertRaisesRegex(ValueError, "outside the reviewed file"):
            review_cases.grade({"findings": [finding]},
                               {"decisions": [self.decision()]}, self.gold)

    def test_location_or_category_without_the_findings_own_explanation_cannot_match(self):
        decision = self.decision(quote="arithmetic")
        with self.assertRaisesRegex(ValueError, "requires its own trigger evidence"):
            review_cases.grade({"findings": [self.finding(body="arithmetic")]},
                               {"decisions": [decision]}, self.gold)

    def test_complete_independent_matches_pass(self):
        second = self.finding("parcel/orders.py", "For another account's order, the account predicate is gone, "
                              "so private data is returned. Restore account scoping.")
        decision = self.decision(2, "tenant", "account predicate is gone")
        decision["evidence"] = {"trigger": "another account's order", "mechanism": "account predicate is gone",
                                "consequence": "private data is returned", "repair": "Restore account scoping"}
        result = review_cases.grade({"findings": [self.finding(), second]},
                                    {"decisions": [self.decision(), decision]}, self.gold)
        self.assertEqual(result["precision"], 1)
        self.assertEqual(result["recall"], 1)
        self.assertTrue(result["pass"])

    def test_clean_review_passes_without_inventing_a_recall_rate(self):
        result = review_cases.grade({"findings": []}, {"decisions": []}, {"cases": []})
        self.assertTrue(result["pass"])
        self.assertIsNone(result["recall"])
        self.assertEqual(result["false_positives"], 0)


class FixtureIntegrityTests(unittest.TestCase):
    def test_prepared_reviewer_tree_excludes_authoring_and_gold(self):
        with tempfile.TemporaryDirectory(prefix="review-integrity-") as directory:
            destination = Path(directory) / "review"
            review_cases.prepare(destination)
            files = {path.relative_to(destination).as_posix()
                     for path in destination.rglob("*") if path.is_file()}
            self.assertNotIn("gold.json", files)
            self.assertNotIn("fixture.py", files)
            self.assertFalse(any(path.startswith("evals/") for path in files))
            self.assertIn("change.diff", files)
            self.assertIn("after/parcel/inventory.py", files)
            self.assertIn("skills/toby-code-review/SKILL.md", files)
            self.assertNotIn("gold", (destination / "TASK.md").read_text().split("Don't inspect")[0])

    def test_preparation_rejects_an_existing_destination(self):
        with tempfile.TemporaryDirectory(prefix="review-existing-") as directory:
            with self.assertRaisesRegex(ValueError, "already exists"):
                review_cases.prepare(Path(directory))

    def test_preparation_uses_the_selected_instruction_snapshot(self):
        with tempfile.TemporaryDirectory(prefix="review-snapshot-") as directory:
            snapshot = Path(directory) / "snapshot"
            (snapshot / "base").mkdir(parents=True)
            (snapshot / "base" / "toby.md").write_text("Selected operating guide.\n")
            skill = snapshot / "skills" / "toby-code-review"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Selected reviewer instructions.\n")
            destination = Path(directory) / "review"
            review_cases.prepare(destination, snapshot)
            self.assertEqual((destination / "GUIDE.md").read_text(), "Selected operating guide.\n")
            self.assertEqual((destination / "skills" / "toby-code-review" / "SKILL.md").read_text(),
                             "Selected reviewer instructions.\n")

    def test_each_gold_probe_matches_a_changed_source_file(self):
        fixture = review_cases.load_fixture()
        changed = fixture.changed_files()
        gold = json.loads((review_cases.CASES / "gold.json").read_text())
        self.assertEqual(set(review_cases.PROBES), {case["probe"] for case in gold["cases"]})
        for case in gold["cases"]:
            with self.subTest(case=case["id"]):
                self.assertNotEqual(fixture.BASE[case["path"]], changed[case["path"]])

    def test_clean_preparation_excludes_every_seeded_regression(self):
        fixture = review_cases.load_fixture()
        gold = json.loads((review_cases.CASES / "gold.json").read_text())
        with tempfile.TemporaryDirectory(prefix="review-clean-") as directory:
            destination = Path(directory) / "review"
            review_cases.prepare(destination, clean=True)
            for case in gold["cases"]:
                with self.subTest(case=case["id"]):
                    path = destination / "after" / case["path"]
                    self.assertEqual(path.read_text(), fixture.BASE[case["path"]])
            self.assertNotEqual((destination / "before/parcel/admin.py").read_text(),
                                (destination / "after/parcel/admin.py").read_text())


if __name__ == "__main__":
    unittest.main()
