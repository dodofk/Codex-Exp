"""Command-line interface for training and evaluating retrieval models."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np

from .configs import TrainingConfig
from .heads import LinearProjectionHead
from .interfaces import RetrievalComponents
from .losses import InfoNCELoss
from .registries import get_audio_tower, get_text_tower
from .trainer import Trainer
from .metrics import evaluate_smoke_run

# Import tower modules for side-effect registration
from . import towers  # noqa: F401


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
    loss = InfoNCELoss()

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

    # compute evaluation metrics on the same smoke batch
    text_emb = components.text_tower.embed_text(batches[0])
    audio_emb = components.audio_tower.embed_audio(batches[0])
    text_proj = components.projection_head.project_text(text_emb)
    audio_proj = components.projection_head.project_audio(audio_emb)
    similarity = np.matmul(np.asarray(text_proj), np.asarray(audio_proj).T)
    eval_report = evaluate_smoke_run(similarity)

    print(f"Mode: {args.mode}")
    print(f"Training metrics: {metrics}")
    print(f"Evaluation metrics: {eval_report.values}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
