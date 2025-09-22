from __future__ import annotations

import numpy as np
import pytest

from model.losses import InfoNCELoss


def test_infonce_loss_numpy() -> None:
    loss = InfoNCELoss(temperature=0.5, spreadout_weight=0.1)
    text = np.eye(2, dtype=np.float32)
    audio = np.eye(2, dtype=np.float32)
    result = loss(text, audio, {})
    assert "loss" in result
    assert result["similarity_mean"] == pytest.approx(1.0)


def test_infonce_loss_torch_backward() -> None:
    torch = pytest.importorskip("torch")
    loss = InfoNCELoss(temperature=0.5, spreadout_weight=0.1, spreadout_margin=0.05)
    text = torch.eye(2, requires_grad=True)
    audio = torch.eye(2, requires_grad=True)
    result = loss(text, audio, {})
    assert isinstance(result["loss"], torch.Tensor)
    result["loss"].backward()
    assert text.grad is not None
    assert audio.grad is not None
