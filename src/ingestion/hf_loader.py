"""Hugging Face datasets integration helpers."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable, Iterator, Optional

from .env import load_env_file
from .logging_utils import log_event

try:  # pragma: no cover - optional dependency
    from datasets import load_dataset  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    load_dataset = None  # type: ignore

DEFAULT_OUTPUT_FORMAT = "jsonl"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download Hugging Face dataset subsets")
    parser.add_argument("--dataset", required=True, help="Dataset repository name (e.g., facebook/covost2)")
    parser.add_argument("--config", help="Dataset configuration/language pair")
    parser.add_argument("--split", default="train", help="Split or slice notation (default: train)")
    parser.add_argument("--limit", type=int, help="Optional row cap for non-streaming datasets")
    parser.add_argument("--streaming", action="store_true", help="Use streaming API (iterates subset; requires limit)")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for saved subset")
    parser.add_argument("--format", choices=["jsonl", "parquet"], default=DEFAULT_OUTPUT_FORMAT)
    parser.add_argument("--env-file", type=Path, default=Path(".env.ingestion"), help="Env file containing HF_TOKEN if needed")
    parser.add_argument("--token", help="Explicit Hugging Face access token (overrides env)")
    parser.add_argument("--metadata", help="Optional JSON metadata to log alongside the download")
    return parser


def _ensure_datasets():
    if load_dataset is None:
        raise RuntimeError(
            "datasets library is required. Ensure it is installed (e.g., run `uv sync`)."
        )


def _iter_stream(dataset, limit: Optional[int]) -> Iterator[dict]:  # pragma: no cover - streaming not exercised in tests
    count = 0
    for record in dataset:
        yield record
        count += 1
        if limit is not None and count >= limit:
            break


def _write_jsonl(records: Iterable[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in records:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def download_subset(
    dataset: str,
    config: Optional[str],
    split: str,
    output_dir: Path,
    file_format: str = DEFAULT_OUTPUT_FORMAT,
    limit: Optional[int] = None,
    streaming: bool = False,
    token: Optional[str] = None,
) -> Path:
    _ensure_datasets()

    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir = output_dir / "logs"
    log_event(dataset, "hf_ingestion_start", {"config": config, "split": split}, log_dir)

    ds = load_dataset(
        dataset,
        config,
        split=split,
        streaming=streaming,
        use_auth_token=token,
        trust_remote_code=True,
    )
    split_safe = split.replace('/', '_').replace(':', '-')

    if streaming:
        if limit is None:
            raise ValueError("limit must be provided when streaming=True")
        records = _iter_stream(ds, limit)
        file_path = output_dir / f"{config or 'default'}_{split_safe}.jsonl"
        _write_jsonl(records, file_path)
    else:
        subset = ds.select(range(limit)) if limit is not None else ds
        if file_format == "jsonl":
            file_path = output_dir / f"{config or 'default'}_{split_safe}.jsonl"
            subset.to_json(str(file_path))
        else:
            file_path = output_dir / f"{config or 'default'}_{split_safe}.parquet"
            subset.to_parquet(str(file_path))

    log_event(
        dataset,
        "hf_ingestion_complete",
        {
            "config": config,
            "split": split,
            "path": str(file_path),
            "rows": int(limit) if limit is not None and not streaming else None,
        },
        log_dir,
    )
    return file_path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    load_env_file(args.env_file)
    token = args.token or os.getenv("HF_TOKEN")

    args.output.mkdir(parents=True, exist_ok=True)
    metadata = json.loads(args.metadata) if args.metadata else None
    if metadata:
        log_event(args.dataset, "hf_ingestion_metadata", metadata, args.output / "logs")

    download_subset(
        dataset=args.dataset,
        config=args.config,
        split=args.split,
        output_dir=args.output,
        file_format=args.format,
        limit=args.limit,
        streaming=args.streaming,
        token=token,
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
