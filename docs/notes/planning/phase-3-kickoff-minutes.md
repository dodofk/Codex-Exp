# Phase 3 Kickoff Minutes – 2025-09-23 09:00 PT

## Attendees
- Director (chair)
- Ingestion Engineer
- Preprocess Engineer
- Compliance Steward
- Lead Architect / Infra SRE liaison

## Highlights
- Phase 2 exit criteria formally accepted; shortlist (FLEURS, CoVoST 2, MuST-C, VoxPopuli) confirmed.
- Ingestion automation demoed (Make targets, telemetry aggregator, `.env` guidance).
- Preprocessing roadmap shared: audio pipeline ready (log-mel + lineage), text normalization still TBD.
- Queue orchestration draft (`phase-3-worker-architecture.md`) reviewed; need Redis provisioning ticket + Prefect deployment target dates.
- Operations runbook skeleton acknowledged; queue health steps to be filled post-infra setup.

## Decisions
1. **Primary dataset**: FLEURS dev subset continues as reference run; CoVoST 2 plan due next sprint.
2. **Pipeline exit criteria**: Phase 3 considered “ready” once ingest→preprocess hand-off runs under Prefect with telemetry captured end-to-end.
3. **Redis**: Request lightweight Redis instance from infra by 2025-09-24; fallback is local Docker during PoC.
4. **Text normalization**: Preprocess Engineer to deliver proposal (SentencePiece + language-specific normalization) by 2025-09-26.
5. **Compliance notices**: Ingestion Engineer and Compliance Steward to ensure manifest/README reflect licensing guidance before readiness review.

## Action Items
| Owner | Action | Due Date | Status |
|-------|--------|----------|--------|
| Ingestion Engineer | Run full ingest→preprocess flow via Prefect PoC and capture telemetry snapshot | 2025-09-27 | Open |
| Preprocess Engineer | Draft text normalization/tokenization plan + tests | 2025-09-26 | Open |
| Lead Architect | File Redis provisioning ticket & document connection info | 2025-09-24 | Open |
| Director | Update operations runbook with queue health checks post-Redis | 2025-09-28 | Open |
| Compliance Steward | Confirm license notices in `config/ingestion/*.json` and README | 2025-09-25 | Open |

## References
- `docs/notes/planning/program-roadmap.md`
- `docs/notes/planning/sprint-backlog-W39.md`
- `docs/notes/planning/phase-3-worker-architecture.md`
- `.code/agents/ingestion_engineer/2025-09-19-fleurs-dev-run.md`
