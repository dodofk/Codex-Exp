from __future__ import annotations

from pathlib import Path

from model.cli import main


def test_cli_plan(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        """
text_tower:
  name: identity
  embedding_dim: 16
audio_tower:
  name: mean_pooling
  embedding_dim: 16
projection_head:
  dim: 16
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

    exit_code = main([str(config_path), "--mode", "train"])

    assert exit_code == 0
