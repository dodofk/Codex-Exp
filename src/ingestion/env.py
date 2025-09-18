"""Environment helper utilities for ingestion."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict

_ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


def load_env_file(path: Path = Path(".env.ingestion")) -> None:
    """Load key=value pairs from `.env.ingestion` if present."""

    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        os.environ.setdefault(key, value)


def expand_env(value: str) -> str:
    """Expand ${VAR} placeholders using environment variables."""

    def _replace(match: re.Match[str]) -> str:
        var = match.group(1)
        if var not in os.environ:
            raise KeyError(f"Missing environment variable '{var}' for ingestion header expansion")
        return os.environ[var]

    return _ENV_PATTERN.sub(_replace, value)


def expand_headers(headers: Dict[str, str] | None) -> Dict[str, str] | None:
    if not headers:
        return headers
    expanded: Dict[str, str] = {}
    for key, value in headers.items():
        expanded[key] = expand_env(value) if isinstance(value, str) else value
    return expanded
