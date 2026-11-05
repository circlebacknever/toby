"""Check that execution fixtures distinguish repairs from incomplete changes."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "execution.py"


REPAIR = '''
def archive_report(report, provider, request_id):
    """Archive a ready report, or raise ArchiveUnavailable without changing it."""
    from time import monotonic
    from .provider import ProviderUnavailable
    started = monotonic()
    if report.state == "archived":
        return report
    if report.state != "ready":
        raise InvalidState("report must be ready")
    try:
        receipt = provider.archive(report.id)
    except ProviderUnavailable as exc:
        emit(logging.ERROR, "report.archive_failed", report_id=report.id,
             request_id=request_id, outcome="failure",
             error_type=type(exc).__name__, duration_ms=(monotonic()-started)*1000)
        raise ArchiveUnavailable("archive unavailable") from exc
    report.archive_id = receipt["receipt"]
    report.state = "archived"
    emit(logging.INFO, "report.archived", report_id=report.id,
         request_id=request_id, outcome="success", duration_ms=(monotonic()-started)*1000)
    return report
'''


class ExecutionChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="toby-execution-test-")
        self.addCleanup(self.temporary.cleanup)
        self.parent = Path(self.temporary.name)

    def prepare(self, case):
        result = subprocess.run(
            [sys.executable, str(RUNNER), "prepare", case, "--parent", str(self.parent),
             "--skills-source", str(ROOT)],
            capture_output=True, text=True, check=True,
        )
        return Path(json.loads(result.stdout)["workspace"])

    def grade(self, case, workspace):
        return subprocess.run(
            [sys.executable, str(RUNNER), "grade", case, str(workspace)],
            capture_output=True, text=True,
        )

    def repair(self, workspace):
        path = workspace / "app" / "reports.py"
        original = ROOT / "evals" / "execution_cases" / "build" / "app" / "reports.py"
        path.write_text(original.read_text() + REPAIR)
        routes = workspace / "app" / "routes.py"
        routes.write_text(routes.read_text().replace(
            '"publish": reports.publish_report,',
            '"publish": reports.publish_report, "archive": reports.archive_report,',
        ))

    def test_prepared_workspace_contains_task_and_snapshot_without_grader(self):
        workspace = self.prepare("build")
        self.assertTrue((workspace / "TASK.md").is_file())
        self.assertEqual((workspace / "AGENTS.md").read_text(), (ROOT / "base/toby.md").read_text())
        self.assertTrue((workspace / ".toby-skills/toby-build/SKILL.md").is_file())
        self.assertFalse((workspace / "execution_grader.py").exists())
        self.assertFalse((workspace / "test_execution.py").exists())

    def test_build_baseline_fails_behavior_checks(self):
        result = self.grade("build", self.prepare("build"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("test_route_archives_a_ready_report", result.stderr)

    def test_bug_baseline_fails_failure_and_diagnostic_checks(self):
        result = self.grade("bug-fix", self.prepare("bug-fix"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("test_provider_failure_preserves_state_and_allows_retry", result.stderr)
        self.assertIn("test_failure_diagnostics_are_emitted_safely", result.stderr)

    def test_complete_repair_passes_both_cases(self):
        for case in ("build", "bug-fix"):
            with self.subTest(case=case):
                workspace = self.prepare(case)
                self.repair(workspace)
                result = self.grade(case, workspace)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_removing_emitted_diagnostics_fails_after_behavior_passes(self):
        workspace = self.prepare("build")
        self.repair(workspace)
        telemetry = workspace / "app" / "telemetry.py"
        telemetry.write_text("def emit(*args, **kwargs):\n    pass\n")
        result = self.grade("build", workspace)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("test_route_archives_a_ready_report", result.stderr)
        self.assertIn("test_success_diagnostics_are_emitted", result.stderr)
        self.assertIn("test_failure_diagnostics_are_emitted_safely", result.stderr)

    def test_candidate_test_edits_cannot_hide_a_broken_operation(self):
        workspace = self.prepare("bug-fix")
        (workspace / "tests" / "test_archive.py").write_text("# Candidate removed its checks.\n")
        result = self.grade("bug-fix", workspace)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("test_provider_failure_preserves_state_and_allows_retry", result.stderr)


if __name__ == "__main__":
    unittest.main()
