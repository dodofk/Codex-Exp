"""Command line interface for preprocessing pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import build_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="preprocess",
        description="Dataset preprocessing tooling",
    )
    parser.add_argument("config", type=Path, help="Path to preprocessing config")
    parser.add_argument(
        "--plan",
        action="store_true",
        help="Print the preprocessing plan without executing",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    pipeline = build_pipeline(args.config)
    if args.plan:
        for line in pipeline.plan():
            print(line)
    else:
        pipeline.execute()
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
