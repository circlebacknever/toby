"""Define report state changes and their caller-visible failures."""

from dataclasses import dataclass
import logging

from .provider import ProviderUnavailable
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


def archive_report(report, provider, request_id):
    """Archive a ready report, or raise ArchiveUnavailable without changing it."""
    if report.state == "archived":
        return report
    if report.state != "ready":
        raise InvalidState("report must be ready")
    report.state = "archived"
    try:
        report.archive_id = provider.archive(report.id)["receipt"]
    except ProviderUnavailable:
        emit(logging.ERROR, "report.archive_failed")
        return report
    emit(logging.INFO, "report.archived", report_id=report.id,
         request_id=request_id, outcome="success", duration_ms=0)
    return report
