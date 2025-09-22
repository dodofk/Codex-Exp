# Phase 4 Dependency & Tooling Proposal

_Last edited: 2025-09-21_

## Objectives
- Document package additions required for CPU-first model implementation.
- Outline optional extras and Makefile extensions before modifying `pyproject.toml`.
- Provide action items for MLOps sign-off and backlog tracking.

## Python Dependencies (baseline `pyproject.toml`)
| Package | Version Hint | Purpose | Notes |
|---------|--------------|---------|-------|
| torch | 2.3.1 (cpu) | Core tensor ops / autograd | Install via PyTorch index: `uv pip install --index-url https://download.pytorch.org/whl/cpu torch==2.3.1+cpu`; guard import errors for devs without torch.
| torchaudio | 2.3.1+cpu | Audio feature loading (Whisper integration) | Optional at runtime; keep behind extra. |
| transformers | ^4.44 | Text tower backbones (Phi-2, Mistral) | Avoid GPU-specific dependencies. |
| accelerate | ^0.34 | Device-agnostic training helpers | Enables zero-gpu config when GPU available. |
| optimum (optional) | ^1.21 | Quantization & optimized kernels | Useful for GGUF or ONNX experiments. |
| sentencepiece | ^0.2 | Tokenization for multilingual text | Already used in preprocessing; align versions. |
| soundfile | ^0.12 | Audio IO support | CPU-friendly. |
| numpy | (existing) | Placeholder towers already rely on numpy; ensure version pinned >= 2.0.
| pydantic | ^2.7 | Already implied via config loader; confirm locked.

### Optional Extras
- Add `[project.optional-dependencies.model-cpu]` containing `torch`, `torchaudio`, `transformers`, `accelerate`, `optimum`, `sentencepiece`, `soundfile`.
- Keep base install minimal; tests referencing torch should be skipped gracefully if extras missing.

## Makefile Extensions
| Target | Command | Description |
|--------|---------|-------------|
| `model-train` | `PYTHONPATH=src uv run python -m model.cli config/model/baseline.yaml --mode train` | Runs baseline training locally (CPU smoke).
| `model-eval` | `PYTHONPATH=src uv run python -m model.cli config/model/baseline.yaml --mode eval` | Evaluation placeholder (once metrics wired).
| `model-check` | `PYTHONPATH=src uv run pylint`/`pytest tests/model` | Wrapper to lint/test model package; confirm final command with QA.

## Future Enhancements
- Hydra-style overrides for nested config keys (evaluate `omegaconf` vs manual approach).
- CLI options for dataset shard selection and logging to JSONL.
- Integrate accelerate config file (`accelerate config`) for multi-device runs once GPU infra available.

## Action Items
1. Validate license compatibility for torch/transformers binaries (Compliance Steward) — due 2025-09-24.
2. Update `pyproject.toml` + `uv.lock` with dependencies (MLOps) after review — target 2025-09-25.
3. Add Makefile targets and document usage in README/ops runbook — target 2025-09-26.
4. QA to ensure CI installs `model-cpu` extras for relevant jobs. 

## Reviewers
- MLOps Engineer (primary)
- Model Engineer (secondary)
- Compliance Steward (license verification)
