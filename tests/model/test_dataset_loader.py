from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from model.data import build_batches


def _write_manifest(root: Path, *, num_samples: int = 3) -> None:
    features_dir = root / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    manifest = root / "manifest.jsonl"
    with manifest.open("w", encoding="utf-8") as handle:
        for idx in range(num_samples):
            feature = np.random.rand(4 + idx, 8).astype(np.float32)
            feature_path = features_dir / f"sample{idx}.npy"
            np.save(feature_path, feature)
            record = {
                "id": f"sample-{idx}",
                "audio_features": f"features/sample{idx}.npy",
                "text": f"hello world {idx}",
                "split": "train" if idx < num_samples - 1 else "dev",
                "language": "en",
            }
            handle.write(json.dumps(record))
            handle.write("\n")


def test_build_batches_basic(tmp_path: Path) -> None:
    dataset_root = tmp_path / "dataset"
    _write_manifest(dataset_root)

    cfg = {
        "root": str(dataset_root),
        "manifest": "manifest.jsonl",
        "batch_size": 2,
        "shuffle": False,
        "split": "train",
    }

    iterator = build_batches(cfg, default_batch_size=2)
    batch = next(iterator)

    assert batch["audio_features"].shape[0] == 2
    assert batch["audio_features"].shape[2] == 8
    assert len(batch["text"]) == 2
    assert batch["audio_feature_lengths"].tolist() == [4, 5]


def test_build_batches_respects_max_batches(tmp_path: Path) -> None:
    dataset_root = tmp_path / "dataset"
    _write_manifest(dataset_root, num_samples=4)

    cfg = {
        "root": str(dataset_root),
        "manifest": "manifest.jsonl",
        "batch_size": 2,
        "shuffle": False,
        "max_batches": 1,
    }

    iterator = build_batches(cfg, default_batch_size=2)
    batches = list(iterator)
    assert len(batches) == 1
