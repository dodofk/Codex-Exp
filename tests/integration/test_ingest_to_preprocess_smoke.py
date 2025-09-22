from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest

pytest.importorskip("numpy")

from ingestion import cli as ingestion_cli
from preprocess import cli as preprocess_cli


def _generate_tone(path: Path, *, sample_rate: int = 8000, duration_sec: float = 0.5) -> None:
    import wave

    tone = bytearray()
    total_frames = int(sample_rate * duration_sec)
    amplitude = 0.4 * 32767
    for index in range(total_frames):
        value = int(amplitude * math.sin(2 * math.pi * 440 * index / sample_rate))
        tone.extend(value.to_bytes(2, "little", signed=True))

    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(tone)


def test_ingest_and_preprocess_smoke(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    raw_root = workspace / "raw"
    processed_root = workspace / "processed"
    fixture_audio = workspace / "fixtures" / "sample.wav"

    _generate_tone(fixture_audio)
    digest = hashlib.sha256(fixture_audio.read_bytes()).hexdigest()

    dataset_name = "smoke"
    dataset_version = "dev"

    ingestion_config = workspace / "ingestion.json"
    ingestion_config.write_text(
        json.dumps(
            {
                "name": dataset_name,
                "version": dataset_version,
                "source_url": "file://fixtures",
                "output_dir": str(raw_root),
                "artifacts": [
                    {
                        "filename": "sample.wav",
                        "url": fixture_audio.as_uri(),
                        "sha256": digest,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = ingestion_cli.main([str(ingestion_config)])
    assert exit_code == 0

    ingested_audio = raw_root / dataset_name / dataset_version / "sample.wav"
    assert ingested_audio.exists()

    preprocess_config = workspace / "preprocess.json"
    preprocess_config.write_text(
        json.dumps(
            {
                "dataset": dataset_name,
                "input_dir": str(ingested_audio.parent),
                "output_dir": str(processed_root / dataset_name / dataset_version),
                "sample_rate": 16000,
                "steps": [
                    {"name": "trim_silence", "params": {"threshold_db": -35}},
                    {"name": "resample", "params": {"rate": 16000}},
                    {"name": "normalize_volume", "params": {"target_dbfs": -18}},
                    {"name": "extract_features", "params": {"type": "log_mel", "n_mels": 40}},
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = preprocess_cli.main([str(preprocess_config)])
    assert exit_code == 0

    processed_audio = processed_root / dataset_name / dataset_version / "sample.wav"
    feature_file = processed_root / dataset_name / dataset_version / "features" / "sample.logmel.npy"
    assert processed_audio.exists()
    assert feature_file.exists()

    lineage_path = processed_root / dataset_name / dataset_version / "lineage.jsonl"
    assert lineage_path.exists()
    events = [json.loads(line) for line in lineage_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert any(entry["step"] == "audio_preprocess" for entry in events)
    assert any(entry["step"].startswith("features_") for entry in events)

    logs_dir = processed_root / dataset_name / dataset_version / "logs"
    assert (logs_dir / "events.jsonl").exists()
