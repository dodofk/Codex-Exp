"""Configuration loading utilities for model training."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Optional

try:  # pragma: no cover - optional dependency
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - fallback path
    BaseModel = None  # type: ignore[misc]

try:  # pragma: no cover - optional dependency
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

from .interfaces import ModelConfig


def _load_raw_config(path: Path) -> Mapping[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        if yaml is None:
            raise ValueError(
                "Configuration file is not valid JSON. Install PyYAML to parse YAML configs."
            )
        data = yaml.safe_load(text)
        if not isinstance(data, Mapping):
            raise ValueError("Model config must decode to a mapping")
        return data


if BaseModel is not None:  # pragma: no branch
    from pydantic import ValidationError

    class _ModelConfigModel(BaseModel):
        text_tower: Mapping[str, Any]
        audio_tower: Mapping[str, Any]
        projection_head: Mapping[str, Any]
        optimizer: Mapping[str, Any]
        training: Mapping[str, Any]
        evaluation: Mapping[str, Any]


    class TrainingConfig(ModelConfig):
        """Concrete implementation backed by Pydantic when available."""

        def __init__(self, payload: Mapping[str, Any]) -> None:
            try:
                self._model = _ModelConfigModel.model_validate(payload)
            except ValidationError as exc:  # pragma: no cover - error path
                raise ValueError(str(exc)) from exc

        @classmethod
        def from_path(cls, path: str) -> "TrainingConfig":
            return cls(_load_raw_config(Path(path)))

        def to_dict(self) -> Mapping[str, Any]:
            return self._model.model_dump()

        def __getattr__(self, item: str) -> Any:
            return getattr(self._model, item)

else:

    @dataclass
    class _ModelConfigData:
        text_tower: Mapping[str, Any]
        audio_tower: Mapping[str, Any]
        projection_head: Mapping[str, Any]
        optimizer: Mapping[str, Any]
        training: Mapping[str, Any]
        evaluation: Mapping[str, Any]

    class TrainingConfig(ModelConfig):
        """Fallback dataclass-backed config when Pydantic is unavailable."""

        def __init__(self, payload: Mapping[str, Any]) -> None:
            required_keys = {
                "text_tower",
                "audio_tower",
                "projection_head",
                "optimizer",
                "training",
                "evaluation",
            }
            missing = required_keys.difference(payload)
            if missing:
                raise ValueError(f"Missing required config keys: {sorted(missing)}")
            self._data = _ModelConfigData(
                text_tower=payload["text_tower"],
                audio_tower=payload["audio_tower"],
                projection_head=payload["projection_head"],
                optimizer=payload["optimizer"],
                training=payload["training"],
                evaluation=payload["evaluation"],
            )

        @classmethod
        def from_path(cls, path: str) -> "TrainingConfig":
            return cls(_load_raw_config(Path(path)))

        def to_dict(self) -> Mapping[str, Any]:
            return asdict(self._data)

        def __getattr__(self, item: str) -> Any:
            return getattr(self._data, item)


__all__ = ["TrainingConfig"]
