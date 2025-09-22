"""Audio feature extraction utilities (log-mel spectrogram)."""
from __future__ import annotations

import math
import wave
from pathlib import Path
from typing import Tuple

import numpy as np


def _load_wav(path: Path) -> Tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as wf:
        sample_width = wf.getsampwidth()
        if sample_width != 2:
            raise ValueError("Only 16-bit PCM WAV files are supported")
        frame_rate = wf.getframerate()
        channels = wf.getnchannels()
        frames = wf.readframes(wf.getnframes())

    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    if channels == 2:
        audio = audio.reshape(-1, 2).mean(axis=1)
    audio /= 32768.0
    return audio, frame_rate


def _mel_filterbank(sample_rate: int, n_fft: int, n_mels: int) -> np.ndarray:
    def hz_to_mel(freq: float) -> float:
        return 2595.0 * math.log10(1.0 + freq / 700.0)

    def mel_to_hz(mel: float) -> float:
        return 700.0 * (10 ** (mel / 2595.0) - 1.0)

    mel_min = hz_to_mel(0)
    mel_max = hz_to_mel(sample_rate / 2)
    mels = np.linspace(mel_min, mel_max, n_mels + 2)
    hzs = mel_to_hz(mels)
    bins = np.floor((n_fft + 1) * hzs / sample_rate).astype(int)
    bins = np.clip(bins, 0, n_fft // 2)

    filterbank = np.zeros((n_mels, n_fft // 2 + 1), dtype=np.float32)
    for m in range(1, n_mels + 1):
        left, center, right = bins[m - 1 : m + 2]
        right = min(right, n_fft // 2)
        center = min(center, right)
        if center <= left:
            center = left + 1
        if right <= center:
            right = center + 1
        right = min(right, n_fft // 2)
        for k in range(left, center):
            filterbank[m - 1, k] = (k - left) / max(center - left, 1)
        for k in range(center, right):
            filterbank[m - 1, k] = (right - k) / max(right - center, 1)
    return filterbank


def log_mel_spectrogram(
    audio: np.ndarray,
    sample_rate: int,
    *,
    frame_length_ms: float = 25.0,
    frame_shift_ms: float = 10.0,
    n_mels: int = 80,
) -> np.ndarray:
    frame_length = int(sample_rate * frame_length_ms / 1000.0)
    frame_shift = int(sample_rate * frame_shift_ms / 1000.0)
    if frame_length <= 0 or frame_shift <= 0:
        raise ValueError("Frame length and shift must be positive")

    n_fft = 1
    while n_fft < frame_length:
        n_fft *= 2

    window = np.hamming(frame_length).astype(np.float32)
    num_frames = max(1, 1 + (len(audio) - frame_length) // frame_shift)
    if len(audio) < frame_length:
        pad_width = frame_length - len(audio)
        audio = np.pad(audio, (0, pad_width))
    frames = np.lib.stride_tricks.sliding_window_view(audio, frame_length)[::frame_shift][:num_frames]
    frames = frames * window

    stft = np.fft.rfft(frames, n=n_fft)
    magnitude = np.abs(stft) ** 2

    filterbank = _mel_filterbank(sample_rate, n_fft, n_mels)
    mel_spec = magnitude @ filterbank.T
    mel_spec = np.maximum(mel_spec, 1e-10)
    return np.log10(mel_spec).astype(np.float32)


def extract_log_mel(
    wav_path: Path,
    output_path: Path,
    *,
    frame_length_ms: float = 25.0,
    frame_shift_ms: float = 10.0,
    n_mels: int = 80,
) -> Path:
    audio, sample_rate = _load_wav(wav_path)
    features = log_mel_spectrogram(
        audio,
        sample_rate,
        frame_length_ms=frame_length_ms,
        frame_shift_ms=frame_shift_ms,
        n_mels=n_mels,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_path, features)
    return output_path
