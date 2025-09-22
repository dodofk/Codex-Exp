"""Audio preprocessing helpers using pure Python."""
from __future__ import annotations

import math
import wave
from array import array
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class AudioConfig:
    target_sample_rate: int = 16000
    target_dbfs: float = -20.0
    trim_silence_enabled: bool = False
    trim_silence_threshold_db: float = -40.0


def _read_wave(path: Path) -> Tuple[array, int, int]:
    with wave.open(str(path), "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        channels = wf.getnchannels()

    if sample_width != 2:
        raise ValueError("Only 16-bit PCM WAV files are supported")

    samples = array("h", frames)
    if channels == 2:
        samples = array("h", ((samples[i] + samples[i + 1]) // 2 for i in range(0, len(samples), 2)))

    return samples, frame_rate, channels


def _resample(samples: array, src_rate: int, tgt_rate: int) -> array:
    if src_rate == tgt_rate:
        return samples
    ratio = tgt_rate / src_rate
    new_length = max(1, int(len(samples) * ratio))
    resampled = array("h")
    for idx in range(new_length):
        src_pos = idx / ratio
        left = int(math.floor(src_pos))
        right = min(left + 1, len(samples) - 1)
        frac = src_pos - left
        value = int(samples[left] * (1 - frac) + samples[right] * frac)
        resampled.append(value)
    return resampled


def normalize_dbfs(samples: array, target_dbfs: float) -> array:
    rms = math.sqrt(sum(s * s for s in samples) / max(len(samples), 1)) or 1.0
    current_dbfs = 20 * math.log10(rms / 32767)
    gain = 10 ** ((target_dbfs - current_dbfs) / 20)
    normalized = array("h")
    for sample in samples:
        value = int(sample * gain)
        value = max(-32768, min(32767, value))
        normalized.append(value)
    return normalized


def _write_wave(path: Path, samples: array, sample_rate: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())


def preprocess_audio(src: Path, dst: Path, config: AudioConfig) -> None:
    samples, src_rate, _ = _read_wave(src)
    if config.trim_silence_enabled:
        samples = trim_silence(samples, threshold_db=config.trim_silence_threshold_db)
    samples = _resample(samples, src_rate, config.target_sample_rate)
    samples = normalize_dbfs(samples, config.target_dbfs)
    _write_wave(dst, samples, config.target_sample_rate)


def trim_silence(samples: array, threshold_db: float = -40.0, frame_size: int = 1024) -> array:
    if not samples:
        return samples
    threshold = 32767 * (10 ** (threshold_db / 20))
    length = len(samples)
    start = 0
    while start < length:
        frame = samples[start : start + frame_size]
        if not frame or max(abs(s) for s in frame) > threshold:
            break
        start += frame_size
    end = length
    while end > start:
        frame = samples[max(start, end - frame_size) : end]
        if not frame or max(abs(s) for s in frame) > threshold:
            break
        end -= frame_size
    return array("h", samples[start:end])
