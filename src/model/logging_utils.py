"""Logging helpers for model training telemetry."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from telemetry.exporter import emit_event as export_event


def log_event(run_id: str, event: str, payload: Mapping[str, Any], log_path: Path) -> None:
    """Append a structured event to the metrics log and telemetry stream."""

    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {"event": event, "timestamp": timestamp, **payload}
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False))
        handle.write("\n")
    export_event(run_id, event, {**payload, "timestamp": timestamp}, log_path.parent)


__all__ = ["log_event"]
