from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

DEFAULT_LOG_DIR = Path("data/logs/model")
DEFAULT_OUTPUT = Path("data/telemetry/model_summary.json")


def _identify_run_dirs(base: Path) -> list[Path]:
    if not base.exists():
        return []
    return sorted(p for p in base.iterdir() if p.is_dir())


def _load_metrics(path: Path) -> tuple[list[dict], list[dict]]:
    telemetry_path = path / "telemetry.jsonl"
    metrics_path = path / "metrics.jsonl"
    telemetry_events: list[dict] = []
    metrics_events: list[dict] = []

    if telemetry_path.exists():
        with telemetry_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    telemetry_events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if metrics_path.exists():
        with metrics_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    metrics_events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return telemetry_events, metrics_events


def aggregate_runs(log_dir: Path, output_path: Path) -> None:
    runs = _identify_run_dirs(log_dir)
    if not runs:
        print("No model runs found", flush=True)
        return

    summary: list[dict] = []
    aggregated: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for run_dir in runs:
        run_id = run_dir.name
        telemetry_events, metrics_events = _load_metrics(run_dir)

        train_epochs = [e for e in metrics_events if e.get("event") == "train_epoch_end"]
        eval_events = [e for e in metrics_events if e.get("event") == "eval_complete"]

        if eval_events:
            latest_eval = eval_events[-1]
            metrics = latest_eval.get("metrics", {})
        else:
            metrics = {}

        record = {
            "run_id": run_id,
            "epochs": len(train_epochs),
            "metrics": metrics,
        }

        if train_epochs:
            record["epoch_metrics"] = train_epochs

        summary.append(record)

        dataset_name = None
        for event in telemetry_events:
            if event.get("event") in {"run_start", "run_resume"}:
                dataset_name = event.get("dataset_root") or event.get("dataset") or dataset_name
        if dataset_name is None:
            dataset_name = "unknown"

        for key, value in metrics.items():
            try:
                aggregated[dataset_name][key].append(float(value))
            except (TypeError, ValueError):
                continue

    output = {"runs": summary}
    dataset_summary = []
    for dataset, metric_map in aggregated.items():
        dataset_entry = {"dataset": dataset}
        for key, values in metric_map.items():
            dataset_entry[key] = mean(values)
        dataset_summary.append(dataset_entry)
    output["dataset_summary"] = dataset_summary

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2, ensure_ascii=False)

    print(json.dumps(output, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize model training telemetry")
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR, help="Model log directory (default: data/logs/model)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output JSON path (default: data/telemetry/model_summary.json)")
    args = parser.parse_args()

    aggregate_runs(args.log_dir, args.output)


if __name__ == "__main__":
    main()
