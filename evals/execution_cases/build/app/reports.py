"""Define report state changes and their caller-visible failures."""

from dataclasses import dataclass
import logging

from .telemetry import emit


class InvalidState(ValueError):
    """Reject an action that the report's current state doesn't permit."""


class ArchiveUnavailable(RuntimeError):
    """Report that archiving failed and the caller may retry."""


@dataclass
class Report:
    id: str
    state: str = "ready"
    archive_id: str | None = None


def publish_report(report, provider, request_id):
    """Publish a ready report, or raise InvalidState without changing it."""
    if report.state != "ready":
        raise InvalidState("report must be ready")
    report.state = "published"
    emit(logging.INFO, "report.published", report_id=report.id,
         request_id=request_id, outcome="success", duration_ms=0)
    return report
