"""Smoke evaluation utilities for retrieval metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np

from model.metrics import (
    DEFAULT_THRESHOLDS,
    compute_mrr,
    compute_recall_at_1,
    evaluate_smoke_run as core_evaluate_smoke_run,
)


@dataclass
class MetricReport:
    values: Dict[str, float]

    def passes(self, thresholds: Dict[str, float] = DEFAULT_THRESHOLDS) -> bool:
        return all(self.values.get(metric, 0.0) >= threshold for metric, threshold in thresholds.items())


def evaluate_smoke_run(
    similarity_matrix: np.ndarray,
    predictions: list[str] | None = None,
    references: list[str] | None = None,
) -> MetricReport:
    return MetricReport(values=core_evaluate_smoke_run(similarity_matrix, predictions, references))
