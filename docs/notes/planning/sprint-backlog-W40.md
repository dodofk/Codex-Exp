# Sprint Backlog – 2025-W40 (Phase 4 Sprint-0)

## Sprint Summary
- **Dates**: 2025-09-22 → 2025-10-04
- **Sprint Goal**: Stand up modular, CPU-friendly model training scaffolding aligned with the Phase 4 kickoff decisions and reference paper.
- **Velocity Target**: 28 points (Director, Lead Architect, Model Engineer, MLOps Engineer, QA Lead, Compliance Steward).

## Committed Work
| Item | Phase | Owner | Story Points | Status | Definition of Done |
|------|-------|-------|--------------|--------|--------------------|
| Author model module interface spec (`src/model/`) | Phase 4 | Lead Architect | 5 | Complete | Spec + interfaces published; includes `ModelConfig`, tower/heads, loss hooks ready for implementation |
| Encoder fallback memo (PaLM vs CPU baseline) | Phase 4 | Lead Architect | 3 | Complete | Memo recorded in `docs/notes/planning/phase-4-log.md` outlining Phi-2 LoRA vs Mistral-q4 fallback |
| Scaffold training loop + config loader | Phase 4 | Model Engineer | 6 | Complete | Config loader + trainer + CLI landed with smoke tests |
| Design text/audio tower skeletons and registries | Phase 4 | Lead Architect & Model Engineer | 6 | Complete | Registries plus identity text + mean pooling audio towers added with tests |
| Implement placeholder loss computer and integrate with trainer | Phase 4 | Model Engineer | 4 | Complete | Dummy contrastive loss + numpy-based trainer execute over smoke batches |
| Update CLI to instantiate components using baseline config | Phase 4 | Model Engineer | 3 | Complete | CLI loads baseline config, instantiates towers/loss, runs smoke training (see `tests/model/test_cli.py`) |
| Add model config validation tests | Phase 4 | Model Engineer | 3 | Complete | `tests/model/test_config.py` and CLI smoke test committed |
| Dependency & tooling proposal (`pyproject`, Make targets) | Phase 4 | MLOps Engineer | 4 | Complete | Proposal documented in `docs/notes/planning/phase-4-dependency-proposal.md`; torch CPU install instructions validated |
| Phase 4 ops appendix (CPU scheduling/log retention) | Phase 4 | MLOps Engineer | 2 | Complete | Section added to `docs/notes/phases/operations-runbook.md` covering CPU limits, telemetry, and incident handling |
| Define metric regression thresholds + smoke eval script | Phase 4 | QA Lead | 3 | Complete | `scripts/model_eval.py` + `docs/notes/planning/phase-4-qa-summary.md` capture smoke thresholds & follow-up actions |
| Compliance review for embeddings/checkpoints | Phase 4 | Compliance Steward | 2 | Complete | Compliance readiness report updated (2025-09-21) with guidance on embedding/checkpoint distribution |

## Supporting Tasks
- Prepare kickoff deck/notes (`docs/notes/planning/phase-4-kickoff.md`).
- Schedule weekly Phase 4 stand-up; update `docs/notes/planning/sprint-backlog.md` with daily async entries.
- Coordinate with Data Scout on any additional corpus needs flagged during architecture planning.

## Blockers to Monitor
- PaLM checkpoint access ETA from platform team.
- Availability of CPU resources for long-running jobs (consider remote executor if throughput insufficient).
- Share-alike obligations (VoxPopuli/WikiMatrix) impacting model artifact sharing.

## References
- `docs/notes/planning/phase-4-kickoff.md`
- `docs/notes/planning/program-roadmap.md`
- `docs/research/LLM_Retrieval.pdf`
