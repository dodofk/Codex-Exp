# Sprint Backlog – 2025-W41 (Phase 4 Sprint-1)

## Sprint Summary
- **Dates**: 2025-10-06 → 2025-10-17
- **Sprint Goal**: Deliver a working dual-encoder baseline capable of training on CPU with real tower implementations and evaluation metrics, paving the way for GPU scaling.
- **Velocity Target**: 30 points (Lead Architect, Model Engineer, MLOps Engineer, QA Lead, Compliance Steward).

## Committed Work
| Item | Phase | Owner | Story Points | Status | Definition of Done |
|------|-------|-------|--------------|--------|--------------------|
| Implement Phi-2 LoRA text tower | Phase 4 | Model Engineer | 8 | In Review | `phi2_lora` tower implemented with registry entry; tests skip if torch unavailable |
| Integrate Distil-Whisper audio tower | Phase 4 | Model Engineer | 8 | In Review | `distil_whisper` tower implemented (`src/model/towers/whisper.py`); tests skip when torch unavailable |
| Replace dummy loss with InfoNCE + spreadout regularizer | Phase 4 | Lead Architect & Model Engineer | 5 | Not Started | Loss module computes contrastive objective and logs metrics |
| Dataset loader + batching pipeline | Phase 4 | Model Engineer | 4 | Not Started | Loader pulls from `data/processed/<dataset>` with configurable shards |
| CLI training enhancements (`model-train`) | Phase 4 | MLOps Engineer | 3 | Not Started | CLI supports dataset selection, logging to JSONL, and resume options |
| Update Makefile + pyproject extras (`model-cpu`) | Phase 4 | MLOps Engineer | 2 | Not Started | Dependencies merged, new targets documented in README |
| Evaluation metrics (MRR, BLEU) & reporting | Phase 4 | QA Lead | 3 | Not Started | `scripts/model_eval.py` computes MRR/BLEU and CLI eval emits MetricReport |
| Compliance checkpoint for model artifacts | Phase 4 | Compliance Steward | 2 | Not Started | Policy note added covering LoRA/quantized checkpoints

## Supporting Tasks
- Benchmark Phi-2 vs. Mistral-q4 CPU throughput (report in phase-4-log).
- Coordinate with Ops on remote executor feasibility if CPU throughput < target.
- Begin drafting ADR addendum for GPU transition requirements once baseline stabilizes.

## Blockers to Monitor
- PaLM checkpoint access timeline (for future alignment).
- Availability of Hugging Face caches for large models on macOS.

## References
- `docs/notes/planning/phase-4-log.md`
- `docs/notes/planning/phase-4-dependency-proposal.md`
- `docs/notes/planning/program-roadmap.md`
