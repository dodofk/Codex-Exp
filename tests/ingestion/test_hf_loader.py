from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from ingestion import hf_loader


class FakeDataset:
    def __init__(self, records):
        self.records = records
        self.selected = None

    def select(self, indices):
        self.selected = indices
        return FakeDataset(self.records[: len(indices)])

    def to_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            for row in self.records:
                handle.write(json.dumps(row) + "\n")


def test_download_subset_non_streaming(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fake_ds = FakeDataset([{"id": 1}, {"id": 2}])

    def fake_load_dataset(dataset, config, split, streaming=False, use_auth_token=None, **kwargs):
        assert dataset == "facebook/covost2"
        assert config == "en_fr"
        assert split == "train[:5%]"
        assert streaming is False
        assert use_auth_token == "fake"
        return fake_ds

    monkeypatch.setattr(hf_loader, "load_dataset", fake_load_dataset)
    os.environ["HF_TOKEN"] = "fake"

    output_dir = tmp_path / "out"
    path = hf_loader.download_subset(
        dataset="facebook/covost2",
        config="en_fr",
        split="train[:5%]",
        output_dir=output_dir,
        limit=2,
        token=os.environ["HF_TOKEN"],
    )

    assert path.exists()
    content = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(content) == 2


def test_cli_uses_env_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload_file = tmp_path / "payload.json"
    payload_file.write_text(json.dumps({"dataset": "facebook/covost2", "config": "en_fr", "split": "train[:1%]", "output_dir": str(tmp_path / "out")}), encoding="utf-8")

    def fake_load_dataset(dataset, config, split, streaming=False, use_auth_token=None, **kwargs):
        return FakeDataset([{"id": 1}])

    monkeypatch.setattr(hf_loader, "load_dataset", fake_load_dataset)
    env_file = tmp_path / ".env"
    env_file.write_text("HF_TOKEN=fake", encoding="utf-8")

    exit_code = hf_loader.main([
        "--dataset", "facebook/covost2",
        "--config", "en_fr",
        "--split", "train[:1%]",
        "--output", str(tmp_path / "out"),
        "--env-file", str(env_file),
    ])

    assert exit_code == 0
    assert (tmp_path / "out").exists()
