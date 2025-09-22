"""Metric utilities for retrieval evaluation."""

from __future__ import annotations

import numpy as np


DEFAULT_THRESHOLDS = {
    "recall_at_1": 0.10,
    "mrr": 0.20,
    "bleu": 5.0,
}


def compute_recall_at_1(similarity_matrix: np.ndarray) -> float:
    correct = np.argmax(similarity_matrix, axis=1)
    hits = (correct == np.arange(similarity_matrix.shape[0])).mean()
    return float(hits)


def compute_mrr(similarity_matrix: np.ndarray) -> float:
    ranks = []
    for idx, row in enumerate(similarity_matrix):
        sorted_idx = np.argsort(row)[::-1]
        rank = np.where(sorted_idx == idx)[0]
        ranks.append(1.0 / (rank[0] + 1) if rank.size else 0.0)
    return float(np.mean(ranks))


def evaluate_smoke_run(similarity_matrix: np.ndarray) -> dict[str, float]:
    return {
        "recall_at_1": compute_recall_at_1(similarity_matrix),
        "mrr": compute_mrr(similarity_matrix),
        "bleu": 0.0,  # TODO: integrate text metrics
    }


__all__ = [
    "DEFAULT_THRESHOLDS",
    "compute_recall_at_1",
    "compute_mrr",
    "evaluate_smoke_run",
]
