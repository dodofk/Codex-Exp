from __future__ import annotations

import json
from pathlib import Path

from preprocess.pipeline import PreprocessPipeline, build_pipeline


def _write_config(tmp_path: Path) -> Path:
    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "dataset": "demo",
                "input_dir": "data/raw/demo",
                "output_dir": "data/processed/demo",
                "sample_rate": 16000,
                "steps": [
                    {"name": "resample", "params": {"rate": 16000}},
                    {"name": "features", "params": {"type": "log_mel"}},
                ],
            }
        ),
        encoding="utf-8",
    )
    return config


def test_build_pipeline(tmp_path: Path) -> None:
    cfg_path = _write_config(tmp_path)
    pipeline = build_pipeline(cfg_path)
    lines = list(pipeline.plan())

    assert "Dataset: demo" in lines[0]
    assert any("resample" in line for line in lines)


def test_execute_not_implemented(tmp_path: Path) -> None:
    cfg_path = _write_config(tmp_path)
    pipeline = build_pipeline(cfg_path)

    try:
        pipeline.execute()
    except NotImplementedError:
        pass
    else:  # pragma: no cover - safeguard
        raise AssertionError("execute should raise NotImplementedError")
