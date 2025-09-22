"""Loss utilities for retrieval training."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from .interfaces import LossComputer, Tensor


class DummyContrastiveLoss(LossComputer):
    """Placeholder InfoNCE-style loss operating on numpy arrays."""

    def __call__(
        self,
        text_embeddings: Tensor,
        audio_embeddings: Tensor,
        logits: Tensor,
        batch: Mapping[str, Any],
    ) -> Mapping[str, Tensor]:
        text = np.asarray(text_embeddings)
        audio = np.asarray(audio_embeddings)
        similarities = (text * audio).sum(axis=1)
        loss = 1.0 - similarities.mean()
        return {"loss": loss, "similarity_mean": similarities.mean()}


__all__ = ["DummyContrastiveLoss"]
