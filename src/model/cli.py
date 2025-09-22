"""Command-line interface for training and evaluating retrieval models."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from .configs import TrainingConfig
from .heads import LinearProjectionHead
from .interfaces import RetrievalComponents
from .losses import InfoNCELoss
from .registries import get_audio_tower, get_text_tower
from .trainer import Trainer
from .metrics import evaluate_smoke_run
from .data import build_batches
from .logging_utils import log_event

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
    parser.add_argument(
        "--dataset-root",
        type=Path,
        help="Override dataset root directory",
    )
    parser.add_argument(
        "--dataset-manifest",
        help="Override dataset manifest (relative to root)",
    )
    parser.add_argument(
        "--dataset-manifest-glob",
        help="Override manifest glob pattern",
    )
    parser.add_argument(
        "--dataset-split",
        help="Limit dataset to a named split",
    )
    parser.add_argument(
        "--dataset-max-samples",
        type=int,
        help="Cap number of samples loaded from manifest",
    )
    parser.add_argument(
        "--dataset-max-batches",
        type=int,
        help="Cap training batches produced per epoch",
    )
    parser.add_argument(
        "--dataset-batch-size",
        type=int,
        help="Override dataset batch size",
    )
    parser.add_argument(
        "--dataset-seed",
        type=int,
        help="Override dataset shuffle seed",
    )
    parser.add_argument(
        "--dataset-shuffle",
        dest="dataset_shuffle",
        action="store_true",
        help="Enable dataset shuffling",
    )
    parser.add_argument(
        "--no-dataset-shuffle",
        dest="dataset_shuffle",
        action="store_false",
        help="Disable dataset shuffling",
    )
    parser.set_defaults(dataset_shuffle=None)
    parser.add_argument(
        "--run-id",
        help="Identifier for this training run (defaults to timestamp)",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        help="Directory to store run logs (default: data/logs/model)",
    )
    parser.add_argument(
        "--log-jsonl",
        type=Path,
        help="Override metrics JSONL path",
    )
    parser.add_argument(
        "--resume-from",
        type=Path,
        help="Resume training based on an existing JSONL log",
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


def _prepare_dataset_config(
    base_cfg: Mapping[str, Any] | None,
    args: argparse.Namespace,
    default_batch_size: int,
) -> dict[str, Any] | None:
    cfg: dict[str, Any] = dict(base_cfg) if isinstance(base_cfg, Mapping) else {}

    if args.dataset_root is not None:
        cfg["root"] = str(args.dataset_root)
    if args.dataset_manifest is not None:
        cfg["manifest"] = args.dataset_manifest
        cfg.pop("manifest_glob", None)
    if args.dataset_manifest_glob is not None:
        cfg["manifest_glob"] = args.dataset_manifest_glob
        cfg.pop("manifest", None)
    if args.dataset_split is not None:
        cfg["split"] = args.dataset_split
    if args.dataset_max_samples is not None:
        cfg["max_samples"] = int(args.dataset_max_samples)
    if args.dataset_max_batches is not None:
        cfg["max_batches"] = int(args.dataset_max_batches)
    if args.dataset_batch_size is not None:
        cfg["batch_size"] = int(args.dataset_batch_size)
    if args.dataset_seed is not None:
        cfg["seed"] = int(args.dataset_seed)
    if args.dataset_shuffle is not None:
        cfg["shuffle"] = bool(args.dataset_shuffle)

    if not cfg:
        return None

    cfg.setdefault("batch_size", default_batch_size)
    return cfg


def _prepare_log_file(path: Path, reuse: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if reuse:
        path.touch(exist_ok=True)
    else:
        path.write_text("", encoding="utf-8")


def _load_last_completed_epoch(path: Path) -> int:
    if not path.exists():
        return -1
    last_epoch = -1
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("event") == "train_epoch_end":
                try:
                    last_epoch = max(last_epoch, int(record.get("epoch", -1)))
                except (TypeError, ValueError):
                    continue
    return last_epoch


def _make_smoke_batch(batch_size: int) -> dict[str, Any]:
    return {
        "text": [f"smoke sample {i}" for i in range(batch_size)],
        "audio_features": np.random.rand(batch_size, 4, 8).astype(np.float32),
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = TrainingConfig.from_path(str(args.config))
    config_dict = config.to_dict()
    config_dict = _apply_overrides(config_dict, args.override)

    training_cfg = config_dict.get("training", {})
    epochs = int(training_cfg.get("epochs", 1))
    default_batch_size = int(training_cfg.get("batch_size", 1))

    dataset_cfg = _prepare_dataset_config(config_dict.get("dataset"), args, default_batch_size)

    text_cfg = config_dict["text_tower"]
    audio_cfg = config_dict["audio_tower"]
    head_cfg = config_dict.get("projection_head", {})
    training_cfg.setdefault("loss", {})
    loss_cfg = training_cfg.get("loss", {})

    text_tower = get_text_tower(text_cfg.get("name", "identity"), text_cfg)
    audio_tower = get_audio_tower(audio_cfg.get("name", "mean_pooling"), audio_cfg)
    head = LinearProjectionHead.from_config(head_cfg)
    loss = InfoNCELoss(
        temperature=float(loss_cfg.get("temperature", 0.07)),
        spreadout_weight=float(loss_cfg.get("spreadout_weight", 0.0)),
        spreadout_margin=float(loss_cfg.get("spreadout_margin", 0.0)),
    )

    components = RetrievalComponents(
        text_tower=text_tower,
        audio_tower=audio_tower,
        projection_head=head,
        loss_computer=loss,
    )

    trainer = Trainer(components=components, loss=loss)

    run_id = args.run_id or datetime.now(timezone.utc).strftime("model-%Y%m%dT%H%M%S")
    base_log_dir = Path(args.log_dir) if args.log_dir else Path("data/logs/model")
    default_log_path = base_log_dir / run_id / "metrics.jsonl"
    log_path = Path(args.log_jsonl) if args.log_jsonl else default_log_path
    resume_path = Path(args.resume_from) if args.resume_from else None
    if resume_path is not None and not resume_path.exists():
        raise FileNotFoundError(f"Resume log not found: {resume_path}")
    reuse = resume_path is not None and log_path.resolve() == resume_path.resolve()
    _prepare_log_file(log_path, reuse=reuse)

    start_epoch = 0
    if resume_path is not None:
        start_epoch = _load_last_completed_epoch(resume_path) + 1
        if start_epoch >= epochs:
            print(f"Resume point beyond configured epochs ({epochs}); skipping training.")

    evaluation_cfg = config_dict.get("evaluation", {})

    run_payload: dict[str, Any] = {
        "config": str(args.config),
        "mode": args.mode,
        "epochs": epochs,
    }
    if dataset_cfg and "root" in dataset_cfg:
        run_payload["dataset_root"] = dataset_cfg["root"]
    if dataset_cfg and "manifest" in dataset_cfg:
        run_payload["manifest"] = dataset_cfg["manifest"]
    elif dataset_cfg and "manifest_glob" in dataset_cfg:
        run_payload["manifest_glob"] = dataset_cfg["manifest_glob"]

    def epoch_dataset_iterator(epoch: int):
        if dataset_cfg is None:
            return iter([_make_smoke_batch(default_batch_size)])
        epoch_cfg = dict(dataset_cfg)
        seed = epoch_cfg.get("seed")
        if seed is not None:
            epoch_cfg["seed"] = int(seed) + epoch
        return build_batches(epoch_cfg, default_batch_size=epoch_cfg.get("batch_size", default_batch_size))

    def evaluation_iterator():
        if dataset_cfg is None:
            return iter([_make_smoke_batch(default_batch_size)])
        eval_cfg = dict(dataset_cfg)
        eval_max_batches = evaluation_cfg.get("max_batches") or evaluation_cfg.get("max_eval_batches")
        if eval_max_batches is not None:
            eval_cfg["max_batches"] = int(eval_max_batches)
        return build_batches(eval_cfg, default_batch_size=eval_cfg.get("batch_size", default_batch_size))

    mode = args.mode
    train_metrics: dict[str, float] | None = None

    if start_epoch > 0:
        log_event(run_id, "run_resume", {**run_payload, "start_epoch": start_epoch}, log_path)
    else:
        log_event(run_id, "run_start", run_payload, log_path)

    if mode == "train" and start_epoch < epochs:
        for epoch in range(start_epoch, epochs):
            metrics = trainer.train_epoch(epoch_dataset_iterator(epoch))
            train_metrics = metrics
            log_event(run_id, "train_epoch_end", {"epoch": epoch, "metrics": metrics}, log_path)
    elif mode == "train":
        train_metrics = {}

    eval_batches = evaluation_iterator()
    try:
        first_batch = next(eval_batches)
    except StopIteration:  # pragma: no cover - defensive
        raise ValueError("Dataset iterator produced no batches for evaluation")
    text_emb = components.text_tower.embed_text(first_batch)
    audio_emb = components.audio_tower.embed_audio(first_batch)
    text_proj = components.projection_head.project_text(text_emb)
    audio_proj = components.projection_head.project_audio(audio_emb)
    similarity = np.matmul(np.asarray(text_proj), np.asarray(audio_proj).T)
    text_refs = list(first_batch.get("text", [])) if isinstance(first_batch.get("text"), list) else None
    predictions = None
    references = None
    if text_refs:
        batch_size = similarity.shape[0]
        truncate = min(batch_size, len(text_refs))
        if truncate:
            indices = np.argmax(similarity[:truncate, :truncate], axis=1)
            predictions = [text_refs[idx] for idx in indices]
            references = text_refs[:truncate]
    eval_report = evaluate_smoke_run(similarity, predictions=predictions, references=references)
    eval_metrics = dict(eval_report)

    print(f"Mode: {args.mode}")
    if train_metrics is not None:
        print(f"Training metrics: {train_metrics}")
    else:
        print("Training metrics: <skipped>")
    print(f"Evaluation metrics: {eval_metrics}")
    log_event(run_id, "eval_complete", {"metrics": eval_metrics}, log_path)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
