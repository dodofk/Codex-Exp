#!/usr/bin/env python3
"""Print the download plan for the FLEURS five-language subset.

This mirrors the behaviour of `python -m ingestion.cli config/ingestion/fleurs_dev.json --plan`
but keeps the invocation handy for quick experimentation.
"""
from __future__ import annotations

from pathlib import Path

from ingestion.config import load_config
from ingestion.tasks import plan_download, render_plan


def main() -> None:
    config_path = Path("config/ingestion/fleurs_dev.json")
    dataset_config = load_config(config_path)
    plan = plan_download(dataset_config)
    print(render_plan(plan))


if __name__ == "__main__":
    main()
