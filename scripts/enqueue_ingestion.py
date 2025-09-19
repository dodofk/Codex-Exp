"""Helper CLI for enqueueing ingestion-style jobs locally."""
from __future__ import annotations

import argparse
import json

from ingestion.worker import main as worker_main


def build_payload(
    dataset: str,
    config: str | None,
    artifacts: list[str] | None,
    priority: str | None,
    metadata_items: list[str] | None,
) -> str:
    payload = {"dataset": dataset}
    if config:
        payload["config_path"] = config
    if artifacts:
        payload["artifacts"] = artifacts
    if priority:
        payload.setdefault("metadata", {})["priority"] = priority
    if metadata_items:
        user_meta = {}
        for item in metadata_items:
            if "=" not in item:
                raise ValueError(f"Metadata must be key=value, got: {item}")
            key, value = item.split("=", 1)
            user_meta[key.strip()] = value.strip()
        payload.setdefault("metadata", {}).update(user_meta)
    return json.dumps(payload)


def run(args: argparse.Namespace) -> int:
    payload_json = build_payload(
        args.dataset,
        args.config,
        args.artifact,
        args.priority,
        args.metadata,
    )
    cli_args = ["--payload-json", payload_json]
    if args.plan:
        cli_args.append("--plan")
    else:
        cli_args.append("--run")
    return worker_main(cli_args)


def main() -> int:
    parser = argparse.ArgumentParser(description="Enqueue ingestion jobs locally")
    parser.add_argument("dataset", help="Dataset name, e.g. fleurs")
    parser.add_argument("--config", help="Override config path", default=None)
    parser.add_argument(
        "--artifact",
        action="append",
        help="Restrict to a specific artifact (repeatable)",
    )
    parser.add_argument(
        "--priority",
        choices=["low", "standard", "high"],
        help="Queue priority hint (stored in metadata)",
    )
    parser.add_argument(
        "--metadata",
        action="append",
        help="Additional metadata entries key=value (repeatable)",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Plan only; default runs ingestion",
    )
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
