# Preprocessing Specification (Phase 3 Draft)

## Scope
- Define normalization, tokenization, and feature extraction steps for speech/text corpora selected in Phase 2.
- Ensure outputs align with ADR-001 baseline (PaLM-compatible tokens, discrete audio tokens) and ADR-002 fallback if invoked.

## Pipeline Components
- Audio preprocessing: sample rate normalization (16 kHz), silence trimming, feature extraction (e.g., log-mel or k-means tokens).
- Text preprocessing: language-specific normalization, sentencepiece tokenization, punctuation handling (per dataset).
- Metadata tracking: input checksum, transformation parameters, output hashes, lineage logs.

### Current Scaffolding
- Config loader: `src/preprocess/config.py`
- Pipeline wrapper: `src/preprocess/pipeline.py`
- Example config: `config/preprocess/fleurs.json`
- Tests: `tests/preprocess/test_pipeline.py`

## Action Items
- [ ] Draft configuration templates (e.g., `config/preprocess/fleurs.yaml`).
- [ ] Identify reusable libraries/tooling (torchaudio, librosa, sentencepiece).
- [ ] Define logging format for lineage (JSONL or CSV).
- [x] Collaborate with Ingestion Engineer on file naming conventions (reuse `data/raw/<dataset>/<version>` paths from ingestion manifest).
- [ ] Prepare unit tests coverage plan for edge cases.

## Dependencies
- Legal clearance on dataset usage (MuST-C NC-ND, VoxPopuli SA).
- Storage paths from dataset manifest.
- Compute availability for feature extraction.
