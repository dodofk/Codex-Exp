"""Metric utilities for retrieval evaluation."""

from __future__ import annotations

import numpy as np
from sacrebleu.metrics import BLEU


DEFAULT_THRESHOLDS = {
    "recall_at_1": 0.10,
    "mrr": 0.20,
    "bleu": 5.0,
}

_BLEU = BLEU(effective_order=True)


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


def compute_bleu(predictions: list[str], references: list[str]) -> float:
    if not predictions or not references:
        return 0.0
    pairs = [
        (pred or "", ref or "")
        for pred, ref in zip(predictions, references)
    ]
    if not pairs:
        return 0.0
    preds_clean, refs_clean = zip(*pairs)
    score = _BLEU.corpus_score(list(preds_clean), [list(refs_clean)]).score
    return float(score)


def evaluate_smoke_run(
    similarity_matrix: np.ndarray,
    predictions: list[str] | None = None,
    references: list[str] | None = None,
) -> dict[str, float]:
    metrics: dict[str, float] = {
        "recall_at_1": compute_recall_at_1(similarity_matrix),
        "mrr": compute_mrr(similarity_matrix),
    }
    if predictions is not None and references is not None:
        metrics["bleu"] = compute_bleu(predictions, references)
    else:
        metrics["bleu"] = 0.0
    return metrics


__all__ = [
    "DEFAULT_THRESHOLDS",
    "compute_recall_at_1",
    "compute_mrr",
    "compute_bleu",
    "evaluate_smoke_run",
]
