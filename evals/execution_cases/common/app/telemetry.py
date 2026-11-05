"""Emit report events as JSON through the existing stderr logger."""

import json
import logging


class EventFormatter(logging.Formatter):
    def format(self, record):
        """Serialize the event and its explicit diagnostic fields."""
        return json.dumps({"event": record.getMessage(), **getattr(record, "fields", {})})


logger = logging.getLogger("report_service")
logger.setLevel(logging.INFO)
logger.propagate = False
handler = logging.StreamHandler()
handler.setFormatter(EventFormatter())
logger.addHandler(handler)


def emit(level, event, **fields):
    """Write one event with safe fields using the report service logger."""
    logger.log(level, event, extra={"fields": fields})
