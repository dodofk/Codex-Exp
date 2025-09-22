from __future__ import annotations

from pathlib import Path

import pytest

from model.configs import TrainingConfig


def test_training_config_round_trip(tmp_path: Path) -> None:
    payload = {
        "text_tower": {"name": "qwen3"},
        "audio_tower": {"name": "distil_whisper"},
        "projection_head": {"dim": 768},
        "optimizer": {"name": "adamw", "lr": 5e-5},
        "training": {"epochs": 1, "batch_size": 2, "loss": {"temperature": 0.07}},
        "evaluation": {"metrics": ["recall_at_1"]},
        "dataset": {"root": "data/processed/fleurs/smoke", "manifest": "manifest.jsonl"},
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
text_tower:
  name: qwen3
audio_tower:
  name: distil_whisper
projection_head:
  dim: 768
optimizer:
  name: adamw
  lr: 5.0e-5
training:
  epochs: 1
  batch_size: 2
  loss:
    temperature: 0.07
dataset:
  root: data/processed/fleurs/smoke
  manifest: manifest.jsonl
evaluation:
  metrics: [recall_at_1]
"""
    )

    cfg = TrainingConfig.from_path(str(config_path))
    data = cfg.to_dict()

    assert data["text_tower"]["name"] == "qwen3"
    assert data["training"]["batch_size"] == 2
    assert data["training"]["loss"]["temperature"] == 0.07
    assert data["dataset"]["manifest"] == "manifest.jsonl"


def test_training_config_missing_keys(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text("{}")

    with pytest.raises(ValueError):
        TrainingConfig.from_path(str(config_path))
