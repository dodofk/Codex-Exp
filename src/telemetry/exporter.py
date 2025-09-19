"""Telemetry exporter stubs for ingestion/preprocessing."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

try:  # pragma: no cover - optional dependency
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
except ModuleNotFoundError:  # pragma: no cover
    trace = None  # type: ignore


def _use_console_exporter() -> bool:
    return bool(os.getenv("OTEL_EXPORTER_CONSOLE"))


def init_tracer(service_name: str = "auto-paper") -> None:
    if trace is None or not _use_console_exporter():
        return
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def emit_event(dataset: str, event: str, payload: Dict[str, Any], log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    entry = {"dataset": dataset, "event": event, **payload}
    with (log_dir / "telemetry.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")
