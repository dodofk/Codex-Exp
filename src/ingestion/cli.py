"""Command line interface for ingestion scaffolding."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import load_config
from .tasks import execute, plan_download, render_plan
from .env import load_env_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ingestion",
        description="Dataset ingestion tooling (scaffolding)",
    )
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the dataset YAML configuration.",
    )
    parser.add_argument(
        "--artifact",
        action="append",
        dest="artifacts",
        help="Download only the specified artifact filename (can repeat).",
    )
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Print the download plan instead of executing the pipeline.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    load_env_file()
    dataset_config = load_config(args.config)
    if args.artifacts:
        dataset_config = dataset_config.with_artifacts(args.artifacts)

    if args.plan:
        plan = plan_download(dataset_config)
        print(render_plan(plan))
        return 0

    try:
        execute(dataset_config)
    except NotImplementedError as exc:  # pragma: no cover - placeholder path
        print(str(exc), file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
