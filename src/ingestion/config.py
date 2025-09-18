"""Configuration helpers for ingestion pipelines."""
from __future__ import annotations

from dataclasses import dataclass, replace
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    yaml = None


@dataclass
class ArtifactSpec:
    """Description of a single dataset artifact to download."""

    filename: str
    url: str
    sha256: Optional[str] = None
    headers: Dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArtifactSpec":
        return cls(
            filename=data["filename"],
            url=data["url"],
            sha256=data.get("sha256"),
            headers=data.get("headers"),
        )


@dataclass
class DatasetConfig:
    """Minimal ingestion configuration for a dataset."""

    name: str
    version: str
    source_url: str
    checksum_manifest: Optional[str] = None
    output_dir: Path = Path("data/raw")
    artifacts: Iterable[ArtifactSpec] = ()
    extra: Dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatasetConfig":
        artifacts_data = data.get("artifacts", [])
        artifacts = tuple(ArtifactSpec.from_dict(item) for item in artifacts_data)
        return cls(
            name=data["name"],
            version=data.get("version", "unknown"),
            source_url=data["source_url"],
            checksum_manifest=data.get("checksum_manifest"),
            output_dir=Path(data.get("output_dir", "data/raw")),
            artifacts=artifacts,
            extra=data.get("extra"),
        )

    def with_artifacts(self, names: Iterable[str]) -> "DatasetConfig":
        selected = {name for name in names}
        filtered = tuple(artifact for artifact in self.artifacts if artifact.filename in selected)
        if not filtered:
            raise ValueError(f"No artifacts matched the selection: {', '.join(selected)}")
        return replace(self, artifacts=filtered)


def _parse_simple_mapping(text: str) -> Dict[str, Any]:
    """Fallback parser for trivial key/value configuration files."""

    result: Dict[str, Any] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise ValueError("Unsupported configuration format without PyYAML")
        key, value = stripped.split(":", 1)
        result[key.strip()] = value.strip().strip('"')
    return result


def load_config(path: str | Path) -> DatasetConfig:
    """Load a dataset configuration from JSON/YAML text."""

    raw_text = Path(path).read_text(encoding="utf-8")

    # Prefer JSON parsing (works with YAML subset when formatted as JSON).
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError:
        payload = None

    if payload is None and yaml is not None:  # pragma: no branch
        payload = yaml.safe_load(raw_text)

    if payload is None:
        payload = _parse_simple_mapping(raw_text)

    if not isinstance(payload, dict):
        raise ValueError("Configuration file must contain a mapping")

    return DatasetConfig.from_dict(payload)
