"""Loss utilities for retrieval training."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from .interfaces import LossComputer, Tensor


class InfoNCELoss(LossComputer):
    """Bidirectional InfoNCE loss computed with numpy for CPU smoke runs."""

    def __init__(self, temperature: float = 0.07) -> None:
        self.temperature = temperature

    def __call__(
        self,
        text_embeddings: Tensor,
        audio_embeddings: Tensor,
        batch: Mapping[str, Any],
    ) -> Mapping[str, Tensor]:
        text = np.asarray(text_embeddings)
        audio = np.asarray(audio_embeddings)

        similarity = text @ audio.T
        logits = similarity / self.temperature

        losses = []
        # text -> audio
        losses.append(self._cross_entropy(logits))
        # audio -> text
        losses.append(self._cross_entropy(logits.T))

        loss_value = float(np.mean(losses))
        diag = np.diag(similarity)

        return {
            "loss": loss_value,
            "similarity_mean": float(diag.mean()),
            "similarity_std": float(diag.std()),
        }

    @staticmethod
    def _cross_entropy(logits: np.ndarray) -> float:
        logits = logits - logits.max(axis=1, keepdims=True)
        exp = np.exp(logits)
        probs = exp / exp.sum(axis=1, keepdims=True)
        targets = np.arange(logits.shape[0])
        return float(-np.log(probs[np.arange(logits.shape[0]), targets] + 1e-9).mean())


__all__ = ["InfoNCELoss"]
