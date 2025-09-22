from __future__ import annotations

from pathlib import Path

import pytest

from model.configs import TrainingConfig


def test_training_config_round_trip(tmp_path: Path) -> None:
    payload = {
        "text_tower": {"name": "phi2_lora"},
        "audio_tower": {"name": "distil_whisper"},
        "projection_head": {"dim": 768},
        "optimizer": {"name": "adamw", "lr": 5e-5},
        "training": {"epochs": 1, "batch_size": 2},
        "evaluation": {"metrics": ["recall_at_1"]},
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
text_tower:
  name: phi2_lora
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
evaluation:
  metrics: [recall_at_1]
"""
    )

    cfg = TrainingConfig.from_path(str(config_path))
    data = cfg.to_dict()

    assert data["text_tower"]["name"] == "phi2_lora"
    assert data["training"]["batch_size"] == 2


def test_training_config_missing_keys(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text("{}")

    with pytest.raises(ValueError):
        TrainingConfig.from_path(str(config_path))
