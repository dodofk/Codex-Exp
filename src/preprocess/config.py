"""Configuration utilities for preprocessing pipelines."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List


@dataclass
class StepConfig:
    name: str
    params: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StepConfig":
        return cls(
            name=data["name"],
            params=data.get("params", {}),
        )


@dataclass
class PreprocessConfig:
    dataset: str
    input_dir: Path
    output_dir: Path
    sample_rate: int
    steps: Iterable[StepConfig]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PreprocessConfig":
        steps = [StepConfig.from_dict(item) for item in data.get("steps", [])]
        return cls(
            dataset=data["dataset"],
            input_dir=Path(data.get("input_dir", "data/raw")),
            output_dir=Path(data.get("output_dir", "data/processed")),
            sample_rate=int(data.get("sample_rate", 16000)),
            steps=steps,
        )


def load_config(path: str | Path) -> PreprocessConfig:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Preprocess config must contain a mapping")
    return PreprocessConfig.from_dict(payload)
