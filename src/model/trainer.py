"""Training loop scaffolding for the dual-encoder retrieval model."""

from __future__ import annotations

from typing import Dict, Iterable, Mapping, Optional

try:  # pragma: no cover - optional dependency
    import torch
except ImportError:  # pragma: no cover - allow import without torch
    torch = None  # type: ignore

import numpy as np

from .interfaces import (
    Batch,
    LossComputer,
    RetrievalComponents,
    TrainerHooks,
)


class Trainer:
    """Lightweight trainer orchestrating retrieval components."""

    def __init__(
        self,
        components: RetrievalComponents,
        loss: LossComputer,
        hooks: Optional[TrainerHooks] = None,
        device: Optional[str] = None,
    ) -> None:
        self.components = components
        self.loss = loss
        self.hooks = hooks
        self.device = device or "cpu"

        if torch is not None:
            torch_device = torch.device(self.device)
            self.components.text_tower.to(torch_device)
            self.components.audio_tower.to(torch_device)

    def train_epoch(self, batches: Iterable[Batch], optimizer: Optional[object] = None) -> Dict[str, float]:
        """Run a single epoch over the provided batches.

        Optimizer is typed loosely to keep this scaffold independent of the
        actual deep learning framework (PyTorch, TensorFlow, etc.).
        """

        metrics: Dict[str, float] = {}
        for step, batch in enumerate(batches):
            text_emb = self.components.text_tower.embed_text(batch)
            audio_emb = self.components.audio_tower.embed_audio(batch)

            text_proj = self.components.projection_head.project_text(text_emb)
            audio_proj = self.components.projection_head.project_audio(audio_emb)
            similarity = np.matmul(np.asarray(text_proj), np.asarray(audio_proj).T)

            loss_dict = self.loss(
                text_proj,
                audio_proj,
                similarity,
                batch,
            )

            if optimizer is not None and torch is not None:
                optimizer.zero_grad()
                loss_value = loss_dict.get("loss")
                if loss_value is not None:
                    loss_value.backward()  # pragma: no cover - requires torch
                    optimizer.step()

            metrics.update({k: float(v) for k, v in loss_dict.items() if k != "loss"})

            if self.hooks is not None:
                self.hooks.on_batch_end(step, loss_dict)

        if self.hooks is not None:
            self.hooks.on_epoch_end(0, metrics)

        return metrics


__all__ = ["Trainer"]
