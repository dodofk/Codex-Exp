from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from ingestion.worker import JobPayload, build_parser, load_payload, main


def test_load_payload_from_file(tmp_path: Path) -> None:
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps({"dataset": "fleurs"}), encoding="utf-8")
    payload = load_payload(payload_file, None)
    assert payload.dataset == "fleurs"


def test_load_payload_from_string() -> None:
    payload = load_payload(None, json.dumps({"dataset": "covost2", "artifacts": ["README.md"]}))
    assert list(payload.artifacts or []) == ["README.md"]


def test_cli_plan_mode(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"dataset": "fleurs"}), encoding="utf-8")

    exit_code = main(["--payload", str(payload), "--plan"])
    assert exit_code == 0
    captured = capsys.readouterr().out
    assert "Dataset:" in captured


def test_cli_run_executes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = tmp_path / "source.txt"
    source.write_text("worker run", encoding="utf-8")
    sha = hashlib.sha256(source.read_bytes()).hexdigest()

    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
                {
                    "name": "demo",
                    "version": "subset",
                    "output_dir": str(tmp_path / "outputs"),
                    "source_url": "http://example.com/demo",
                    "artifacts": [
                        {"filename": "sample.txt", "url": source.as_uri(), "sha256": sha}
                    ],
                }
        ),
        encoding="utf-8",
    )

    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"dataset": "demo", "config_path": str(config_path)}), encoding="utf-8")

    exit_code = main(["--payload", str(payload), "--run"])
    assert exit_code == 0
    target = tmp_path / "outputs" / "demo" / "subset" / "sample.txt"
    assert target.exists()

def test_compliance_block(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    config_path.write_text(
        json.dumps(
            {
                "name": "demo",
                "output_dir": str(tmp_path / "outputs"),
                "source_url": "http://example.com",
                "distribution": "internal",
                "artifacts": [
                    {"filename": "sample.txt", "url": "http://example.com/sample.txt"}
                ],
            }
        ),
        encoding="utf-8",
    )

    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps({"dataset": "demo", "config_path": str(config_path)}), encoding="utf-8")

    with pytest.raises(PermissionError):
        main(["--payload", str(payload), "--run"])
