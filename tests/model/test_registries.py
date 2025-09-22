from __future__ import annotations

from model.registries import get_audio_tower, get_text_tower


def test_registry_returns_instances():
    text = get_text_tower("identity", {"embedding_dim": 16})
    audio = get_audio_tower("mean_pooling", {"embedding_dim": 16})

    batch = {
        "text_tokens": [[1, 2, 3], [4, 5, 6]],
        "audio_features": [[[0.1] * 4] * 2, [[0.2] * 4] * 2],
    }

    text_embed = text.embed_text(batch)
    audio_embed = audio.embed_audio(batch)

    assert text_embed.shape[1] == 16
    assert audio_embed.shape[1] == 16
