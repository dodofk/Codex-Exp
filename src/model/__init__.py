"""Model package scaffolding for Phase 4 dual-encoder implementation."""

from __future__ import annotations

from .configs import TrainingConfig
from .trainer import Trainer
from .registries import (
    register_text_tower,
    register_audio_tower,
    get_text_tower,
    get_audio_tower,
)

__all__ = [
    "interfaces",
    "TrainingConfig",
    "Trainer",
    "register_text_tower",
    "register_audio_tower",
    "get_text_tower",
    "get_audio_tower",
]
