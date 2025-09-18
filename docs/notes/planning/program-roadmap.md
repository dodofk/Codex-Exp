# Program Roadmap

## Overview
- **Vision**: Reproduce “Transforming LLMs into Cross-modal and Cross-lingual Retrieval Systems” end-to-end, then extend it with Auto-Paper-driven ablations while maintaining auditable data governance.
- **Current Phase**: Phase 2 – Data Discovery & Governance (kickoff 2025-09-18).
- **Time Horizon**: 2025-09-18 → 2026-01-31.

## Milestones
| Milestone | Target Date | Owner | Dependencies | Success Criteria |
|-----------|-------------|-------|--------------|-----------------|
| Phase 2 kickoff alignment | 2025-09-19 | Director | ADR-001 primary paper approved | Rubric + working agreements captured in sprint backlog |
| Backup paper refresh complete | 2025-09-23 | Research Curator | Phase 1 matrix archived | Alternative papers summarized with dataset viability notes |
| Dataset shortlist checkpoint (#1) | 2025-09-18 | Data Scout & Compliance Steward | Kickoff notes circulated | Completed – shortlist approved (FLEURS, CoVoST 2, MuST-C, VoxPopuli) |
| Compliance assessment checkpoint (#2) | 2025-09-18 | Compliance Steward | Shortlist dataset matrix complete | Completed – legal restrictions documented, risk log updated |
| Manifest & sign-off checkpoint (#3) | 2025-09-18 | Director | Compliance report ready | Completed – manifest + readiness report published |
| Phase 3 readiness review | 2025-10-04 | Director | Phase 2 exit criteria met | Ingestion & preprocess backlog prioritized |

## Phase Progress
| Phase | Status | Entry Criteria | Exit Criteria | Notes |
|-------|--------|----------------|---------------|-------|
| Phase 1 – Problem & Paper Scoping | ✅ Complete (follow-up pending) | Research curator + architect assigned | ADR-001 ratified, success metrics defined | Backup paper matrix refresh due 2025-09-23. |
| Phase 2 – Data Discovery & Governance | ✅ Complete | ADR-001 finalized, rubric drafted | Dataset manifest + compliance sign-off captured | Shortlist, compliance readiness, manifest approved 2025-09-18. |
| Phase 3 – Data Ingestion & Preprocessing | 🚧 In Progress | Phase 2 deliverables accepted | Reproducible ingestion + preprocess pipelines | Kickoff targeted for 2025-09-23 (see phase-3 kickoff agenda). |
| Phase 4 – Model Implementation | ⏳ Planned | Preprocess spec stabilized | Baseline model + tests ready | Architect collecting reference implementations. |
| Phase 5 – Training Orchestration | ⏳ Planned | Baseline model merged | Experiment runner operational | Training Ops evaluating logging stack options. |
| Phase 6 – Evaluation & Analysis | ⏳ Planned | Training pipeline stabilized | Evaluation protocol validated | Evaluation agent to define metrics following Phase 5 demo. |
| Phase 7 – Documentation & Operations | ⏳ Planned | Evaluation insights assembled | Docs + CI readiness achieved | Docs + MLOps drafting release checklist template. |

## Risk Register
| Risk | Impact | Probability | Mitigation | Owner | Status |
|------|--------|-------------|------------|-------|--------|
| LDC license approval delayed | High | Medium | Submit request 2025-09-19; prepare Common Voice backup | Compliance Steward | Open |
| Backup paper coverage insufficient | Medium | Medium | Research Curator to refresh 2 alternative papers and update matrix | Director | Open |
| Low-resource language coverage insufficient | Medium | Medium | Commission regional Data Scout clone to explore local corpora | Director | Monitoring |
| Dataset checksums unavailable | Medium | Low | Coordinate with dataset maintainers; plan fallback hash generation | Data Scout | Open |
| MuST-C non-commercial clause limits downstream sharing | Medium | Low | Restrict distribution to internal use; add NC-ND notices | Compliance Steward | Mitigated |
| VoxPopuli share-alike obligation complicates model release | Medium | Medium | Apply CC BY-SA to external artifacts or keep internal; add notice in docs | Compliance Steward | Monitoring |
| YouTube-derived datasets risk takedown | Medium | Medium | Track source URLs, respect removal requests, store derived features only | Data Scout | Monitoring |

## Communication Cadence
- **Sprint Length**: 2 weeks (Thursday → Wednesday) to align with reporting cycles.
- **Stand-up Rhythm**: Daily async updates logged in `docs/notes/planning/sprint-backlog.md` (What happened / Blockers / Next steps).
- **Reviews & Retros**: Sprint review + retro every other Wednesday; Director records outcomes under sprint backlog "Retrospective Notes".
- **Stakeholder Touchpoints**: Weekly Friday sync with initiative sponsors; compliance escalations ad hoc within 24 hours of discovery.

## Upcoming Decisions
- Confirm FLEURS as primary dataset for Phase 3 ingestion (and identify backups) by 2025-09-27.
- Validate checksum tooling path (Python vs. shell-based) by 2025-09-25.
- Decide whether to instrument W&B vs. local logging ahead of Phase 5 planning.

## Notes & References
- `docs/notes/auto-paper-plan.md`
- `docs/notes/agents/agent-briefs.md`
- `.code/agents/` transcripts for Data Scout & Compliance Steward once Phase 2 work begins
- `docs/adr/ADR-001-primary-paper.md`
