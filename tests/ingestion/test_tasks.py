"""Tests for ingestion task scaffolding."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from ingestion.config import ArtifactSpec, DatasetConfig
from ingestion.tasks import execute, plan_download, render_plan


def _make_artifact(tmp_path: Path, name: str, content: bytes = b"payload", with_hash: bool = False) -> ArtifactSpec:
    source = tmp_path / name
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(content)
    sha = hashlib.sha256(content).hexdigest() if with_hash else None
    return ArtifactSpec(filename=name, url=source.as_uri(), sha256=sha)


def test_plan_download_contains_expected_fields(tmp_path: Path) -> None:
    artifact = _make_artifact(tmp_path, "artifact.bin")
    config = DatasetConfig(
        name="demo",
        version="v1",
        source_url="https://example.com/demo",
        output_dir=tmp_path / "data",
        artifacts=(artifact,),
    )

    plan = plan_download(config)
    assert plan["dataset"] == "demo"
    assert plan["version"] == "v1"
    assert plan["source"].startswith("https://example.com")
    assert plan["target"].endswith("demo/v1")
    assert plan["artifacts"][0]["filename"] == "artifact.bin"

    rendered = render_plan(plan)
    assert "Dataset: demo" in rendered
    assert "artifact.bin" in rendered


def test_execute_downloads_artifact_and_logs(tmp_path: Path) -> None:
    artifact = _make_artifact(tmp_path, "audio/dev.tar.gz", b"demo-bytes")
    config = DatasetConfig(
        name="fleurs",
        version="smoke",
        source_url="https://huggingface.co/datasets/google/fleurs",
        output_dir=tmp_path / "out",
        artifacts=(artifact,),
    )

    execute(config)

    target = tmp_path / "out" / "fleurs" / "smoke" / "audio" / "dev.tar.gz"
    assert target.read_bytes() == b"demo-bytes"

    events_log = tmp_path / "out" / "fleurs" / "logs" / "events.jsonl"
    telemetry_log = tmp_path / "out" / "fleurs" / "logs" / "telemetry.jsonl"
    assert events_log.exists()
    assert telemetry_log.exists()

    events = [json.loads(line) for line in events_log.read_text().splitlines() if line]
    assert any(entry["event"] == "ingestion_start" for entry in events)
    assert any(entry["event"] == "artifact_download_complete" for entry in events)
    assert any(entry["event"] == "ingestion_complete" for entry in events)


def test_execute_skips_existing_verified_artifact(tmp_path: Path) -> None:
    artifact = _make_artifact(tmp_path, "docs/README.md", b"hello", with_hash=True)
    config = DatasetConfig(
        name="fleurs",
        version="v1",
        source_url="https://huggingface.co/datasets/google/fleurs",
        output_dir=tmp_path / "out",
        artifacts=(artifact,),
    )

    execute(config)
    execute(config)  # second run should skip download

    events_log = tmp_path / "out" / "fleurs" / "logs" / "events.jsonl"
    events = [json.loads(line) for line in events_log.read_text().splitlines() if line]
    skip_events = [entry for entry in events if entry["event"] == "artifact_skipped"]
    assert skip_events, "expected artifact_skipped event when rerunning execute"
