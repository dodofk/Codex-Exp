# Auto-Paper Phase 3 Scaffolding

This repository reproduces and extends “Transforming LLMs into Cross-modal and
Cross-lingual Retrieval Systems”. Phase 3 introduces ingestion and preprocessing
layers for the approved dataset shortlist (FLEURS, CoVoST 2, MuST-C, VoxPopuli).

## Environment Setup (uv)

1. Install the project dependencies with uv (creates/updates `.venv` automatically):
   ```bash
   uv sync
   ```
   The sync installs both runtime and dev dependencies defined in `pyproject.toml`/`uv.lock`.
2. Run commands through uv so the managed environment is used, e.g.:
   ```bash
   uv run pytest
   uv run make data-plan DATASET=fleurs
   ```
   Use `uv run --with <package>` for one-off extras when experimenting.
3. For Phase 4 model experiments install the optional CPU extras:
   ```bash
   uv sync --extra model-cpu
   ```
   This pulls Torch CPU wheels, transformers/PEFT, and SacreBLEU for evaluation.

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
   Copy `.env.ingestion.example` to `.env.ingestion` and populate the variables
   you need:

   - `MUSTC_TOKEN` — FBK-issued bearer token for MuST-C archives.
   - `VOXPOPULI_COOKIE` — cookie header string for authenticated VoxPopuli mirrors.
   - `YOUTUBE_API_KEY` — used to avoid rate limits on YouTube-derived datasets.
   - `HUGGINGFACE_TOKEN` — optional personal access token for private datasets.
   - `OTEL_EXPORTER_CONSOLE` — set to `1` to mirror telemetry to stdout while debugging.

   Never commit real secrets—the CLI will read these values when secured endpoints
   are wired in. See `examples/ingestion/` for ready-to-run commands and helper
   scripts.

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
   pipeline.execute()  # writes processed audio to data/processed/fleurs/v1
   ```
   Or via Make helpers:
   ```bash
   make preprocess-plan DATASET=fleurs
   make preprocess-run DATASET=fleurs
   ```
   The pipeline resamples to 16 kHz, normalizes loudness, and writes log-mel features + lineage metadata.

### Queue Worker Demo

Automated runs can use the queue-style package entry point:

```bash
# Plan only
PYTHONPATH=src python -m ingestion.worker --payload-json '{"dataset":"fleurs"}' --plan

# Execute (downloads to data/raw/fleurs/docs)
PYTHONPATH=src python -m ingestion.worker --payload-json '{"dataset":"fleurs"}' --run

# Using Make helper with artifact filter
make worker-run DATASET=covost2 ARGS="--artifact README.md"

# Prefect deployment (optional PoC)
scripts/dev_infra.sh  # starts Redis + Prefect locally (Docker + uv)
make queue-prefect-deploy
uv run prefect worker start --pool ingestion  # in separate terminal
make queue-prefect-run DATASET=fleurs CONFIG=config/ingestion/fleurs_dev.json
# (combined flow triggers ingestion followed by preprocess)
```

### Hugging Face Subset Download

Use the integrated Hugging Face loader to pull curated slices without manual steps:

```bash
# download 1% of the English→French CoVoST 2 split
make hf-download HF_ARGS="--dataset facebook/covost2 --config en_fr --split train[:1%] --output data/raw/covost2/en_fr_subset"

# or call the module directly
PYTHONPATH=src python -m ingestion.hf_loader \
  --dataset facebook/covost2 --config en_fr --split train[:1000] \
  --output data/raw/covost2/en_fr_subset --limit 1000
