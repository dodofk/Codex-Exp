"""Distil-Whisper audio tower implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

try:  # pragma: no cover - optional dependency
    import torch
    from transformers import AutoModel
except ImportError:  # pragma: no cover
    torch = None  # type: ignore

import numpy as np

from ..interfaces import AudioTower, Batch, Configurable
from ..registries import register_audio_tower


@dataclass
class DistilWhisperAudioTower(AudioTower, Configurable):
    """Audio tower using Distil-Whisper encoder with feature inputs."""

    checkpoint: str = "openai/whisper-small"
    feature_dim: int = 80
    projection_dim: int = 768
    device: str = "cpu"

    def __post_init__(self) -> None:
        if torch is None:  # pragma: no cover
            raise ImportError("torch/transformers required for DistilWhisperAudioTower")
        self.model = AutoModel.from_pretrained(self.checkpoint)
        self.model.to(torch.device(self.device))
        self.embedding_dim = self.model.config.hidden_size

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "DistilWhisperAudioTower":
        return cls(
            checkpoint=config.get("checkpoint", cls.checkpoint),
            feature_dim=int(config.get("feature_dim", cls.feature_dim)),
            projection_dim=int(config.get("projection_dim", cls.projection_dim)),
            device=config.get("device", cls.device),
        )

    def embed_audio(self, batch: Batch) -> Any:
        if torch is None:  # pragma: no cover
            raise RuntimeError("torch not available")
        features = batch.get("audio_features")
        if features is None:
            raise ValueError("Batch missing 'audio_features'")
        array = np.asarray(features)
        if array.ndim != 3:
            raise ValueError("audio_features must be 3D (batch, frames, dim)")
        tensor = torch.tensor(array, dtype=torch.float32, device=self.model.device)
        with torch.no_grad():
            outputs = self.model(inputs_embeds=tensor)
            hidden = outputs.last_hidden_state
            embeddings = hidden.mean(dim=1)
        return embeddings

    def to(self, device: Any) -> None:
        if torch is None:  # pragma: no cover
            return
        self.model.to(torch.device(device))

    def parameters(self) -> Iterable[Any]:
        if torch is None:  # pragma: no cover
            return []
        return self.model.parameters()


register_audio_tower("distil_whisper", DistilWhisperAudioTower)


__all__ = ["DistilWhisperAudioTower"]
