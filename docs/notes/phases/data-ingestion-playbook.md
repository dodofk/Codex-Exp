# Data Ingestion Playbook (Phase 3 Draft)

## Objectives
- Provide reproducible download scripts and verification steps for approved datasets (FLEURS, CoVoST 2, MuST-C v2, VoxPopuli, WikiMatrix).
- Standardize directory structure and metadata logging for `data/raw`, `data/interim`, and `data/processed`.

## Checklist
- [x] Configure Make targets (`make data-plan`, `make data-download`, `make data-verify`).
- [x] Add retry, checksum validation, and HTTP range resume in `src/ingestion/tasks.execute`.
- [ ] Document required credentials and `.env` entries.
- [x] Capture telemetry (timestamp, dataset, status, bytes, duration) in JSONL logs.
- [ ] Archive run instructions in `.code/agents/ingestion_engineer/`.

## Current Scaffolding
- CLI entry-point: `python -m ingestion.cli <config> --plan`
- Make helpers: `make data-plan DATASET=<dataset>`, `make data-download DATASET=<dataset>`
- Config loader: `src/ingestion/config.py` (JSON/YAML with artifact specs)
- Example configs: `config/ingestion/fleurs.json`, `covost2.json`, `mustc.json`, `voxpopuli.json`, `wikimatrix.json`
- Unit tests: `tests/ingestion/test_cli.py`
- Telemetry: JSONL appended to `data/raw/<dataset>/logs/events.jsonl`
- Environment file: `.env.ingestion` (see `.env.ingestion.example`) loaded automatically by the CLI for credentials/headers.

## Credentials & Environment
- **MuST-C v2**: requires FBK account; store credential token as `MUSTC_TOKEN` in `.env.ingestion` (not committed). CLI will be extended to use this token when downloading archives.
- **VoxPopuli**: use public mirrors; if internal mirrors require SSO, capture cookies in `VOXPOPULI_COOKIE` env.
- **How2 / YouTube-derived datasets**: no direct credentials, but make sure `YOUTUBE_API_KEY` is available if rate limits require API-based downloads.
- Create `.env.ingestion.example` documenting these variables for contributors; real values belong in developer-local `.env.ingestion` referenced by future download scripts.

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
