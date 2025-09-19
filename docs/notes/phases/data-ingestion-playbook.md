# Data Ingestion Playbook (Phase 3 Draft)

## Objectives
- Provide reproducible download scripts and verification steps for approved datasets (FLEURS, CoVoST 2, MuST-C v2, VoxPopuli, WikiMatrix).
- Standardize directory structure and metadata logging for `data/raw`, `data/interim`, and `data/processed`.

## Checklist
- [x] Configure Make targets (`make data-plan`, `make data-download`, `make data-verify`).
- [x] Add retry, checksum validation, and HTTP range resume in `src/ingestion/tasks.execute`.
- [x] Document required credentials and `.env` entries.
- [x] Capture telemetry (timestamp, dataset, status, bytes, duration) in JSONL logs.
- [x] Archive run instructions in `.code/agents/ingestion_engineer/`.

## Current Scaffolding
- CLI entry-point: `python -m ingestion.cli <config> --plan`
- Worker entry-point: `python -m ingestion.worker --payload <payload.json> [--run]`
- HF loader entry-point: `python -m ingestion.hf_loader --dataset ... --output ...`
- Make helpers: `make data-plan DATASET=<dataset>`, `make data-download DATASET=<dataset>`, `make worker-run DATASET=<dataset> ARGS="--artifact ..."`, `make hf-download HF_ARGS="..."`
- Config loader: `src/ingestion/config.py` (JSON/YAML with artifact specs)
- Example configs: `config/ingestion/fleurs.json`, `covost2.json`, `mustc.json`, `voxpopuli.json`, `wikimatrix.json`
- Unit tests: `tests/ingestion/test_cli.py`
- Telemetry: JSONL appended to `data/raw/<dataset>/logs/events.jsonl`
- Environment file: `.env.ingestion` (see `.env.ingestion.example`) loaded automatically by the CLI for credentials/headers.
- Sample run transcript: `.code/agents/ingestion_engineer/2025-09-19-fleurs-dev-run.md`.
- Optional OpenTelemetry exporter: set `OTEL_EXPORTER_CONSOLE=1` to mirror events to stdout for scraping.
- Compliance gate: configs provide `"distribution": "public|internal|restricted"`. Worker refuses to run non-public datasets unless metadata is updated per compliance policy.

## Credentials & Environment
- **MuST-C v2 (`MUSTC_TOKEN`)** — Required FBK bearer token for protected tarballs.
- **VoxPopuli (`VOXPOPULI_COOKIE`)** — Raw cookie header string for authenticated mirrors.
- **YouTube-derived datasets (`YOUTUBE_API_KEY`)** — Prevents rate throttling when pulling captions/audio.
- **Hugging Face private repos (`HUGGINGFACE_TOKEN`)** — Optional personal access token.
- **Telemetry debugging (`OTEL_EXPORTER_CONSOLE`)** — Set to `1` to mirror events to stdout during troubleshooting.

Copy `.env.ingestion.example` to `.env.ingestion` and fill in only the variables
your run requires. Never commit real secrets; share rotation guidance in the
operations runbook once published.

Example run with headers:
```bash
# .env.ingestion contains MUSTC_TOKEN=...
make data-download DATASET=mustc
```
The config `config/ingestion/mustc.json` injects `Authorization: Bearer ${MUSTC_TOKEN}`
into the HTTP request.

## Open Questions
- Preferred tooling (Python CLI vs. bash) for large dataset downloads.
- Storage quota and retention policy per dataset.
- Handling of restricted datasets if legal imposes constraints (MuST-C, VoxPopuli).
- Document MFA/secret rotation flows for `.env.queue` and `.env.ingestion`.
