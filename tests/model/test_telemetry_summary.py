from __future__ import annotations

import json
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import model_telemetry_summary as summary


def _write_run(run_dir: Path, run_id: str, metrics: list[dict], eval_metrics: dict[str, float]) -> None:
    run_path = run_dir / run_id
    run_path.mkdir(parents=True, exist_ok=True)
    telemetry_events = [
        {"event": "run_start", "dataset_root": "data/processed/demo"},
        {"event": "train_epoch_end", "epoch": 0},
    ]
    with (run_path / "telemetry.jsonl").open("w", encoding="utf-8") as handle:
        for event in telemetry_events:
            handle.write(json.dumps(event) + "\n")

    records = []
    for record in metrics:
        records.append({"event": "train_epoch_end", **record})
    records.append({"event": "eval_complete", "metrics": eval_metrics})
    with (run_path / "metrics.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")


def test_model_telemetry_summary(tmp_path: Path) -> None:
    log_dir = tmp_path / "logs"
    run_metrics = [{"epoch": 0, "metrics": {"loss": 0.5}}, {"epoch": 1, "metrics": {"loss": 0.4}}]
    eval_metrics = {"recall_at_1": 0.5, "mrr": 0.6, "bleu": 10.0}
    _write_run(log_dir, "runA", run_metrics, eval_metrics)

    output_path = tmp_path / "telemetry" / "model_summary.json"
    summary.aggregate_runs(log_dir, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert data["runs"][0]["run_id"] == "runA"
    assert data["runs"][0]["epochs"] == 2
    dataset_entry = data["dataset_summary"][0]
    assert dataset_entry["dataset"] == "data/processed/demo"
    assert dataset_entry["bleu"] == 10.0
