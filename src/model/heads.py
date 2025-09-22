"""Projection head utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import numpy as np

from .interfaces import Configurable, ProjectionHead, Tensor


@dataclass
class LinearProjectionHead(ProjectionHead, Configurable):
    """Projects embeddings using a simple scaling factor."""

    dim: int = 768
    temperature_init: float = 0.07

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "LinearProjectionHead":
        return cls(
            dim=int(config.get("dim", cls.dim)),
            temperature_init=float(config.get("temperature_init", cls.temperature_init)),
        )

    def project_text(self, embeddings: Tensor) -> Tensor:
        array = np.asarray(embeddings)
        return np.resize(array, (array.shape[0], self.dim))

    def project_audio(self, embeddings: Tensor) -> Tensor:
        array = np.asarray(embeddings)
        return np.resize(array, (array.shape[0], self.dim))

    @property
    def temperature(self) -> float:
        return self.temperature_init


__all__ = ["LinearProjectionHead"]
