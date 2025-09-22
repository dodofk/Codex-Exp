"""Helpers for writing preprocessing lineage metadata."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


@dataclass
class LineageRecord:
    dataset: str
    step: str
    input_path: str
    output_path: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def append_lineage(record: LineageRecord, root: Path) -> None:
    """Append a lineage record to ``root/lineage.jsonl``."""

    root.mkdir(parents=True, exist_ok=True)
    lineage_path = root / "lineage.jsonl"
    with lineage_path.open("a", encoding="utf-8") as handle:
        handle.write(record.to_json())
        handle.write("\n")
