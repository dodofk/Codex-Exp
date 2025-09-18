# Sprint Backlog – 2025-W39 (Tentative)

## Sprint Summary
- **Dates**: 2025-09-23 → 2025-10-02
- **Sprint Goal**: Stand up ingestion and preprocessing pipelines for selected datasets with reproducible download and feature generation.
- **Velocity Target**: 30 points (Director, Ingestion Engineer, Preprocess Engineer, Data Scout, Compliance Steward).

## Committed Work (Draft)
| Item | Phase | Owner | Story Points | Status | Definition of Done |
|------|-------|-------|--------------|--------|--------------------|
| Build ingestion scaffolding (`src/ingestion/`) | Phase 3 | Ingestion Engineer | 6 | Draft | CLI entry + config file, dry-run on sample |
| Draft data-ingestion playbook | Phase 3 | Ingestion Engineer | 2 | Draft | `docs/notes/phases/data-ingestion-playbook.md` populated |
| Establish preprocessing spec | Phase 3 | Preprocess Engineer | 4 | Draft | `docs/notes/phases/preprocess-spec.md` with configs + logging plan |
| Validate dataset manifest against legal guidance | Phase 2 → 3 | Compliance Steward | 3 | Draft | Manifest statuses updated, readiness report drafted |
| Produce sample ingestion run (FLEURS subset) | Phase 3 | Ingestion Engineer + Data Scout | 5 | Draft | Sample downloaded, checksums verified |
| Update ADR-002 based on legal outcome | Phase 2 ↔ 3 | Lead Architect | 2 | Draft | ADR accepted/rejected with notes |

## Prep Tasks Before Sprint Start
- Confirm compliance notices reflected in manifest, readiness report, and README.
- Finalize dataset shortlist scores using `docs/notes/datasets/shortlist-rubric.md` and select top set.
- Confirm compute/storage availability for ingestion workloads.

## Blockers to Monitor
- MuST-C/VoxPopuli legal constraints (meeting 2025-09-20).
- Storage allocation for large corpora (>1 TB).
- Pending access tokens (e.g., TED downloads) if required.
