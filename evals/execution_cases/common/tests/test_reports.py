"""Check the existing publish behavior through its API entry point."""

import unittest

from app.provider import ArchiveProvider
from app.reports import Report
from app.routes import handle


class ReportChecks(unittest.TestCase):
    def test_publish_changes_a_ready_report(self):
        report = Report("report-1")
        result = handle("publish", report, ArchiveProvider(), "request-1")
        self.assertEqual(result["status"], 200)
        self.assertEqual(report.state, "published")

    def test_unknown_action_returns_404(self):
        result = handle("unknown", Report("report-1"), ArchiveProvider(), "request-1")
        self.assertEqual(result["status"], 404)


if __name__ == "__main__":
    unittest.main()
