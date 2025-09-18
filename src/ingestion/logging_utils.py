"""Simple telemetry logging for ingestion runs."""
from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict


def log_event(dataset: str, event: str, payload: Dict[str, Any], root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    entry: Dict[str, Any] = {
        "timestamp": datetime.now(UTC).isoformat(),
        "dataset": dataset,
        "event": event,
    }
    entry.update(payload)
    log_file = root / "events.jsonl"
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
