from __future__ import annotations

from pathlib import Path

from ingestion.logging_utils import log_event


def test_log_event_exports_telemetry(tmp_path: Path) -> None:
    log_event("demo", "test_event", {"value": 1}, tmp_path)
    telemetry = tmp_path / "telemetry.jsonl"
    events = tmp_path / "events.jsonl"
    assert telemetry.exists()
    assert events.exists()
    content = telemetry.read_text(encoding="utf-8").strip()
    assert "test_event" in content
