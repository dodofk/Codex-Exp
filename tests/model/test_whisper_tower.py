from __future__ import annotations

import pytest

from model.registries import get_audio_tower


def test_distil_whisper_embedding_shape():
    torch = pytest.importorskip("torch")

    tower = get_audio_tower(
        "distil_whisper",
        {
            "checkpoint": "openai/whisper-tiny",
            "feature_dim": 80,
        },
    )
    batch = {
        "audio_features": [[[0.1] * 80] * 4, [[0.2] * 80] * 4],
    }
    embeddings = tower.embed_audio(batch)
    assert embeddings.shape[0] == 2
    assert isinstance(embeddings, torch.Tensor)
