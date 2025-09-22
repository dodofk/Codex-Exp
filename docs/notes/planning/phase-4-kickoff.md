# Phase 4 Kickoff Agenda – Model Implementation (2025-09-22 09:00 PT)

## Objectives
- Confirm Phase 3 exit artifacts and formally commence Phase 4 workstreams.
- Align on architecture choices derived from *Transforming LLMs into Cross-modal and Cross-lingual Retrieval Systems* (`docs/research/LLM_Retrieval.pdf`).
- Establish CPU-only development workflows and modular training configuration expectations.
- Seed backlog items and ownership for the first Sprint-0 window (2025-09-22 → 2025-10-04).

## Pre-reads
- `docs/notes/planning/phase-3-readiness-review.md`
- `docs/notes/planning/program-roadmap.md`
- `docs/adr/ADR-001-primary-paper.md` and `docs/adr/ADR-002-fallback-modalities.md`
- Agent synthesis: `.code/agents/66084c42-92c0-4b43-a0be-b53ec9668e00/result.txt`

## Agenda
1. **Phase 3 sign-off recap** (Director) – 5 min
2. **Architecture baseline** (Lead Architect) – 15 min
   - Dual encoder modules, CPU-friendly model selections, fallback path
3. **Training pipeline scaffolding** (Model Engineer) – 15 min
   - Config schema plan (`config/model/`), CLI entry points, testing strategy
4. **Operations & tooling** (MLOps) – 10 min
   - `uv` dependency strategy, Make targets, telemetry integration, resource budgeting
5. **Compliance & data governance** (Compliance Steward) – 10 min
   - Licensing reminders, checkpoint distribution rules, attribution requirements
6. **Sprint-0 backlog review & commitments** (All) – 15 min
7. **Risks / parking lot** – 5 min

## Initial Deliverables & Owners
- Lead Architect:
  - Draft module interface spec for `src/model/` (encoders, projection head, trainer hooks) by 2025-09-25.
  - Produce encoder fallback memo (PaLM vs CPU baseline) referencing ADR-002 by 2025-09-26.
- Model Engineer:
  - Scaffold training loop + config loader (`config/model/baseline.yaml`) and smoke dataset binding by 2025-10-02.
  - Add `tests/model/test_config.py` for schema validation by 2025-09-29.
- MLOps Engineer:
  - Update `pyproject.toml` dependency proposal and Make targets (`model-train`, `model-eval`, `model-check`) draft by 2025-09-27.
  - Author Phase 4 ops appendix (CPU scheduling, log retention) within `docs/notes/phases/operations-runbook.md` by 2025-10-01.
- QA Lead:
  - Define metric regression thresholds (Recall@1, MRR, BLEU) and smoke evaluation script skeleton by 2025-10-03.
- Compliance Steward:
  - Verify dataset license coverage for generated embeddings/checkpoints and update compliance report by 2025-09-30.

## Risks & Mitigations (Kickoff)
- **CPU throughput** – measure baseline throughput on `fleurs_smoke`; escalate infra request if <250 samples/min.
- **Checkpoint licensing** – confirm share-alike restrictions before external artifact publishing; fallback to internal-only distribution if necessary.
- **Model availability** – PaLM checkpoint access uncertain; plan LoRA/GGUF alternatives.

## Next Steps
- Capture kickoff decisions in sprint backlog (`docs/notes/planning/sprint-backlog-W40.md`).
- Schedule weekly Phase 4 sync (Tuesdays 09:30 PT) with status logged in `docs/notes/planning/sprint-backlog.md`.
- Prepare Phase 4 status section for sponsor update due 2025-09-27.
