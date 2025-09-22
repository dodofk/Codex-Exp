from __future__ import annotations

import math
import wave
from array import array
from pathlib import Path

import numpy as np

from preprocess.features import extract_log_mel


def _write_wav(path: Path, samples: array, sample_rate: int, channels: int = 1) -> None:
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())


def test_log_mel_handles_silence(tmp_path: Path) -> None:
    wav_path = tmp_path / "silence.wav"
    samples = array("h", [0] * 1600)
    _write_wav(wav_path, samples, sample_rate=16000)

    feature_path = tmp_path / "silence.npy"
    extract_log_mel(wav_path, feature_path)

    mel = np.load(feature_path)
    assert mel.shape[1] == 80
    assert np.isfinite(mel).all()


def test_log_mel_downmixes_stereo(tmp_path: Path) -> None:
    wav_path = tmp_path / "stereo.wav"
    sample_rate = 16000
    duration = 0.1
    samples_per_channel = int(sample_rate * duration)
    sine = [int(30000 * math.sin(2 * math.pi * 440 * t / sample_rate)) for t in range(samples_per_channel)]
    # Create stereo by interleaving identical channels
    interleaved = array("h")
    for sample in sine:
        interleaved.extend([sample, sample])
    _write_wav(wav_path, interleaved, sample_rate=sample_rate, channels=2)

    feature_path = tmp_path / "stereo.npy"
    extract_log_mel(wav_path, feature_path, n_mels=40)

    mel = np.load(feature_path)
    assert mel.shape[1] == 40
    # Energy should be non-zero since we fed a sine wave.
    assert np.any(mel > -5)
