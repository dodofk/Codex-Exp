"""Ingestion worker utilities.

This module defines the job payload schema for queue-driven ingestion and exposes
an entry point that can be reused by rq/Celery workers. Execution is intentionally
thin for now—the next step will connect it to the actual queue runtime.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from .config import DatasetConfig, load_config
from .env import load_env_file
from .tasks import execute, plan_download, render_plan


@dataclass
class JobPayload:
    """Schema describing an ingestion job submitted to the queue."""

    dataset: str
    config_path: Optional[str] = None
    artifacts: Optional[Iterable[str]] = None
    env_file: Optional[str] = None
    metadata: Dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobPayload":
        return cls(
            dataset=data["dataset"],
            config_path=data.get("config_path"),
            artifacts=data.get("artifacts"),
            env_file=data.get("env_file"),
            metadata=data.get("metadata"),
        )


def load_payload(path: Path | None = None, json_str: str | None = None) -> JobPayload:
    if path is None and json_str is None:
        raise ValueError("Either payload path or json string is required")

    if path is not None:
        raw = path.read_text(encoding="utf-8")
    else:
        raw = json_str or "{}"

    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Payload must decode to a mapping")
    return JobPayload.from_dict(data)


def _load_dataset_config(payload: JobPayload) -> DatasetConfig:
    config_path = Path(payload.config_path or f"config/ingestion/{payload.dataset}.json")
    config = load_config(config_path)
    if payload.artifacts:
        config = config.with_artifacts(payload.artifacts)
    return config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingestion worker CLI")
    parser.add_argument("--payload", type=Path, help="Path to payload JSON file", required=False)
    parser.add_argument("--payload-json", type=str, help="Raw JSON payload string", required=False)
    parser.add_argument("--plan", action="store_true", help="Print ingestion plan and exit")
    parser.add_argument("--run", action="store_true", help="Execute ingestion after planning")
    parser.add_argument("--artifact", action="append", dest="artifacts", help="Restrict execution to selected artifacts")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    payload = load_payload(args.payload, args.payload_json)
    if args.artifacts:
        payload.artifacts = list(args.artifacts)
    result = execute_job(payload, plan_only=not args.run)
    print(render_plan(result["plan"]))
    return 0


def execute_job(payload: JobPayload, *, plan_only: bool = False) -> dict[str, Any]:
    env_file = Path(payload.env_file or ".env.ingestion")
    load_env_file(env_file)

    dataset_config = _load_dataset_config(payload)
    _validate_compliance(dataset_config)
    plan = plan_download(dataset_config)

    if plan_only:
        return {"plan": plan, "status": "planned"}

    execute(dataset_config)
    return {"plan": plan, "status": "completed"}


COMPLIANCE_DEFS = {
    "internal": "Dataset marked internal-only; cannot run ingestion without override.",
    "restricted": "Dataset requires explicit approval; update manifest before proceeding.",
}


def _validate_compliance(config: DatasetConfig) -> None:
    distribution = (config.distribution or "public").lower()
    if distribution in COMPLIANCE_DEFS:
        raise PermissionError(COMPLIANCE_DEFS[distribution])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
