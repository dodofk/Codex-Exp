from __future__ import annotations

import pytest

from model.registries import get_text_tower


def test_phi2_lora_embedding_shape():
    torch = pytest.importorskip("torch")

    tower = get_text_tower(
        "phi2_lora",
        {
            "checkpoint": "sshleifer/tiny-gpt2",
            "adapter_rank": 2,
            "max_length": 32,
        },
    )
    batch = {"text": ["hello world", "auto paper"]}
    embeddings = tower.embed_text(batch)
    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] == tower.embedding_dim
    assert isinstance(embeddings, torch.Tensor)
