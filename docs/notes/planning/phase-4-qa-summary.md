# Phase 4 QA Metrics Summary

_Last updated: 2025-09-21_

## Smoke Evaluation Thresholds
- **recall_at_1** ≥ 0.10 (baseline CPU smoke run target).
- **MRR** ≥ 0.20 (placeholder until true metric implemented).
- **BLEU** ≥ 5.0 (placeholder; to be revisited when text metrics wired).
- Thresholds codified in `scripts/model_eval.py::DEFAULT_THRESHOLDS`.

## QA Action Items
1. Implement MRR computation in `scripts/model_eval.py` once retrieval logits available.
2. Integrate BLEU measurement using tokenized transcript/reference pairs.
3. Wire CLI `--mode eval` to emit `MetricReport` JSONL for regression tracking.

## Notes
- Metrics tuned for smoke dataset (`fleurs_smoke`); adjust when scaling to full evaluation sets.
- QA to maintain golden metric snapshots under `data/metrics/golden/` once pipeline stabilizes.
