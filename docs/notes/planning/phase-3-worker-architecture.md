# Phase 3 Worker & Queue Architecture (Draft)

## Objectives
- Automate ingestion and preprocessing jobs using a queue-based orchestrator.
- Provide retry-safe execution with clear credential handling and telemetry.
- Ensure local development parity via helper scripts before infra rollout.

## Components
- **Queue**: Redis (hosted or managed) storing job payloads.
- **Orchestrator**: Prefect 2.0 (initial) managing DAGs and retries. Alternative: Celery/rq if Prefect unsuitable.
- **Workers**:
  - `ingestion-worker`: wraps `python -m ingestion.worker --payload-json …`.
  - `preprocess-worker`: wraps `python -m preprocess.worker --payload-json …`.
- **Scheduler**: Prefect deployments triggered nightly + manual kickoffs.
- **Telemetry Sink**: JSONL → `scripts/telemetry_aggregate.py`; long term: export to Prometheus/W&B.
- **Secrets**: `.env.ingestion` locally; production via Prefect blocks or Hashicorp Vault.

## Payload Schema
```json
{
  "dataset": "fleurs",
  "config_path": "config/ingestion/fleurs_dev.json",
  "artifacts": ["README.md"],
  "metadata": {
    "priority": "standard",
    "requested_by": "auto-paper"
  }
}
```

- Ingestion jobs validate `distribution` before download.
- Preprocessing jobs (future) will reference processed output path and feature params.

## Local Development Flow
1. Developer crafts payload JSON or uses helper: `PYTHONPATH=src python scripts/enqueue_ingestion.py fleurs --config config/ingestion/fleurs_dev.json --priority high --metadata requested_by=auto-paper`.
2. `scripts/enqueue_ingestion.py` forwards to `ingestion.worker` in-process; telemetry and logs stored under `data/raw/<dataset>/logs`.
3. Prefect PoC wraps the helper via `scripts/prefect_flows.py:ingest_preprocess_flow`, enabling local Prefect runs before Redis wiring.

## Prefect PoC Plan (Sept 2025)
1. Create Prefect deployment `auto-paper-ingest-preprocess/prod` using `scripts/prefect_flows.py:ingest_preprocess_flow` (`make queue-prefect-deploy`).
2. Configure Redis block for queue persistence; evaluate worker concurrency vs. dataset size (`uv run prefect blocks create redis/auto-paper --host 127.0.0.1 --port 6379`).
3. Implement Prefect hook for preprocess hand-off: ingestion task immediately invokes the preprocess task inside the same flow (current implementation).
4. Capture metrics (success/failure counts, retries) and feed to `scripts/telemetry_aggregate.py` nightly.

### Latest Validation (2025-09-21)
- Verified on local stack (`./scripts/dev_infra.sh` + Docker Redis) with worker type `process`.
- Flow run `hallowed-gecko` (`9ead8c5e-3cc2-4af1-961d-2d73d9db8125`) processed the `fleurs_smoke` (<3 GiB) ingestion + preprocess chain end-to-end; telemetry + lineage logs captured under `data/raw/fleurs/logs/` and `data/processed/fleurs/smoke/`.
- Run surfaced checksum drift for `am_et/audio/dev.tar.gz`; hashes now fixed in `config/ingestion/fleurs_smoke.json`, enabling subsequent runs to skip previously downloaded artifacts cleanly.
- Prefect logs confirm sequential execution order: ingestion task finishes, preprocess task runs immediately, then flow exits `Completed`.
- Use this run ID as readiness evidence for queue orchestration milestone in the roadmap (2025-09-30).

### Deployment Steps (Draft)
1. `prefect block register -m prefect.blocks.system` (once per workspace).
2. `prefect config set PREFECT_API_URL="https://prefect.your-org/api"` (or leave default for Prefect Cloud).
3. `prefect block create 'redis/auto-paper-queue' --host <redis-host> --port 6379 --password ****`.
4. `make queue-prefect-deploy` (deploys flow as `auto-paper-ingest-preprocess/prod`).
5. `uv run prefect worker start --pool ingestion` (runs locally until containerised).
6. `make queue-prefect-run DATASET=fleurs CONFIG=config/ingestion/fleurs_dev.json` to validate ingestion + preprocess hand-off.

### Provisioning Redis & Prefect (Temporary Guide)
1. Run `scripts/dev_infra.sh` (start Redis container + Prefect server via uv).
2. Ensure `PREFECT_API_URL` exported (script prints endpoint) and work pool created via `make queue-prefect-deploy`.
3. Start worker in a separate terminal: `PREFECT_API_URL=http://127.0.0.1:4200/api uv run prefect worker start --pool ingestion`.
4. Execute smoke run: `PREFECT_API_URL=http://127.0.0.1:4200/api uv run prefect deployment run auto-paper-ingest-preprocess/prod --params '{"dataset":"fleurs","config_path":"config/ingestion/fleurs_smoke.json","preprocess_config":"config/preprocess/fleurs_smoke.json"}'`.
5. Tear down with `pkill -f "prefect worker start --pool ingestion"`, `pkill -f "prefect server start"`, and `docker stop auto-paper-redis` to avoid orphaned processes.

## Retry & Backoff
- Default retries: 3 (exponential backoff 2s → 8s).
- Hard failures raise Prefect incident, notify #auto-paper-ingestion (Slack) and log runbook entry.

## Dependencies & TODOs
- Provision Redis instance or select managed service (infra ticket).
- Document Prefect deployment steps (README section under Operations, due with readiness review).
- Integrate queue health checks into operations runbook (add once Prefect deployment live).
- Extend flow to trigger preprocess worker after ingestion pipeline merges. ✅
- Harden checksum manifest ingestion for other datasets (CoVoST, MuST-C) and capture corresponding smoke run IDs once completed.

## References
- `.code/agents/ingestion_engineer/2025-09-19-fleurs-dev-run.md`
- `scripts/enqueue_ingestion.py`
- `scripts/prefect_flows.py`
- `docs/notes/phases/operations-runbook.md`
- `docs/notes/planning/program-roadmap.md`
