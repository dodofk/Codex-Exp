"""Tests for the ingestion worker entry points."""
from __future__ import annotations

import json
from pathlib import Path

from ingestion.worker import JobPayload, execute_job


def _build_payload(tmp_path: Path) -> str:
    source = tmp_path / "artifact.bin"
    source.write_bytes(b"demo")
    config = {
        "name": "demo",
        "version": "worker",
        "source_url": "https://example.com/demo",
        "output_dir": str(tmp_path / "data"),
        "artifacts": [
            {"filename": "artifact.bin", "url": source.as_uri()},
        ],
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    payload = {
        "dataset": "demo",
        "config_path": str(config_path),
    }
    return json.dumps(payload)


def test_execute_job_plan_only(tmp_path: Path) -> None:
    payload_json = _build_payload(tmp_path)
    result = execute_job(payload=JobPayload.from_dict(json.loads(payload_json)), plan_only=True)
    assert result["status"] == "planned"
    assert result["plan"]["dataset"] == "demo"
    assert result["plan"]["artifacts"][0]["filename"] == "artifact.bin"


def test_execute_job_run(tmp_path: Path) -> None:
    payload_json = _build_payload(tmp_path)
    payload = JobPayload.from_dict(json.loads(payload_json))
    result = execute_job(payload=payload, plan_only=False)
    assert result["status"] == "completed"

    target = tmp_path / "data" / "demo" / "worker" / "artifact.bin"
    assert target.exists()
