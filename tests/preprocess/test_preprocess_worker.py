from __future__ import annotations

import json
from pathlib import Path

import pytest

from preprocess.worker import JobPayload, execute_job


def _write_audio(tmp_path: Path, name: str = "sample.wav", *, frames: bytes | None = None) -> Path:
    import wave
    import math

    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if frames is None:
        sample_rate = 8000
        duration = 0.25
        samples = int(sample_rate * duration)
        data = bytearray()
        for i in range(samples):
            val = int(0.4 * 32767 * math.sin(2 * math.pi * 440 * i / sample_rate))
            data.extend(int.to_bytes(val, 2, "little", signed=True))
        frames = bytes(data)
    else:
        sample_rate = 8000

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(frames)
    return path


def _write_config(tmp_path: Path, input_dir: Path, output_dir: Path) -> Path:
    config = {
        "dataset": "demo",
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "sample_rate": 16000,
        "steps": [
            {"name": "trim_silence", "params": {"threshold_db": -30}},
            {"name": "resample", "params": {"rate": 16000}},
            {"name": "normalize_volume", "params": {"target_dbfs": -20}},
            {"name": "extract_features", "params": {"type": "log_mel", "n_mels": 32}},
        ],
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def test_execute_job_plan_only(tmp_path: Path) -> None:
    input_dir = tmp_path / "data/raw/demo/v1"
    _write_audio(input_dir)
    config_path = _write_config(tmp_path, input_dir, tmp_path / "data/processed/demo/v1")

    payload = JobPayload(dataset="demo", config_path=str(config_path))
    result = execute_job(payload, plan_only=True)

    assert result["status"] == "planned"
    assert any("extract_features" in line for line in result["plan"])


def test_execute_job_runs_pipeline(tmp_path: Path) -> None:
    input_dir = tmp_path / "data/raw/demo/v1"
    _write_audio(input_dir)
    output_dir = tmp_path / "data/processed/demo/v1"
    config_path = _write_config(tmp_path, input_dir, output_dir)

    payload = JobPayload(dataset="demo", config_path=str(config_path))
    result = execute_job(payload, plan_only=False)

    assert result["status"] == "completed"
    processed = output_dir / "sample.wav"
    assert processed.exists()
    feature = output_dir / "features/sample.logmel.npy"
    assert feature.exists()
