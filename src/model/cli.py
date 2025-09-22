"""Command-line interface for training and evaluating retrieval models."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np

from .configs import TrainingConfig
from .heads import LinearProjectionHead
from .interfaces import RetrievalComponents
from .losses import DummyContrastiveLoss
from .registries import get_audio_tower, get_text_tower
from .trainer import Trainer

# Import tower modules for side-effect registration
from .towers import audio as _audio_towers  # noqa: F401
from .towers import text as _text_towers  # noqa: F401


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train or evaluate the retrieval model")
    parser.add_argument("config", type=Path, help="Path to model config YAML/JSON")
    parser.add_argument(
        "--mode",
        choices=["train", "eval"],
        default="train",
        help="Execution mode (train or evaluate)",
    )
    parser.add_argument(
        "--override",
        action="append",
        help="Override config values (key=value)",
    )
    return parser


def _apply_overrides(config_dict: dict[str, Any], overrides: list[str] | None) -> dict[str, Any]:
    if not overrides:
        return config_dict
    updated = config_dict.copy()
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"Override must be key=value, got: {item}")
        key, value = item.split("=", 1)
        updated[key] = value
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = TrainingConfig.from_path(str(args.config))
    config_dict = config.to_dict()
    config_dict = _apply_overrides(config_dict, args.override)

    text_cfg = config_dict["text_tower"]
    audio_cfg = config_dict["audio_tower"]
    head_cfg = config_dict.get("projection_head", {})

    text_tower = get_text_tower(text_cfg.get("name", "identity"), text_cfg)
    audio_tower = get_audio_tower(audio_cfg.get("name", "mean_pooling"), audio_cfg)
    head = LinearProjectionHead.from_config(head_cfg)
    loss = DummyContrastiveLoss()

    components = RetrievalComponents(
        text_tower=text_tower,
        audio_tower=audio_tower,
        projection_head=head,
        loss_computer=loss,
    )

    trainer = Trainer(components=components, loss=loss)

    # Smoke data (two samples)
    batches = [
        {
            "text_tokens": np.random.randint(0, 10, size=(4, 16)),
            "audio_features": np.random.rand(4, 8, 16),
        }
    ]

    metrics = trainer.train_epoch(batches)
    print(f"Mode: {args.mode}")
    print(f"Metrics: {metrics}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
