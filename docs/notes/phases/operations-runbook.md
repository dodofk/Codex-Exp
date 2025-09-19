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
