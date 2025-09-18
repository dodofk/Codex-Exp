"""Ingestion task scaffolding.

This module provides placeholder implementations that will be expanded with
real download and checksum verification logic in subsequent iterations.
"""
from __future__ import annotations

import hashlib
import shutil
import time
from pathlib import Path
from typing import Iterable, List
import urllib.error
import urllib.request

from .logging_utils import log_event
from .env import expand_headers

from .config import ArtifactSpec, DatasetConfig


def plan_download(config: DatasetConfig) -> dict[str, str | Path | list[dict[str, str]]]:
    """Return a structured plan describing the download steps.

    The plan currently acts as documentation to assist with manual validation
    and will become actionable automation in future revisions.
    """

    artifacts: List[dict[str, str]] = [
        {
            "filename": artifact.filename,
            "url": artifact.url,
            "sha256": artifact.sha256 or "(not provided)",
        }
        for artifact in config.artifacts
    ]

    return {
        "dataset": config.name,
        "version": config.version,
        "source": config.source_url,
        "target": str(config.output_dir / config.name / config.version),
        "checksum_manifest": config.checksum_manifest or "(not provided)",
        "artifacts": artifacts,
    }


def render_plan(plan: dict[str, str | Path]) -> str:
    """Render the plan as a human-readable summary."""

    lines: Iterable[str] = (
        f"Dataset: {plan['dataset']}",
        f"Version: {plan['version']}",
        f"Source URL: {plan['source']}",
        f"Target Directory: {plan['target']}",
        f"Checksum Manifest: {plan['checksum_manifest']}",
    )
    artifact_lines = []
    for artifact in plan.get("artifacts", []):
        artifact_lines.append(
            f"  - {artifact['filename']} ({artifact['url']})"
            + (f" [sha256={artifact['sha256']}]" if artifact.get("sha256") else "")
        )

    return "\n".join(str(item) for item in (*lines, *artifact_lines))


def _calculate_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_target(root: Path, artifact: ArtifactSpec) -> Path:
    return root / artifact.filename


def _artifact_already_valid(target: Path, artifact: ArtifactSpec) -> bool:
    if not target.exists() or not artifact.sha256:
        return False
    return _calculate_sha256(target).lower() == artifact.sha256.lower()


def _http_range_header(start: int) -> dict[str, str]:
    return {"Range": f"bytes={start}-"}


def _download_artifact(
    dataset: str,
    data_root: Path,
    log_root: Path,
    artifact: ArtifactSpec,
    attempts: int = 3,
) -> dict[str, str]:
    target = _artifact_target(data_root, artifact)
    target.parent.mkdir(parents=True, exist_ok=True)

    if _artifact_already_valid(target, artifact):
        log_event(
            dataset,
            "artifact_skipped",
            {"filename": artifact.filename, "path": str(target)},
            log_root,
        )
        return {"filename": artifact.filename, "status": "skipped", "path": str(target)}

    tmp_path = target.with_suffix(target.suffix + ".part")
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            start_time = time.time()
            log_event(
                dataset,
                "artifact_download_start",
                {"filename": artifact.filename, "url": artifact.url, "attempt": attempt},
                log_root,
            )
            existing_size = tmp_path.stat().st_size if tmp_path.exists() else 0
            request = urllib.request.Request(artifact.url)
            if existing_size:
                request.headers.update(_http_range_header(existing_size))

            if artifact.headers:
                headers = expand_headers(artifact.headers)
                if headers:
                    request.headers.update(headers)

            bytes_written = 0
            mode = "ab" if existing_size else "wb"
            with urllib.request.urlopen(request) as response, tmp_path.open(mode) as handle:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    handle.write(chunk)
                    bytes_written += len(chunk)
            shutil.move(tmp_path, target)

            if artifact.sha256:
                digest = _calculate_sha256(target)
                if digest.lower() != artifact.sha256.lower():
                    target.unlink(missing_ok=True)
                    raise ValueError(
                        f"Checksum mismatch for {artifact.filename}: expected "
                        f"{artifact.sha256}, got {digest}"
                    )
            duration = time.time() - start_time
            log_event(
                dataset,
                "artifact_download_complete",
                {
                    "filename": artifact.filename,
                    "path": str(target),
                    "bytes": bytes_written,
                    "duration_sec": round(duration, 3),
                },
                log_root,
            )
            status = "verified" if artifact.sha256 else "downloaded"
            return {"filename": artifact.filename, "status": status, "path": str(target)}
        except (urllib.error.URLError, ValueError) as exc:
            last_error = exc
            tmp_path.unlink(missing_ok=True)
            if attempt < attempts:
                log_event(
                    dataset,
                    "artifact_download_retry",
                    {"filename": artifact.filename, "error": str(exc), "attempt": attempt},
                    log_root,
                )
                time.sleep(min(2 ** attempt, 5))
                continue
            log_event(
                dataset,
                "artifact_download_failed",
                {"filename": artifact.filename, "error": str(exc)},
                log_root,
            )
            raise

    # Should never reach here because we either return or raise in the loop.
    raise RuntimeError(f"Failed to download artifact {artifact.filename}") from last_error


def execute(config: DatasetConfig) -> None:  # pragma: no cover - placeholder
    """Execute the ingestion workflow.

    Downloads each artifact and validates checksums when specified.
    """
    if not config.artifacts:
        raise ValueError(
            "No artifacts defined for dataset. Update the ingestion config with "
            "a list of files to download."
        )

    target_root = config.output_dir / config.name / config.version
    log_dir = config.output_dir / config.name / "logs"
    start = time.time()
    log_event(config.name, "ingestion_start", {"version": config.version}, log_dir)
    for artifact in config.artifacts:
        _download_artifact(config.name, target_root, log_dir, artifact)
    duration = time.time() - start
    log_event(
        config.name,
        "ingestion_complete",
        {"version": config.version, "duration_sec": round(duration, 3)},
        log_dir,
    )
