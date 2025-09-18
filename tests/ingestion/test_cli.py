from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path

import pytest

from ingestion.cli import build_parser, main
from ingestion.config import load_config
from ingestion.tasks import execute


def _write_json_config(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )


def test_parser_parses_plan_flag(tmp_path: Path) -> None:
    config = tmp_path / "config.yaml"
    _write_json_config(
        config,
        {
            "name": "demo",
            "source_url": "http://example.com",
            "artifacts": [],
        },
    )

    parser = build_parser()
    args = parser.parse_args([str(config), "--plan"])

    assert args.plan is True
    assert args.config == config


def test_main_plan_mode(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    config = tmp_path / "config.yaml"
    _write_json_config(
        config,
        {
            "name": "sample",
            "version": "test",
            "source_url": "http://example.com",
            "artifacts": [],
        },
    )

    exit_code = main([str(config), "--plan"])

    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "Dataset: sample" in captured
    assert "Source URL: http://example.com" in captured


def test_execute_downloads_and_verifies(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    source.write_text("hello ingestion", encoding="utf-8")
    sha = hashlib.sha256(source.read_bytes()).hexdigest()

    config_path = tmp_path / "config.json"
    _write_json_config(
        config_path,
        {
            "name": "demo",
            "version": "test",
            "source_url": "http://example.com",
            "output_dir": str(tmp_path / "outputs"),
            "artifacts": [
                {
                    "filename": "sample.txt",
                    "url": source.as_uri(),
                    "sha256": sha,
                }
            ],
        },
    )

    dataset_config = load_config(config_path)
    execute(dataset_config)

    target = dataset_config.output_dir / dataset_config.name / dataset_config.version / "sample.txt"
    assert target.read_text(encoding="utf-8") == "hello ingestion"

    # Second run should reuse the existing verified artifact without error.
    execute(dataset_config)

    log_file = dataset_config.output_dir / dataset_config.name / "logs" / "events.jsonl"
    entries = [json.loads(line) for line in log_file.read_text(encoding="utf-8").splitlines()]
    assert any(entry["event"] == "artifact_download_complete" for entry in entries)
    assert any(entry["event"] == "ingestion_complete" for entry in entries)
    complete = [e for e in entries if e["event"] == "artifact_download_complete"][-1]
    assert complete["bytes"] > 0


def test_execute_checksum_failure(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    source.write_text("bad checksum", encoding="utf-8")

    config_path = tmp_path / "config.json"
    _write_json_config(
        config_path,
        {
            "name": "demo",
            "version": "test",
            "source_url": "http://example.com",
            "output_dir": str(tmp_path / "outputs"),
            "artifacts": [
                {
                    "filename": "sample.txt",
                    "url": source.as_uri(),
                    "sha256": "deadbeef",
                }
            ],
        },
    )

    dataset_config = load_config(config_path)

    with pytest.raises(ValueError):
        execute(dataset_config)


def test_execute_with_headers_and_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    source.write_text("header world", encoding="utf-8")
    sha = hashlib.sha256(source.read_bytes()).hexdigest()

    config_path = tmp_path / "config.json"
    _write_json_config(
        config_path,
        {
            "name": "demo",
            "version": "headers",
            "source_url": "http://example.com",
            "output_dir": str(tmp_path / "outputs"),
            "artifacts": [
                {
                    "filename": "sample.txt",
                    "url": source.as_uri(),
                    "sha256": sha,
                    "headers": {"Authorization": "Bearer ${TEST_TOKEN}"},
                }
            ],
        },
    )

    calls = []

    class FakeResponse(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            self.close()
            return False

    def fake_urlopen(request, *args, **kwargs):
        calls.append(request.headers.get("Authorization"))
        return FakeResponse(source.read_bytes())

    monkeypatch.setenv("TEST_TOKEN", "abc123")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    dataset_config = load_config(config_path)
    execute(dataset_config)

    assert calls == ["Bearer abc123"]


def test_plan_with_selected_artifact(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config = tmp_path / "config.json"
    _write_json_config(
        config,
        {
            "name": "demo",
            "source_url": "http://example.com",
            "artifacts": [
                {"filename": "a.txt", "url": "http://example.com/a"},
                {"filename": "b.txt", "url": "http://example.com/b"}
            ]
        }
    )

    exit_code = main([str(config), "--plan", "--artifact", "b.txt"])
    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "b.txt" in captured
    assert "a.txt" not in captured
