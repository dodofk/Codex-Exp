"""Loss utilities for retrieval training."""

from __future__ import annotations

from typing import Any, Mapping

import numpy as np

try:  # pragma: no cover - optional dependency
    import torch
    import torch.nn.functional as F
except ImportError:  # pragma: no cover - torch optional
    torch = None  # type: ignore
    F = None  # type: ignore

from .interfaces import LossComputer


class InfoNCELoss(LossComputer):
    """Bidirectional InfoNCE loss with optional torch autograd support."""

    def __init__(
        self,
        temperature: float = 0.07,
        spreadout_weight: float = 0.0,
        spreadout_margin: float = 0.0,
    ) -> None:
        self.temperature = temperature
        self.spreadout_weight = spreadout_weight
        self.spreadout_margin = spreadout_margin

    def __call__(
        self,
        text_embeddings: Any,
        audio_embeddings: Any,
        batch: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        if torch is not None and isinstance(text_embeddings, torch.Tensor) and isinstance(audio_embeddings, torch.Tensor):
            return self._torch_forward(text_embeddings, audio_embeddings)
        text = np.asarray(text_embeddings)
        audio = np.asarray(audio_embeddings)
        return self._numpy_forward(text, audio)

    def _torch_forward(self, text: "torch.Tensor", audio: "torch.Tensor") -> Mapping[str, Any]:
        logits = text @ audio.T / self.temperature
        target = torch.arange(logits.shape[0], device=logits.device)
        loss_text = F.cross_entropy(logits, target)
        loss_audio = F.cross_entropy(logits.T, target)
        loss = 0.5 * (loss_text + loss_audio)
        if self.spreadout_weight > 0.0:
            loss = loss + self.spreadout_weight * self._torch_spreadout(text, audio)
        diag = torch.diagonal(text @ audio.T)
        return {
            "loss": loss,
            "similarity_mean": diag.mean().detach().cpu().item(),
            "similarity_std": diag.std().detach().cpu().item(),
        }

    def _numpy_forward(self, text: np.ndarray, audio: np.ndarray) -> Mapping[str, Any]:
        similarity = text @ audio.T
        logits = similarity / self.temperature

        losses = []
        losses.append(self._cross_entropy_numpy(logits))
        losses.append(self._cross_entropy_numpy(logits.T))

        loss_value = float(np.mean(losses))
        if self.spreadout_weight > 0.0:
            loss_value += self.spreadout_weight * float(self._numpy_spreadout(text, audio))
        diag = np.diag(similarity)
        return {
            "loss": loss_value,
            "similarity_mean": float(diag.mean()),
            "similarity_std": float(diag.std()),
        }

    @staticmethod
    def _cross_entropy_numpy(logits: np.ndarray) -> float:
        logits = logits - logits.max(axis=1, keepdims=True)
        exp = np.exp(logits)
        probs = exp / exp.sum(axis=1, keepdims=True)
        targets = np.arange(logits.shape[0])
        return float(-np.log(probs[np.arange(logits.shape[0]), targets] + 1e-9).mean())

    def _torch_spreadout(self, text: "torch.Tensor", audio: "torch.Tensor") -> "torch.Tensor":
        embeddings = torch.cat([text, audio], dim=0)
        embeddings = F.normalize(embeddings, p=2, dim=1)
        sim = embeddings @ embeddings.T
        margin = self.spreadout_margin
        mask = torch.eye(sim.size(0), device=sim.device, dtype=torch.bool)
        sim = sim.masked_fill(mask, 0.0)
        if margin > 0:
            penalty = torch.clamp(sim - margin, min=0.0) ** 2
        else:
            penalty = sim ** 2
        return penalty.mean()

    def _numpy_spreadout(self, text: np.ndarray, audio: np.ndarray) -> float:
        embeddings = np.concatenate([text, audio], axis=0)
        embeddings = embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-9)
        sim = embeddings @ embeddings.T
        np.fill_diagonal(sim, 0.0)
        if self.spreadout_margin > 0:
            penalty = np.maximum(sim - self.spreadout_margin, 0.0) ** 2
        else:
            penalty = sim ** 2
        return float(penalty.mean())


__all__ = ["InfoNCELoss"]
