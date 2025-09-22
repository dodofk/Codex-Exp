from __future__ import annotations

import pytest

from model.registries import get_text_tower


@pytest.mark.parametrize(
    "tower_name, config",
    [
        (
            "qwen3",
            {
                "checkpoint": "sshleifer/tiny-gpt2",
                "enable_lora": False,
                "max_length": 16,
            },
        ),
        (
            "phi2_lora",
            {
                "checkpoint": "sshleifer/tiny-gpt2",
                "enable_lora": False,
                "max_length": 32,
            },
        ),
    ],
)
def test_hf_text_tower_embedding_shape(tower_name: str, config: dict[str, object]) -> None:
    torch = pytest.importorskip("torch")

    tower = get_text_tower(tower_name, config)
    batch = {"text": ["hello world", "retrieval"]}
    embeddings = tower.embed_text(batch)

    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] == tower.embedding_dim
    assert isinstance(embeddings, torch.Tensor)
