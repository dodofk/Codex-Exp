from __future__ import annotations

import json
from pathlib import Path

import pytest

from ingestion.worker import execute_job, JobPayload


def test_compliance_allows_public(tmp_path: Path) -> None:
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "name": "demo",
                "source_url": "http://example.com",
                "output_dir": str(tmp_path / "out"),
                "distribution": "public",
                "artifacts": [
                    {"filename": "sample.txt", "url": "data:text/plain,hello"}
                ],
            }
        ),
        encoding="utf-8",
    )
    payload = JobPayload(dataset="demo", config_path=str(config), artifacts=["sample.txt"])
    result = execute_job(payload, plan_only=True)
    assert result["status"] == "planned"


def test_compliance_blocks_internal(tmp_path: Path) -> None:
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "name": "demo",
                "source_url": "http://example.com",
                "output_dir": str(tmp_path / "out"),
                "distribution": "internal",
                "artifacts": []
            }
        ),
        encoding="utf-8",
    )
    payload = JobPayload(dataset="demo", config_path=str(config))
    with pytest.raises(PermissionError):
        execute_job(payload, plan_only=True)
