from __future__ import annotations

import numpy as np
import pytest

from model.metrics import compute_bleu, compute_mrr, compute_recall_at_1, evaluate_smoke_run


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


def test_compute_bleu_perfect_match() -> None:
    preds = ["hello world", "foo bar"]
    refs = ["hello world", "foo bar"]
    score = compute_bleu(preds, refs)
    assert score == pytest.approx(100.0)


def test_evaluate_smoke_run_bleu_included() -> None:
    sim = np.eye(2)
    metrics = evaluate_smoke_run(sim, ["one", "two"], ["one", "two"])
    assert metrics["bleu"] == pytest.approx(100.0)
