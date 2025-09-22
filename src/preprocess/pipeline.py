"""Preprocessing pipeline scaffolding."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .config import PreprocessConfig, StepConfig
from ingestion.logging_utils import log_event
from .audio_utils import AudioConfig, preprocess_audio
from .features import extract_log_mel
from .lineage import LineageRecord, append_lineage


class PreprocessPipeline:
    """Simple pipeline that reports planned preprocessing steps."""

    def __init__(self, config: PreprocessConfig) -> None:
        self.config = config

    def plan(self) -> Iterable[str]:
        yield f"Dataset: {self.config.dataset}"
        yield f"Input dir: {self.config.input_dir}"
        yield f"Output dir: {self.config.output_dir}"
        yield f"Target sample rate: {self.config.sample_rate}"
        for step in self.config.steps:
            yield f"Step: {step.name} ({step.params})"

    def execute(self) -> None:
        output_root = Path(self.config.output_dir)
        input_root = Path(self.config.input_dir)
        log_root = output_root / "logs"
        log_event(
            self.config.dataset,
            "preprocess_start",
            {"output": str(self.config.output_dir)},
            log_root,
        )
        audio_cfg = AudioConfig(target_sample_rate=self.config.sample_rate)
        feature_steps: list[StepConfig] = []
        for step in self.config.steps:
            if step.name == "resample":
                audio_cfg.target_sample_rate = int(
                    step.params.get("rate", audio_cfg.target_sample_rate)
                )
            elif step.name == "normalize_volume":
                audio_cfg.target_dbfs = float(
                    step.params.get("target_dbfs", audio_cfg.target_dbfs)
                )
            elif step.name == "trim_silence":
                audio_cfg.trim_silence_enabled = True
                audio_cfg.trim_silence_threshold_db = float(
                    step.params.get("threshold_db", audio_cfg.trim_silence_threshold_db)
                )
            elif step.name == "extract_features":
                feature_steps.append(step)

        audio_files = sorted(input_root.rglob("*.wav"))
        processed_count = 0
        for audio_input in audio_files:
            rel_path = audio_input.relative_to(input_root)
            audio_output = output_root / rel_path
            audio_output.parent.mkdir(parents=True, exist_ok=True)
            preprocess_audio(audio_input, audio_output, audio_cfg)
            log_event(
                self.config.dataset,
                "preprocess_file_complete",
                {"input": str(audio_input), "output": str(audio_output)},
                log_root,
            )
            append_lineage(
                LineageRecord(
                    dataset=self.config.dataset,
                    step="audio_preprocess",
                    input_path=str(audio_input),
                    output_path=str(audio_output),
                    metadata={
                        "target_sample_rate": audio_cfg.target_sample_rate,
                        "steps": [step.name for step in self.config.steps],
                    },
                ),
                output_root,
            )
            processed_count += 1

            for step in feature_steps:
                feature_type = step.params.get("type", "log_mel").lower()
                feature_dir = output_root / "features" / rel_path.parent
                if feature_type == "log_mel":
                    frame_len = float(step.params.get("frame_length", 25))
                    frame_shift = float(step.params.get("frame_shift", 10))
                    n_mels = int(step.params.get("n_mels", 80))
                    feature_name = rel_path.with_suffix(".logmel.npy").name
                    feature_path = feature_dir / feature_name
                    extract_log_mel(
                        audio_output,
                        feature_path,
                        frame_length_ms=frame_len,
                        frame_shift_ms=frame_shift,
                        n_mels=n_mels,
                    )
                    append_lineage(
                        LineageRecord(
                            dataset=self.config.dataset,
                            step="features_log_mel",
                            input_path=str(audio_output),
                            output_path=str(feature_path),
                            metadata={
                                "frame_length_ms": frame_len,
                                "frame_shift_ms": frame_shift,
                                "n_mels": n_mels,
                            },
                        ),
                        output_root,
                    )
                else:  # pragma: no cover
                    raise NotImplementedError(f"Unsupported feature type: {feature_type}")

        log_event(
            self.config.dataset,
            "preprocess_complete",
            {"processed_files": processed_count},
            log_root,
        )


def build_pipeline(config_path: str | Path) -> PreprocessPipeline:
    from .config import load_config

    cfg = load_config(config_path)
    return PreprocessPipeline(cfg)
