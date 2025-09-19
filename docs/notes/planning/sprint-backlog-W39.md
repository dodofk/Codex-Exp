# Sprint Backlog – 2025-W39 (Tentative)

## Sprint Summary
- **Dates**: 2025-09-23 → 2025-10-02
- **Sprint Goal**: Stand up ingestion and preprocessing pipelines for selected datasets with reproducible download and feature generation.
- **Velocity Target**: 30 points (Director, Ingestion Engineer, Preprocess Engineer, Data Scout, Compliance Steward).

## Committed Work (Draft)
| Item | Phase | Owner | Story Points | Status | Definition of Done |
|------|-------|-------|--------------|--------|--------------------|
| Build ingestion scaffolding (`src/ingestion/`) | Phase 3 | Ingestion Engineer | 6 | In Progress | CLI + worker cover subset download, telemetry aggregated, docs PR ready |
| Finalize data-ingestion playbook + run log | Phase 3 | Ingestion Engineer | 3 | In Progress | `.env` guidance updated, run transcript archived in `.code/agents/ingestion_engineer/`, checklist marked done |
| Establish preprocessing spec & configs | Phase 3 | Preprocess Engineer | 5 | In Progress | Feature stack chosen, configs for FLEURS/CoVoST documented, lineage schema captured |
| Queue orchestration design (Redis/Prefect) | Phase 3 | Lead Architect & Ingestion Engineer | 5 | In Progress | `docs/notes/planning/phase-3-worker-architecture.md` + `scripts/prefect_flows.py` drafted; infra asks captured |
| Draft operations runbook with owners | Phase 3 | Director | 2 | In Progress | `docs/notes/phases/operations-runbook.md` published (queue health steps pending live infra) |
| Migrate dependency workflow to uv (docs + CI) | Phase 3 | Preprocess Engineer | 3 | Complete | `pyproject.toml` + `uv.lock` committed, README/ops runbook updated, CI uses `uv sync --frozen`, smoke test green via `uv run` |
| Produce sample ingestion run (FLEURS subset) | Phase 3 | Ingestion Engineer + Data Scout | 5 | In Progress | Subset artifacts downloaded, checksums validated, telemetry archived |
| Preprocessing feature extraction pipeline | Phase 3 | Preprocess Engineer | 6 | Complete | Pipeline processes full directory, log-mel features saved, tests passing (pytest + sample run) |
| Validate dataset manifest against legal guidance | Phase 2 → 3 | Compliance Steward | 3 | Complete | Manifest statuses updated, readiness report drafted |
| Update ADR-002 based on legal outcome | Phase 2 ↔ 3 | Lead Architect | 2 | In Progress | ADR accepted/rejected with notes and Phase 3 implications |

## Prep Tasks Before Sprint Start
- Confirm compliance notices reflected in manifest, readiness report, and README.
- Finalize dataset shortlist scores using `docs/notes/datasets/shortlist-rubric.md` and select top set.
- Confirm compute/storage availability for ingestion workloads.
- Reserve Redis/Prefect infrastructure (or approved alternative) and document access steps.
- Align preprocessing compute budget (CPU vs. GPU) for feature extraction.

## Blockers to Monitor
- MuST-C/VoxPopuli legal constraints (meeting 2025-09-20).
- Storage allocation for large corpora (>1 TB).
- Pending access tokens (e.g., TED downloads) if required.
- Redis/Prefect provisioning delays impacting queue automation.
