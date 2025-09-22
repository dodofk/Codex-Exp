"""CLI surface tests for ingestion tooling."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from ingestion import cli


def _write_config(tmp_path: Path, artifact_path: Path) -> Path:
    config = {
        "name": "demo",
        "version": "local",
        "source_url": "https://example.com/demo",
        "output_dir": str(tmp_path / "data"),
        "artifacts": [
            {"filename": artifact_path.name, "url": artifact_path.as_uri()},
        ],
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def test_cli_plan_renders_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = tmp_path / "artifact.bin"
    payload.write_bytes(b"demo")
    config_path = _write_config(tmp_path, payload)

    exit_code = cli.main([str(config_path), "--plan"])
    assert exit_code == 0

    stdout = capsys.readouterr().out
    assert "Dataset: demo" in stdout
    assert "artifact.bin" in stdout


def test_cli_run_executes_download(tmp_path: Path) -> None:
    payload = tmp_path / "artifact.bin"
    payload.write_bytes(b"demo")
    config_path = _write_config(tmp_path, payload)

    exit_code = cli.main([str(config_path)])
    assert exit_code == 0

    target = tmp_path / "data" / "demo" / "local" / "artifact.bin"
    assert target.exists()
