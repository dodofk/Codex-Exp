"""Placeholder text tower implementations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import numpy as np

from ..interfaces import Batch, Configurable, TextTower
from ..registries import register_text_tower


@dataclass
class IdentityTextTower(TextTower, Configurable):
    """CPU-friendly text tower that returns bag-of-words embeddings."""

    vocab_size: int = 32768
    embedding_dim: int = 768

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "IdentityTextTower":
        return cls(
            vocab_size=int(config.get("vocab_size", cls.vocab_size)),
            embedding_dim=int(config.get("embedding_dim", cls.embedding_dim)),
        )

    def embed_text(self, batch: Batch) -> Any:
        tokens = batch.get("text_tokens")
        if tokens is None:
            raise ValueError("Batch missing 'text_tokens'")
        array = np.asarray(tokens)
        if array.ndim != 2:
            raise ValueError("text_tokens must be 2D")
        embeddings = array.mean(axis=1, keepdims=True)
        return np.repeat(embeddings, self.embedding_dim, axis=1)

    def to(self, device: Any) -> None:  # pragma: no cover - CPU no-op
        return None

    def parameters(self) -> Iterable[Any]:  # pragma: no cover - no params
        return []


__all__ = ["IdentityTextTower"]


register_text_tower("identity", IdentityTextTower)
