"""Placeholder audio tower implementations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import numpy as np

from ..interfaces import AudioTower, Batch, Configurable
from ..registries import register_audio_tower


@dataclass
class MeanPoolingAudioTower(AudioTower, Configurable):
    """Simple audio tower averaging precomputed feature vectors."""

    embedding_dim: int = 768

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "MeanPoolingAudioTower":
        return cls(embedding_dim=int(config.get("embedding_dim", cls.embedding_dim)))

    def embed_audio(self, batch: Batch) -> Any:
        features = batch.get("audio_features")
        if features is None:
            raise ValueError("Batch missing 'audio_features'")
        array = np.asarray(features)
        if array.ndim != 3:
            raise ValueError("audio_features must be 3D (batch, frames, dim)")
        pooled = array.mean(axis=1)
        if pooled.shape[1] != self.embedding_dim:
            pooled = np.resize(pooled, (pooled.shape[0], self.embedding_dim))
        return pooled

    def to(self, device: Any) -> None:  # pragma: no cover - CPU no-op
        return None

    def parameters(self) -> Iterable[Any]:  # pragma: no cover - no params
        return []


__all__ = ["MeanPoolingAudioTower"]


register_audio_tower("mean_pooling", MeanPoolingAudioTower)
