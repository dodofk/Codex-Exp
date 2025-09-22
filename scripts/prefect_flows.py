"""Prefect flow stubs for Auto-Paper Phase 3."""
from __future__ import annotations

import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
for path in (BASE_DIR, SRC_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from prefect import flow, task

from scripts.enqueue_ingestion import run as enqueue_run
from preprocess.worker import main as preprocess_worker_main


def _build_ingestion_args(dataset: str, config: str | None, priority: str | None) -> object:
    args = type("Args", (), {})()
    args.dataset = dataset
    args.config = config
    args.artifact = None
    args.priority = priority
    args.metadata = None
    args.plan = False
    return args


def _build_preprocess_payload(dataset: str, config: str | None) -> str:
    payload = {"dataset": dataset}
    if config:
        payload["config_path"] = config
    payload["plan_only"] = False
    return json.dumps(payload)


@task
def launch_ingestion(dataset: str, config: str | None = None, priority: str | None = None) -> None:
    enqueue_run(_build_ingestion_args(dataset, config, priority))


@task
def launch_preprocess(dataset: str, config: str | None = None) -> None:
    payload_json = _build_preprocess_payload(dataset, config)
    preprocess_worker_main(["--payload-json", payload_json, "--run"])


@flow(name="auto-paper-ingestion")
def ingestion_flow(dataset: str, config_path: str | None = None, priority: str | None = "standard") -> None:
    launch_ingestion(dataset, config_path, priority)


@flow(name="auto-paper-preprocess")
def preprocess_flow(dataset: str, config_path: str | None = None) -> None:
    launch_preprocess(dataset, config_path)


@flow(name="auto-paper-ingest-preprocess")
def ingest_preprocess_flow(
    dataset: str,
    config_path: str | None = None,
    preprocess_config: str | None = None,
    priority: str | None = "standard",
) -> None:
    launch_ingestion(dataset, config_path, priority)
    launch_preprocess(dataset, preprocess_config or _default_preprocess_config(dataset))


def _default_preprocess_config(dataset: str) -> str:
    return str(Path(f"config/preprocess/{dataset}.json"))


if __name__ == "__main__":  # pragma: no cover
    ingest_preprocess_flow(
        "fleurs",
        str(Path("config/ingestion/fleurs_dev.json")),
        str(Path("config/preprocess/fleurs.json")),
    )
