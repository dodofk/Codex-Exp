# Preprocessing Specification (Phase 3 Draft)

## Scope
- Define normalization, tokenization, and feature extraction steps for speech/text corpora selected in Phase 2.
- Ensure outputs align with ADR-001 baseline (PaLM-compatible tokens, discrete audio tokens) and ADR-002 fallback if invoked.

## Pipeline Components
- Audio preprocessing: sample rate normalization (16 kHz), silence trimming, log-mel spectrogram extraction (numpy baseline) with optional k-means tokens for downstream models.
- Text preprocessing: language-specific normalization, SentencePiece tokenization, punctuation handling (per dataset).
- Metadata tracking: JSONL lineage capturing input checksum, transformation parameters, output hashes, and timestamps.

### Current Scaffolding
- Config loader: `src/preprocess/config.py`
- Pipeline wrapper & CLI: `src/preprocess/pipeline.py`, `src/preprocess/cli.py`
- Audio helpers: `src/preprocess/audio_utils.py` (resample + normalize)
- Example configs: `config/preprocess/fleurs.json` (full), `config/preprocess/fleurs_smoke.json` (subset), `config/preprocess/covost2_en_fr.json`
- Tests: `tests/preprocess/test_pipeline.py`, `tests/preprocess/test_audio_utils.py`, `tests/preprocess/test_feature_extraction.py`

## Action Items
- [x] Draft configuration templates (e.g., `config/preprocess/fleurs.json`).
- [x] Identify reusable libraries/tooling for feature extraction (torchaudio log-mel + SentencePiece tokenizer).
- [x] Define logging format for lineage (JSONL entries written via `src/preprocess/lineage.py`).
- [x] Coordinate file naming conventions with ingestion (`data/raw/<dataset>/<version>` -> `data/processed/<dataset>/<version>`).
- [x] Extend tests to cover edge cases (multi-channel audio, silence trimming, feature extraction).

### Lineage Format
- Location: `data/processed/<dataset>/<version>/lineage.jsonl`.
- Schema example:
  ```json
  {
    "dataset": "fleurs",
    "step": "audio_preprocess",
    "input_path": "data/raw/fleurs/v1/sample.wav",
    "output_path": "data/processed/fleurs/v1/sample.wav",
    "metadata": {
      "target_sample_rate": 16000,
      "steps": ["resample", "features"]
    },
    "timestamp": "2025-09-19T00:00:00Z"
  }
  ```
- Features are written to `data/processed/<dataset>/<version>/features/<relative-path>.logmel.npy` to mirror the raw directory layout.

### Dataset Profiles
- **FLEURS (full)** — Input `data/raw/fleurs/v1`, output `data/processed/fleurs/v1`; four-step chain (trim, resample, normalize, log-mel 80 bins). Use when the full corpus is staged.
- **FLEURS Smoke (<3 GiB)** — Input `data/raw/fleurs/smoke`, output `data/processed/fleurs/smoke`; mirrors full pipeline but targets the ingestion smoke slice so developers can validate end-to-end quickly. Command:
  ```bash
  PYTHONPATH=src uv run --frozen python -m preprocess.cli config/preprocess/fleurs_smoke.json --plan
  ```
  (Drop `--plan` to execute; runs emit lineage + features under `data/processed/fleurs/smoke/`.)
- **CoVoST 2 en→fr subset** — Input `data/raw/covost2/en_fr_subset`, output `data/processed/covost2/en_fr_subset`; slightly hotter normalization target (-18 dBFS) and 64-bin log-mel features for faster experiments. Plan via `config/preprocess/covost2_en_fr.json`.

All configs now include SHA-256 lineage/metadata via `src/preprocess/lineage.py`; ensure new datasets clone these profiles and adjust silence thresholds per corpus noise floor.

## Dependencies
- Legal clearance on dataset usage (MuST-C NC-ND, VoxPopuli SA).
- Storage paths from dataset manifest.
- Compute availability for feature extraction; smoke configs keep validation under ~2 GB to fit on dev laptops.
