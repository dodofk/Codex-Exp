# Auto-Paper Phase 3 Scaffolding

This repository reproduces and extends “Transforming LLMs into Cross-modal and
Cross-lingual Retrieval Systems”. Phase 3 introduces ingestion and preprocessing
layers for the approved dataset shortlist (FLEURS, CoVoST 2, MuST-C, VoxPopuli).

## Quickstart

1. **Inspect an ingestion plan**
   ```bash
   make data-plan DATASET=fleurs
   ```
   Plans read configs under `config/ingestion/*.json`. Sample configs download
   README files so you can verify the workflow without large transfers.

2. **Download & verify artifacts**
   ```bash
   make data-download DATASET=covost2
   ```
   Artifacts are saved to `data/raw/<dataset>/<version>/`. Checksums (if
   provided) are validated automatically.

   Sensitive datasets (e.g., MuST-C, VoxPopuli mirrors) may need credentials.
   Copy `.env.ingestion.example` to `.env.ingestion` and populate keys such as
   `MUSTC_TOKEN`, `VOXPOPULI_COOKIE`, or `YOUTUBE_API_KEY`. Never commit real
   secrets—the CLI will read these values when secured endpoints are wired in.

   Example (MuST-C docs):
   ```bash
   export MUSTC_TOKEN=... # or set in .env.ingestion
   make data-download DATASET=mustc
   ```
   The request header `Authorization: Bearer ${MUSTC_TOKEN}` is populated from
   the environment at runtime.

3. **Preprocessing scaffold**
   ```python
   from preprocess.pipeline import build_pipeline
   pipeline = build_pipeline("config/preprocess/fleurs.json")
   print("\n".join(pipeline.plan()))
   ```
   Execution currently raises `NotImplementedError`; the scaffold documents
   the intended steps before we wire real transformations.

## Compliance & Attribution
- **FLEURS** — © Google. Licensed CC BY 4.0. Quote attribution (“© Google LLC,
  used under CC BY 4.0”) wherever the dataset or derived results appear.
- **CoVoST 2** — CC0. Reference Mozilla Common Voice volunteer statement and
  scrub incidental PII from metadata.
- **MuST-C** — CC BY-NC-ND 4.0. Internal research only; do not redistribute
  trained models or filtered datasets without FBK approval. Include NC-ND notices
  in release notes.
- **VoxPopuli / WikiMatrix** — CC BY-SA. Any external artefact must inherit the
  same share-alike license; otherwise keep artefacts internal.
- **How2, AudioCaps** — CC BY + YouTube Terms. Download captions/audio features
  only, respect takedown requests, and avoid sharing raw video/audio.

Quick reference for wording lives in the dataset manifest (`docs/notes/datasets/dataset-manifest.md`).
See `docs/notes/compliance/compliance-readiness-report.md` for the full legal
summary and mitigation steps.

## Testing
Run the automated tests with:
```bash
pytest
```
Tests exercise the ingestion CLI, checksum validation, and preprocessing
pipeline planning.

## Repo Layout Highlights
- `config/ingestion/` — JSON configs backing each dataset.
- `config/preprocess/` — Preprocessing configuration prototypes.
- `src/ingestion/` — Config loader, download tasks, CLI entry point.
- `src/preprocess/` — Config + pipeline scaffolding for Phase 3.
- `docs/notes/` — Project documentation (roadmap, compliance, playbooks).

## Next Steps
- Populate ingestion configs with full artifact manifests and credentials.
- Implement real preprocessing transforms (audio normalization, feature
  extraction) and log lineage as described in `docs/notes/phases/preprocess-spec.md`.
- Capture minutes from the Phase 3 kickoff (2025-09-23) under `docs/notes/planning/`.
