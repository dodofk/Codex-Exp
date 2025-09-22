"""Smoke evaluation utilities for retrieval metrics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


DEFAULT_THRESHOLDS = {
    "recall_at_1": 0.10,
    "mrr": 0.20,
    "bleu": 5.0,
}


@dataclass
class MetricReport:
    values: Dict[str, float]

    def passes(self, thresholds: Dict[str, float] = DEFAULT_THRESHOLDS) -> bool:
        return all(self.values.get(metric, 0.0) >= threshold for metric, threshold in thresholds.items())


def compute_recall_at_1(similarity_matrix: np.ndarray) -> float:
    correct = np.argmax(similarity_matrix, axis=1)
    hits = (correct == np.arange(similarity_matrix.shape[0])).mean()
    return float(hits)


def evaluate_smoke_run(similarity_matrix: np.ndarray) -> MetricReport:
    return MetricReport(
        values={
            "recall_at_1": compute_recall_at_1(similarity_matrix),
            "mrr": 0.0,  # TODO: implement
            "bleu": 0.0,  # TODO: integrate text metrics
        }
    )
