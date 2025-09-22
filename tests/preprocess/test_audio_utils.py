from __future__ import annotations

from pathlib import Path
import math
import wave
from array import array

from preprocess.audio_utils import AudioConfig, normalize_dbfs, preprocess_audio


def test_normalize_dbfs() -> None:
    sample_width = 2
    samples = array("h", [1000] * 8000)
    normalized = normalize_dbfs(samples, target_dbfs=-20)
    rms = math.sqrt(sum(s * s for s in normalized) / len(normalized))
    dbfs = 20 * math.log10(rms / 32767)
    assert abs(dbfs + 20) < 1e-2


def test_preprocess_audio(tmp_path: Path, monkeypatch) -> None:
    src = tmp_path / "input.wav"
    dst = tmp_path / "output.wav"

    with wave.open(str(src), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(8000)
        wf.writeframes(bytes(array("h", [1000] * 8000)))

    preprocess_audio(src, dst, AudioConfig(target_sample_rate=16000, target_dbfs=-30))

    assert dst.exists()
    with wave.open(str(dst), "rb") as wf:
        assert wf.getframerate() == 16000
