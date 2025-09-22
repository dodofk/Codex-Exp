# Phase 3 Operations Runbook

## Purpose
Provide on-call guidance for ingestion and preprocessing jobs during Phase 3. Updated 2025-09-19.

## Ownership
- **Primary On-Call**: Ingestion Engineer (weekday coverage)
- **Secondary**: Preprocess Engineer (pipelines/features)
- **Tertiary/Infra**: Lead Architect (queue infra, Redis/Prefect)
- **Compliance Escalation**: Compliance Steward (license issues)

## Daily Checklist
1. Review overnight telemetry: `python scripts/telemetry_aggregate.py data/raw/<dataset>/logs`.
2. Spot-check lineage entries in `data/processed/<dataset>/<version>/lineage.jsonl` for recent preprocess runs.
3. Prefect/Redis health: `prefect deployment ls --name auto-paper-ingestion` (ensure last run <24h) and `redis-cli -h <host> llen ingestion` (<5 pending jobs).
4. Verify credentials in `.env.ingestion` have not expired (check rotation dates below).
5. Ensure local environment synced via `uv sync --frozen` before running Make/CLI commands; prefer `uv run …` wrappers for all Python entry points.

## Prefect & Redis Provisioning Checklist
1. Ensure Docker Desktop (or equivalent) is running; Redis spins up as a container (`auto-paper-redis`).
2. Export `PREFECT_API_URL=http://127.0.0.1:4200/api` (or target control-plane URL) for all following commands.
3. Start local infra via `./scripts/dev_infra.sh`—this launches Redis and a Prefect server with logs at `/tmp/prefect-server.log`.
4. Deploy flows with `make queue-prefect-deploy`; this creates the `ingestion` work pool and registers `auto-paper-ingest-preprocess/prod` against `scripts/prefect_flows.py`.
5. Start a worker in a new terminal: `uv run prefect worker start --pool ingestion` (Ctrl+C when shutting down).
6. Kick off a smoke run: `uv run prefect deployment run auto-paper-ingest-preprocess/prod --params '{"dataset":"fleurs","config_path":"config/ingestion/fleurs_smoke.json","preprocess_config":"config/preprocess/fleurs.json"}'` to stay under ~3 GiB. Switch the `config_path` to the full `fleurs_dev.json` (or similar) once storage and bandwidth are cleared.
7. Cancel the run after verifying telemetry wiring if you only need a connectivity check (`uv run prefect flow-run cancel <run-id>`).
8. Tear down when finished: `pkill -f "prefect worker start --pool ingestion"`, `pkill -f "prefect server start"`, and `docker stop auto-paper-redis`.

> Note: Prefect/Redis CLIs are provided through the project environment (`uv sync` installs `prefect` and `redis` from `pyproject.toml`). Update `docs/notes/planning/sprint-backlog.md` if provisioning exposes new blockers (e.g., cloud endpoint access, quota issues).

## Phase 4 Ops Appendix – Model Training
- **Resource Planning**: Default to macOS CPU. Limit `model-train` jobs to ≤16 threads (`export OMP_NUM_THREADS=16`). For overnight runs, coordinate with Ops for remote executor scheduling.
- **Environment Setup**: Install optional extras via `uv pip install .[model-cpu]` after proposal approval. Confirm `torch` and `torchaudio` CPU wheels.
- **Telemetry**: Training CLI emits metrics to `data/logs/model/<run-id>/metrics.jsonl` (defaults to timestamp-based `run-id`). Per-epoch and eval events mirror to `telemetry.jsonl`. Summaries live under `data/telemetry/model_summary.json`; refresh with `make telemetry-model-summary` (wrapper around `scripts/model_telemetry_summary.py`).
- **Log Retention**: Store training logs under `data/logs/model/<run-id>/`. Retain at least two sprint cycles for regression comparison.
- **Incident Response**: Failures in `model-train` smoke jobs must be recorded in sprint backlog daily updates; escalate to MLOps if CPU thrash observed.

## Incident Playbooks
- **Download failure / checksum mismatch**
  1. Inspect `data/raw/<dataset>/logs/events.jsonl` for error event.
  2. Reproduce with `PYTHONPATH=src python scripts/enqueue_ingestion.py <dataset> --plan` (safe mode).
  3. Retry with `--run` after addressing connectivity or credentials.
  4. Escalate to infra if repeated `artifact_download_retry` exceeds 5 attempts.
- **Queue backlog / worker crash (post-orchestration)**
  1. Check Prefect dashboard (deployment `auto-paper-ingest-preprocess/prod`) and Redis queue length.
  2. Restart worker (`uv run prefect worker start --pool ingestion`) or associated container.
  3. File incident note in this runbook + sprint backlog.
- **Credential expiry**
  1. Rotate token (see cadence table).
  2. Update `.env.ingestion` and share with relevant engineer securely.

## Credential Rotation Cadence
| Variable | Owner | Rotation Frequency | Notes |
|----------|-------|--------------------|-------|
| MUSTC_TOKEN | Ingestion Engineer | 90 days | FBK portal reset reminder set for 2025-12-18 |
| VOXPOPULI_COOKIE | Compliance Steward | 30 days | Renew after mirror cookie invalidation |
| YOUTUBE_API_KEY | Research | 180 days | Monitor quota usage weekly |
| HUGGINGFACE_TOKEN | Individual devs | Upon offboarding | Personal PAT, rotate when running automation |

## Communication
- Slack channel: #auto-paper-ingestion (create before 2025-09-23 kickoff).
- Incident reports: add bullets to this runbook and create backlog ticket referencing root cause.
- Weekly summary: Director compiles highlights + incidents for sponsor update.

## Upcoming Enhancements
- Integrate Redis/Prefect metrics endpoint once architecture doc finalises.
- Add W&B / logging pipeline decision (pending Phase 5 planning).
- Expand runbook with screenshot walkthroughs after first full pipeline execution.
- Replace local Docker/Python instructions with managed infra once Redis/Prefect tickets close.
- Document uv cache management + upgrade cadence after first CI run completes with new workflow (target 2025-09-24).
