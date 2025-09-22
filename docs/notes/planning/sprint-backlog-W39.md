# Sprint Backlog – 2025-W39 (Tentative)

## Sprint Summary
- **Dates**: 2025-09-23 → 2025-10-02
- **Sprint Goal**: Stand up ingestion and preprocessing pipelines for selected datasets with reproducible download and feature generation.
- **Velocity Target**: 30 points (Director, Ingestion Engineer, Preprocess Engineer, Data Scout, Compliance Steward).

## Committed Work (Draft)
| Item | Phase | Owner | Story Points | Status | Definition of Done |
|------|-------|-------|--------------|--------|--------------------|
| Build ingestion scaffolding (`src/ingestion/`) | Phase 3 | Ingestion Engineer | 6 | Complete | CLI + worker exercised via `fleurs_smoke` profile, telemetry logged, unit tests & docs updates merged |
| Finalize data-ingestion playbook + run log | Phase 3 | Ingestion Engineer | 3 | Complete | Playbook documents `fleurs_smoke` flow, new transcript added (2025-09-21), `.env` guidance and checklist confirmed |
| Establish preprocessing spec & configs | Phase 3 | Preprocess Engineer | 5 | Complete | Preprocess spec updated with dataset profiles; configs `fleurs_smoke` + `covost2_en_fr` landed; lineage + plan commands captured |
| Queue orchestration design (Redis/Prefect) | Phase 3 | Lead Architect & Ingestion Engineer | 5 | Complete | Architecture doc updated with `hallowed-gecko` validation, smoke-run command, teardown steps (`phase-3-worker-architecture.md`) |
| Draft operations runbook with owners | Phase 3 | Director | 2 | Complete | Runbook now includes Prefect/Redis provisioning checklist, queue health cadence, and ownership matrix (`operations-runbook.md`) |
| Migrate dependency workflow to uv (docs + CI) | Phase 3 | Preprocess Engineer | 3 | Complete | `pyproject.toml` + `uv.lock` committed, README/ops runbook updated, CI uses `uv sync --frozen`, smoke test green via `uv run` |
| Produce sample ingestion run (FLEURS subset) | Phase 3 | Ingestion Engineer + Data Scout | 5 | Complete | Prefect run `hallowed-gecko` (9ead8c5e-3cc2-4af1-961d-2d73d9db8125) captured telemetry, checksum-verified smoke slice archived with transcript |
| Preprocessing feature extraction pipeline | Phase 3 | Preprocess Engineer | 6 | Complete | Pipeline processes full directory, log-mel features saved, tests passing (pytest + sample run) |
| Validate dataset manifest against legal guidance | Phase 2 → 3 | Compliance Steward | 3 | Complete | Manifest statuses updated, readiness report drafted |
| Update ADR-002 based on legal outcome | Phase 2 ↔ 3 | Lead Architect | 2 | Complete | ADR-002 updated 2025-09-21 with legal meeting notes; roadmap references fallback triggers |

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
