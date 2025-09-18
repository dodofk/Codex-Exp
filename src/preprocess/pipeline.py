"""Preprocessing pipeline scaffolding."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .config import PreprocessConfig


class PreprocessPipeline:
    """Simple pipeline that reports planned preprocessing steps."""

    def __init__(self, config: PreprocessConfig) -> None:
        self.config = config

    def plan(self) -> Iterable[str]:
        yield f"Dataset: {self.config.dataset}"
        yield f"Input dir: {self.config.input_dir}"
        yield f"Output dir: {self.config.output_dir}"
        yield f"Target sample rate: {self.config.sample_rate}"
        for step in self.config.steps:
            yield f"Step: {step.name} ({step.params})"

    def execute(self) -> None:  # pragma: no cover - placeholder
        raise NotImplementedError("Preprocessing execution not implemented yet")


def build_pipeline(config_path: str | Path) -> PreprocessPipeline:
    from .config import load_config

    cfg = load_config(config_path)
    return PreprocessPipeline(cfg)
