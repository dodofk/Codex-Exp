from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from preprocess.pipeline import PreprocessPipeline, build_pipeline


def _write_config(tmp_path: Path) -> Path:
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "dataset": "demo",
                "input_dir": "data/raw/demo",
                "output_dir": "data/processed/demo",
                "sample_rate": 16000,
                "steps": [
                    {"name": "resample", "params": {"rate": 16000}},
                    {"name": "features", "params": {"type": "log_mel"}},
                ],
            }
        ),
        encoding="utf-8",
    )
    return config


def test_build_pipeline(tmp_path: Path) -> None:
    cfg_path = _write_config(tmp_path)
    pipeline = build_pipeline(cfg_path)
    lines = list(pipeline.plan())

    assert "Dataset: demo" in lines[0]
    assert any("resample" in line for line in lines)


def test_execute_not_implemented(tmp_path: Path) -> None:
    audio_path = tmp_path / "data/raw/demo/sample.wav"
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    import wave
    with wave.open(str(audio_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(8000)
        wf.writeframes(b"\x00\x10" * 8000)

    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "dataset": "demo",
                "input_dir": str(tmp_path / "data/raw/demo"),
                "output_dir": str(tmp_path / "data/processed/demo"),
                "sample_rate": 16000,
                "steps": [],
            }
        ),
        encoding="utf-8",
    )

    pipeline = build_pipeline(config)
    pipeline.execute()

    processed_dir = tmp_path / "data/processed/demo"
    assert (processed_dir / "sample.wav").exists()
    log_file = processed_dir / "logs/events.jsonl"
    assert log_file.exists()
    assert "preprocess_complete" in log_file.read_text(encoding="utf-8")
    lineage_file = processed_dir / "lineage.jsonl"
    assert lineage_file.exists()
    lineage_entry = json.loads(lineage_file.read_text(encoding="utf-8").splitlines()[-1])
    assert lineage_entry["step"] == "audio_preprocess"
    assert lineage_entry["metadata"]["target_sample_rate"] == 16000
    feature_file = processed_dir / "features/sample.logmel.npy"
    assert not feature_file.exists()


def test_execute_with_features(tmp_path: Path) -> None:
    audio_path = tmp_path / "data/raw/demo/sample.wav"
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    import wave

    with wave.open(str(audio_path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(8000)
        wf.writeframes(b"\x00\x10" * 8000 * 2)

    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "dataset": "demo",
                "input_dir": str(tmp_path / "data/raw/demo"),
                "output_dir": str(tmp_path / "data/processed/demo"),
                "sample_rate": 16000,
                "steps": [
                    {"name": "resample", "params": {"rate": 16000}},
                    {"name": "extract_features", "params": {"type": "log_mel", "n_mels": 64}},
                ],
            }
        ),
        encoding="utf-8",
    )

    pipeline = build_pipeline(config)
    pipeline.execute()

    processed_dir = tmp_path / "data/processed/demo"
    feature_file = processed_dir / "features/sample.logmel.npy"
    assert feature_file.exists()
    mel = np.load(feature_file)
    assert mel.ndim == 2
    assert mel.shape[1] == 64


def test_execute_with_trim_silence(tmp_path: Path) -> None:
    audio_path = tmp_path / "data/raw/demo/sample.wav"
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    import wave

    silence = b"\x00\x00" * 2000
    tone = b"\xff\x0f" * 4000
    with wave.open(str(audio_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(silence + tone + silence)

    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "dataset": "demo",
                "input_dir": str(tmp_path / "data/raw/demo"),
                "output_dir": str(tmp_path / "data/processed/demo"),
                "sample_rate": 16000,
                "steps": [
                    {"name": "trim_silence", "params": {"threshold_db": -30}},
                    {"name": "resample", "params": {"rate": 16000}},
                ],
            }
        ),
        encoding="utf-8",
    )

    pipeline = build_pipeline(config)
    pipeline.execute()

    processed_file = tmp_path / "data/processed/demo/sample.wav"
    assert processed_file.exists()
    with wave.open(str(processed_file), "rb") as wf:
        frames = wf.readframes(wf.getnframes())
    # trimmed audio should be shorter than original (silence removed)
    assert len(frames) < len(silence + tone + silence)
