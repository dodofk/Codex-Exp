"""Registries for text/audio tower implementations."""

from __future__ import annotations

from typing import Dict, Mapping, Type

from .interfaces import AudioTower, Configurable, TextTower


_TEXT_TOWERS: Dict[str, Type[TextTower]] = {}
_AUDIO_TOWERS: Dict[str, Type[AudioTower]] = {}


def register_text_tower(name: str, cls: Type[TextTower]) -> None:
    if name in _TEXT_TOWERS:
        raise ValueError(f"Text tower '{name}' already registered")
    _TEXT_TOWERS[name] = cls


def get_text_tower(name: str, config: Mapping[str, object]) -> TextTower:
    try:
        cls = _TEXT_TOWERS[name]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"Unknown text tower '{name}'") from exc
    if issubclass(cls, Configurable):
        return cls.from_config(config)  # type: ignore[return-value]
    return cls(**config)  # type: ignore[arg-type, return-value]


def register_audio_tower(name: str, cls: Type[AudioTower]) -> None:
    if name in _AUDIO_TOWERS:
        raise ValueError(f"Audio tower '{name}' already registered")
    _AUDIO_TOWERS[name] = cls


def get_audio_tower(name: str, config: Mapping[str, object]) -> AudioTower:
    try:
        cls = _AUDIO_TOWERS[name]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"Unknown audio tower '{name}'") from exc
    if issubclass(cls, Configurable):
        return cls.from_config(config)  # type: ignore[return-value]
    return cls(**config)  # type: ignore[arg-type, return-value]


__all__ = [
    "register_text_tower",
    "get_text_tower",
    "register_audio_tower",
    "get_audio_tower",
]
