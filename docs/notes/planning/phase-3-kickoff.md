# Phase 3 Kickoff Agenda – Data Ingestion & Preprocessing

- **Meeting Date**: 2025-09-23 09:00 PT
- **Participants**: Director, Ingestion Engineer, Preprocess Engineer, Data Scout, Compliance Steward, Lead Architect
- **Prerequisites**:
  - Legal decisions recorded in `docs/notes/compliance/compliance-risk-log.md`
  - Dataset shortlist approved and manifest statuses updated
  - ADR-002 finalized (if needed)

## Agenda
1. **Recap Phase 2 Outcomes**
   - Final dataset selections + compliance notes
   - Review dataset manifest & storage plan
2. **Ingestion Plan**
   - Directory structure (`data/raw`, `data/interim`, `data/processed`)
   - Required Make targets (`make data-download`, `make data-verify`)
   - Secrets / credential handling
3. **Preprocessing Strategy**
   - Feature extraction requirements (audio tokens, text normalization)
   - Config templates & logging expectations
4. **Milestones & Deliverables**
   - Define sprint goals, checkpoints, and integration tests
5. **Risks & Dependencies**
   - Outstanding legal constraints, infra needs, compute scheduling

## Outputs
- Confirmed action items with owners
- Updated sprint backlog (W39) entries for ingestion/preprocessing tasks
- Notes archived in `.code/agents/director/phase-3-kickoff.md`
