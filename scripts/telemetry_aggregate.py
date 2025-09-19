from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def aggregate(log_dir: Path) -> None:
    telemetry_file = log_dir / "telemetry.jsonl"
    if not telemetry_file.exists():
        print("No telemetry found", flush=True)
        return

    events = Counter()
    bytes_totals = defaultdict(int)
    duration_totals = defaultdict(float)
    with telemetry_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            entry = json.loads(line)
            key = (entry.get("dataset"), entry.get("event"))
            events[key] += 1
            if "bytes" in entry:
                bytes_totals[key] += int(entry["bytes"])
            if "duration_sec" in entry:
                duration_totals[key] += float(entry["duration_sec"])

    for (dataset, event), count in sorted(events.items()):
        details = []
        total_bytes = bytes_totals.get((dataset, event))
        if total_bytes:
            details.append(f"bytes={total_bytes}")
        total_duration = duration_totals.get((dataset, event))
        if total_duration:
            details.append(f"duration_sec={total_duration:.3f}")
        suffix = f" ({', '.join(details)})" if details else ""
        print(f"{dataset}:{event} count={count}{suffix}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate telemetry logs")
    parser.add_argument("log_dir", type=Path)
    args = parser.parse_args()
    aggregate(args.log_dir)


if __name__ == "__main__":
    main()
