"""Interfaces for the Phase 4 dual-encoder retrieval stack.

These protocols document the contracts that upcoming model components must
respect. They deliberately avoid importing heavy dependencies (e.g. torch)
so the file can be imported in environments where those packages are not yet
installed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Optional, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Common type aliases
# ---------------------------------------------------------------------------

Batch = Mapping[str, Any]
Tensor = Any  # Placeholder: implementations will typically return torch.Tensor


@runtime_checkable
class Configurable(Protocol):
    """Marker protocol for components that can be constructed from config data."""

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "Configurable":  # pragma: no cover - interface
        ...


@runtime_checkable
class ModelConfig(Protocol):
    """Configuration contract backing the YAML/Pydantic schema."""

    @classmethod
    def from_path(cls, path: str) -> "ModelConfig":  # pragma: no cover - interface
        ...

    def to_dict(self) -> Mapping[str, Any]:
        ...


@runtime_checkable
class TextTower(Protocol):
    """Text encoder contract."""

    def embed_text(self, batch: Batch) -> Tensor:
        """Return text embeddings for a batch (shape: [batch, dim])."""

    def to(self, device: Any) -> None:
        """Move underlying weights to device (CPU by default)."""

    def parameters(self) -> Iterable[Any]:  # pragma: no cover - interface
        """Expose parameters for optimizer construction."""


@runtime_checkable
class AudioTower(Protocol):
    """Audio encoder operating on precomputed feature tensors."""

    def embed_audio(self, batch: Batch) -> Tensor:
        """Return audio embeddings for a batch (shape: [batch, dim])."""

    def to(self, device: Any) -> None:
        ...

    def parameters(self) -> Iterable[Any]:  # pragma: no cover - interface
        ...


@runtime_checkable
class ProjectionHead(Protocol):
    """Projects tower embeddings into the shared retrieval space."""

    def project_text(self, embeddings: Tensor) -> Tensor:
        ...

    def project_audio(self, embeddings: Tensor) -> Tensor:
        ...

    @property
    def temperature(self) -> Optional[float]:
        """Return learnable temperature value if available."""


@runtime_checkable
class RetrievalModel(Protocol):
    """Combines towers and projection head to produce similarity logits."""

    text_tower: TextTower
    audio_tower: AudioTower
    projection_head: ProjectionHead

    def forward(self, batch: Batch) -> Mapping[str, Tensor]:
        """Return logits/embeddings used for loss computation."""


@runtime_checkable
class LossComputer(Protocol):
    """Computes contrastive losses for retrieval."""

    def __call__(
        self,
        text_embeddings: Tensor,
        audio_embeddings: Tensor,
        logits: Tensor,
        batch: Batch,
    ) -> Mapping[str, Tensor]:
        """Return mapping containing scalar loss and diagnostics."""


@runtime_checkable
class TrainerHooks(Protocol):
    """Lifecycle callbacks for the training loop."""

    def on_batch_end(self, step: int, metrics: Mapping[str, Any]) -> None:
        ...

    def on_epoch_end(self, epoch: int, metrics: Mapping[str, Any]) -> None:
        ...


@dataclass
class RetrievalComponents:
    """Container bundling all major retrieval components."""

    text_tower: TextTower
    audio_tower: AudioTower
    projection_head: ProjectionHead
    loss_computer: LossComputer


__all__ = [
    "Batch",
    "Tensor",
    "Configurable",
    "ModelConfig",
    "TextTower",
    "AudioTower",
    "ProjectionHead",
    "RetrievalModel",
    "LossComputer",
    "TrainerHooks",
    "RetrievalComponents",
]
