"""Preprocess worker utilities."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from .cli import build_pipeline


@dataclass
class JobPayload:
    """Schema describing a preprocessing job submitted to the queue."""

    dataset: str
    config_path: Optional[str] = None
    plan_only: bool = False
    metadata: Dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobPayload":
        return cls(
            dataset=data["dataset"],
            config_path=data.get("config_path"),
            plan_only=bool(data.get("plan_only", False)),
            metadata=data.get("metadata"),
        )


def load_payload(path: Path | None = None, json_str: str | None = None) -> JobPayload:
    if path is None and json_str is None:
        raise ValueError("Either payload path or json string is required")

    raw = path.read_text(encoding="utf-8") if path is not None else json_str or "{}"
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Payload must decode to a mapping")
    return JobPayload.from_dict(data)


def _resolve_config(payload: JobPayload) -> Path:
    if payload.config_path:
        return Path(payload.config_path)
    return Path(f"config/preprocess/{payload.dataset}.json")


def execute_job(payload: JobPayload, *, plan_only: bool | None = None) -> dict[str, Any]:
    config_path = _resolve_config(payload)
    pipeline = build_pipeline(config_path)
    if plan_only is None:
        plan_only = payload.plan_only
    if plan_only:
        lines = list(pipeline.plan())
        return {"plan": lines, "status": "planned"}
    pipeline.execute()
    return {"plan": list(pipeline.plan()), "status": "completed"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preprocess worker CLI")
    parser.add_argument("--payload", type=Path, help="Path to payload JSON file", required=False)
    parser.add_argument("--payload-json", type=str, help="Raw JSON payload string", required=False)
    parser.add_argument("--plan", action="store_true", help="Print preprocessing plan and exit")
    parser.add_argument("--run", action="store_true", help="Execute preprocessing after planning")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    payload = load_payload(args.payload, args.payload_json)
    plan_only = not args.run
    result = execute_job(payload, plan_only=plan_only)
    for line in result["plan"]:
        print(line)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