```

### Telemetry
- Ingestion, Hugging Face loader, and worker flows append events to
  `data/raw/<dataset>/logs/events.jsonl` and `telemetry.jsonl`.
- Set `OTEL_EXPORTER_CONSOLE=1` to mirror telemetry to stdout for scraping or
  OpenTelemetry testing.
- Summarize ingestion activity with `python scripts/telemetry_aggregate.py data/raw/<dataset>/logs`
  to view counts plus total bytes and durations per event type.
- Summarize model runs with `make telemetry-model-summary`, which scans
  `data/logs/model/` and writes `data/telemetry/model_summary.json` (aggregated
  recall/MRR/BLEU metrics).

### Operations
- Daily and incident procedures live in `docs/notes/phases/operations-runbook.md`.
- Sample ingestion transcript: `.code/agents/ingestion_engineer/2025-09-19-fleurs-dev-run.md`.
- Queue design & Prefect/Redis plan: `docs/notes/planning/phase-3-worker-architecture.md`.
- Prefect deployment checklist (blocks, agents, test run) documented inside the architecture note.

## Compliance & Attribution
- **FLEURS** — © Google LLC, licensed CC BY 4.0. Quote the attribution string
  (“© Google LLC, used under CC BY 4.0”) wherever data or derivatives appear.
- **CoVoST 2** — CC0. Reference the Mozilla Common Voice volunteer statement and
  scrub incidental PII from metadata before storage.
- **Multilingual LibriSpeech** — Public Domain. Attribute narrators/speakers and
  retain the public-domain notice in downstream artifacts.
- **MuST-C v2** — CC BY-NC-ND 4.0. Internal research only; do not redistribute
  trained models or filtered datasets externally without FBK consent. Include
  NC-ND warnings in any release notes.
- **VoxPopuli** — CC BY-SA 4.0. Any external artifact must inherit CC BY-SA 4.0;
  otherwise keep the outputs internal. Document share-alike obligations in
  manifests and reports.
- **WikiMatrix** — CC BY-SA 3.0. Same share-alike requirement as VoxPopuli;
  ensure attribution to Wikimedia contributors.
- **How2 / How2QA** — CC BY 4.0 + YouTube Terms. Download captions/audio
  features only, respect takedown requests, and avoid storing raw video/audio.
- **AudioCaps** — CC BY 4.0. Attribute KU Leuven and annotators; monitor YouTube
  removals to purge invalid clips.
- **Clotho v2** — CC BY 4.0. Attribute Tampere University and crowdworkers; keep
  consent statements with distributed subsets.

The ingestion worker enforces per-dataset policies via the `distribution` field
in `config/ingestion/*.json` (e.g., `internal`, `restricted`, `public`). Jobs are
blocked when distribution is not permitted. Reference
`docs/notes/compliance/compliance-readiness-report.md` for complete guidance.

Quick reference for wording lives in the dataset manifest (`docs/notes/datasets/dataset-manifest.md`).
See `docs/notes/compliance/compliance-readiness-report.md` for the full legal
summary and mitigation steps.

## Model Training (Phase 4 Preview)

The Phase 4 retrieval scaffold lives under `src/model/` and can be exercised on
macOS/CPU. After installing the `model-cpu` extras:

```bash
uv sync --extra model-cpu
```

You can launch a smoke training run with:

```bash
make model-train MODEL_CONFIG=config/model/baseline.yaml
```

and run evaluation-only passes with:

```bash
make model-eval MODEL_CONFIG=config/model/baseline.yaml
```

Both targets stream metrics to `data/logs/model/<run-id>/metrics.jsonl` and
mirror summary events into `data/logs/model/<run-id>/telemetry.jsonl`. Override
CLI options via `MODEL_ARGS="--dataset-root data/processed/fleurs/smoke"` to
experiment with alternate manifests or logging directories.

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
- `scripts/model_telemetry_summary.py` — Aggregates `data/logs/model/` runs into
  `data/telemetry/model_summary.json`.

## Next Steps
- Populate ingestion configs with full artifact manifests and credentials.
- Implement real preprocessing transforms (audio normalization, feature
  extraction) and log lineage as described in `docs/notes/phases/preprocess-spec.md`.
- Capture minutes from the Phase 3 kickoff (2025-09-23) under `docs/notes/planning/`.
