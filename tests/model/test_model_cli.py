from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from model.cli import main


def _write_manifest(root: Path, *, num_samples: int = 2) -> None:
    features_dir = root / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    manifest = root / "manifest.jsonl"
    with manifest.open("w", encoding="utf-8") as handle:
        for idx in range(num_samples):
            feature = np.random.rand(4, 8).astype(np.float32)
            feature_path = features_dir / f"sample{idx}.npy"
            np.save(feature_path, feature)
            entry = {
                "id": f"sample-{idx}",
                "audio_features": f"features/sample{idx}.npy",
                "text": f"hello world {idx}",
            }
            handle.write(json.dumps(entry))
            handle.write("\n")


def _write_config(path: Path, dataset_root: Path, *, epochs: int = 1) -> None:
    path.write_text(
        f"""
text_tower:
  name: qwen3
  checkpoint: sshleifer/tiny-gpt2
  enable_lora: false
audio_tower:
  name: mean_pooling
  embedding_dim: 16
projection_head:
  dim: 16
optimizer:
  name: adamw
  lr: 5.0e-5
training:
  epochs: {epochs}
  batch_size: 2
dataset:
  root: {dataset_root}
  manifest: manifest.jsonl
  batch_size: 2
  shuffle: false
evaluation:
  metrics: [recall_at_1]
"""
    )


def test_cli_train_logs_metrics(tmp_path: Path) -> None:
    pytest.importorskip("torch")

    dataset_root = tmp_path / "dataset"
    _write_manifest(dataset_root)

    config_path = tmp_path / "config.yaml"
    _write_config(config_path, dataset_root, epochs=1)

    log_path = tmp_path / "train_log.jsonl"

    exit_code = main([str(config_path), "--mode", "train", "--log-jsonl", str(log_path)])

    assert exit_code == 0
    records = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    train_events = [r for r in records if r.get("event") == "train_epoch_end"]
    eval_events = [r for r in records if r.get("event") == "eval_complete"]
    assert train_events
    assert eval_events
    assert "bleu" in eval_events[0]["metrics"]


def test_cli_resume_skips_completed_epochs(tmp_path: Path) -> None:
    pytest.importorskip("torch")

    dataset_root = tmp_path / "dataset"
    _write_manifest(dataset_root, num_samples=3)

    config_path = tmp_path / "config.yaml"
    _write_config(config_path, dataset_root, epochs=2)

    log_path = tmp_path / "resume_log.jsonl"
    log_path.write_text(
        json.dumps({"event": "train_epoch_end", "epoch": 0, "metrics": {"loss": 1.23}}) + "\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            str(config_path),
            "--mode",
            "train",
            "--log-jsonl",
            str(log_path),
            "--resume-from",
            str(log_path),
        ]
    )

    assert exit_code == 0
    lines = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    epochs = [entry["epoch"] for entry in lines if entry.get("event") == "train_epoch_end"]
    assert epochs == [0, 1]
