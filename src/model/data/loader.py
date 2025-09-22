"""Manifest-backed dataset loader for training batches."""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional

import numpy as np


FIELD_ALIASES = {
    "audio": ["audio_features", "audio_path", "features"],
    "text": ["text", "transcript", "caption"],
    "tokens": ["text_tokens", "token_ids"],
    "tokens_path": ["text_tokens_path", "token_ids_path"],
    "id": ["id", "sample_id", "uid"],
    "language": ["language", "lang"],
}


@dataclass
class Sample:
    """Lightweight manifest sample reference."""

    audio_path: Path
    text: Optional[str]
    text_tokens: Optional[List[int]]
    text_tokens_path: Optional[Path]
    metadata: Dict[str, Any]


def _resolve_field(record: Mapping[str, Any], key: str) -> Any:
    for alias in FIELD_ALIASES.get(key, [key]):
        if alias in record:
            return record[alias]
    return None


def _load_manifest_samples(
    root: Path,
    manifest_paths: Iterable[Path],
    *,
    split: Optional[str] = None,
    max_samples: Optional[int] = None,
) -> List[Sample]:
    samples: List[Sample] = []
    for manifest_path in manifest_paths:
        with manifest_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                record = json.loads(line)
                if split and record.get("split") not in {split, None}:
                    continue
                audio_rel = _resolve_field(record, "audio")
                if audio_rel is None:
                    raise ValueError(f"Manifest entry missing audio path: {record}")
                audio_path = (root / audio_rel).expanduser().resolve()
                text = _resolve_field(record, "text")
                tokens = _resolve_field(record, "tokens")
                text_tokens = list(tokens) if isinstance(tokens, (list, tuple)) else None
                tokens_path = _resolve_field(record, "tokens_path")
                tokens_path_resolved = (
                    (root / tokens_path).expanduser().resolve()
                    if isinstance(tokens_path, str)
                    else None
                )
                metadata = {
                    "id": _resolve_field(record, "id"),
                    "language": _resolve_field(record, "language"),
                }
                samples.append(
                    Sample(
                        audio_path=audio_path,
                        text=text,
                        text_tokens=text_tokens,
                        text_tokens_path=tokens_path_resolved,
                        metadata={k: v for k, v in metadata.items() if v is not None},
                    )
                )
                if max_samples is not None and len(samples) >= max_samples:
                    return samples
    return samples


def _pad_tensor_list(items: List[np.ndarray], pad_value: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    if not items:
        raise ValueError("Cannot pad empty tensor list")
    max_len = max(arr.shape[0] for arr in items)
    feature_dim = items[0].shape[1]
    batch = np.full((len(items), max_len, feature_dim), pad_value, dtype=items[0].dtype)
    lengths = np.zeros(len(items), dtype=np.int32)
    for idx, arr in enumerate(items):
        length = arr.shape[0]
        batch[idx, :length, :] = arr
        lengths[idx] = length
    return batch, lengths


def _load_tokens_from_path(path: Path) -> List[int]:
    if path.suffix in {".npy", ".npz"}:
        tokens = np.load(path)
        return [int(x) for x in tokens.tolist()]
    data = path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(data)
        if isinstance(parsed, list):
            return [int(x) for x in parsed]
    except json.JSONDecodeError:
        pass
    return [int(part) for part in data.strip().split() if part]


def build_batches(config: Mapping[str, Any], *, default_batch_size: int) -> Iterator[Dict[str, Any]]:
    """Yield training batches from a manifest configuration."""

    root = Path(config.get("root") or config.get("root_dir", "")).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Dataset root does not exist: {root}")

    manifest = config.get("manifest")
    manifest_glob = config.get("manifest_glob")
    if manifest_glob:
        manifest_paths = sorted(root.glob(manifest_glob))
    elif manifest:
        manifest_paths = [root / manifest]
    else:
        manifest_paths = [root / "manifest.jsonl"]

    manifest_paths = [p for p in manifest_paths if p.exists()]
    if not manifest_paths:
        raise FileNotFoundError(f"No manifest files found under {root}")

    split = config.get("split")
    max_samples = config.get("max_samples")
    samples = _load_manifest_samples(root, manifest_paths, split=split, max_samples=max_samples)
    if not samples:
        raise ValueError(f"No samples found for dataset at {root}")

    batch_size = int(config.get("batch_size", default_batch_size))
    shuffle = bool(config.get("shuffle", False))
    seed = config.get("seed")
    drop_last = bool(config.get("drop_last", False))
    max_batches = config.get("max_batches")

    indices = list(range(len(samples)))
    rng = random.Random(seed)
    if shuffle:
        rng.shuffle(indices)

    num_batches = math.floor(len(indices) / batch_size) if drop_last else math.ceil(len(indices) / batch_size)
    batch_iter = 0
    for batch_idx in range(num_batches):
        start = batch_idx * batch_size
        end = start + batch_size
        batch_indices = indices[start:end]
        if len(batch_indices) < batch_size and drop_last:
            continue

        audio_tensors: List[np.ndarray] = []
        text_list: List[str] = []
        token_sequences: List[np.ndarray] = []
        languages: List[str] = []
        sample_ids: List[str] = []

        for idx in batch_indices:
            sample = samples[idx]
            audio = np.load(sample.audio_path)
            if audio.ndim != 2:
                raise ValueError(f"Expected audio features to be 2D, got shape {audio.shape} for {sample.audio_path}")
            audio_tensors.append(audio.astype(np.float32))

            if sample.text is not None:
                text_list.append(sample.text)
            else:
                text_list.append("")

            tokens = sample.text_tokens
            if tokens is None and sample.text_tokens_path is not None:
                tokens = _load_tokens_from_path(sample.text_tokens_path)
            if tokens is not None:
                arr = np.asarray(tokens, dtype=np.int32)
                token_sequences.append(arr)
            else:
                pass

            if "language" in sample.metadata:
                languages.append(sample.metadata["language"])
            if "id" in sample.metadata:
                sample_ids.append(sample.metadata["id"])

        audio_batch, audio_lengths = _pad_tensor_list(audio_tensors)

        batch: Dict[str, Any] = {
            "audio_features": audio_batch,
            "audio_feature_lengths": audio_lengths,
            "text": text_list,
        }

        if token_sequences:
            padded_tokens, token_len_array = _pad_tensor_list([arr.reshape(-1, 1) for arr in token_sequences], pad_value=0)
            batch["text_tokens"] = padded_tokens.squeeze(-1)
            batch["text_token_lengths"] = token_len_array

        if languages:
            batch["language"] = languages
        if sample_ids:
            batch["sample_id"] = sample_ids

        yield batch
        batch_iter += 1
        if max_batches is not None and batch_iter >= int(max_batches):
            break
