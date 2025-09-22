from __future__ import annotations

import numpy as np

from model.metrics import compute_mrr, compute_recall_at_1


def test_metrics_with_perfect_similarity() -> None:
    sim = np.eye(3)
    assert compute_recall_at_1(sim) == 1.0
    assert compute_mrr(sim) == 1.0


def test_metrics_with_random_similarity() -> None:
    sim = np.array(
        [
            [0.9, 0.1, 0.0],
            [0.2, 0.5, 0.3],
            [0.3, 0.4, 0.8],
        ]
    )
    mrr = compute_mrr(sim)
    assert 0.0 <= mrr <= 1.0
