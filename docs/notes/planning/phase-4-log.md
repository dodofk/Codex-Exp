# Phase 4 Log – Model Implementation

## 2025-09-21 Encoder Fallback Memo
- **Prepared by**: Lead Architect
- **Context**: ADR-001 establishes PaLM-based dual encoder as target; ADR-002 defines fallback modalities. macOS dev environment lacks CUDA; need practical CPU baseline.
- **Decision**:
  - Use `phi-2` (2.7B) with LoRA adapters as primary CPU-friendly text tower for local development.
  - Maintain `Mistral-7B-q4` GGUF variant as optional alternative if Phi-2 licensing blocks distribution.
  - Audio tower baseline: `distil-whisper-small.en` fine-tuned with mean-pooling head; supports CPU inference.
  - Retrieval head + loss remain framework-agnostic; eventual GPU runs can swap implementations via registry.
- **Implications**:
  - Baseline configs (`config/model/baseline.yaml`) default to lightweight identity / mean pooling towers for smoke tests; we will swap to Phi-2/Whisper once quantized checkpoints integrated.
  - LoRA adapter weights must be kept internal until compliance clears redistribution.
  - Need follow-up ticket to document quantization + checkpoint instructions for developers.
- **Next Actions**:
  - Open backlog item to evaluate Phi-2 vs Mistral throughput on macOS (due 2025-09-24).
  - Update compliance report with checkpoint distribution guidelines (ties to existing sprint task).
  - Ensure trainer/CLI support hot-swapping towers via registries (done in current sprint).

## 2025-09-22 Qwen3 Baseline Swap
- **Owner**: Model Engineer
- **Summary**: Swapped default text tower from Phi-2 LoRA to `qwen3` (0.6B) for CPU-friendly experimentation. Generalized HF tower loader to support optional LoRA, Qwen `trust_remote_code`, and broader dtype handling. Added registry aliases for `qwen3` and `qwen3_lora` while keeping `phi2_lora` compatible.
- **Implications**: Baseline config now references `Qwen/Qwen3-0.6B`; LoRA remains opt-in per config. Future large-model integrations (PaLM, Phi-2) reuse the generalized tower without code changes.

## 2025-09-22 Manifest Dataset Loader
- **Owner**: Model Engineer
- **Summary**: Implemented manifest-driven dataset loader (`src/model/data/loader.py`) producing padded batches from `data/processed/<dataset>` shards. CLI now consumes dataset config, replacing synthetic smoke batches.
- **Implications**: Baseline config includes `dataset` block with manifest glob, shuffle controls, and batch overrides. Tests fabricate lightweight manifests to keep CPU smoke runs hermetic. Future work: integrate tokenizer outputs when text token manifests become available and wire loader into CLI logging once JSONL telemetry lands.

## 2025-09-22 Model CLI Enhancements
- **Owner**: MLOps Engineer
- **Summary**: Extended `model.cli` with dataset override flags, JSONL logging, and resume support. Training now honours multi-epoch configs, logs per-epoch metrics, and reuses existing logs to skip completed epochs. Evaluation runs compute recall@1, MRR, and corpus BLEU (via SacreBLEU) and emit structured metrics alongside training output.
- **Implications**: Configs can be shared across agents while still allowing developers to override dataset paths at runtime. JSONL logs feed directly into QA telemetry. Resume behaviour relies on log records; follow-up task will capture optimizer state once we integrate torch-based training.

## 2025-09-22 Telemetry Aggregation Script
- **Owner**: QA Lead
- **Summary**: Added `scripts/model_telemetry_summary.py` to aggregate per-run logs under `data/logs/model/` and produce `data/telemetry/model_summary.json` with averaged recall/MRR/BLEU per dataset.
- **Implications**: QA can reference a single artifact for readiness reviews. Future work: integrate with dashboards once Phase 5 telemetry targets are defined.

## 2025-09-23 Torch-capable InfoNCE Loss
- **Owner**: Model Engineer
- **Summary**: Upgraded `InfoNCELoss` to leverage PyTorch autograd when available while keeping the NumPy fallback. `Trainer` now feeds raw tower outputs into the loss, enabling gradient propagation for future optimizer integration.
- **Implications**: Torch-based runs can compute gradients without modifying the trainer. Ensure future optimizers pass a real torch optimizer to `Trainer.train_epoch` for parameter updates.

## 2025-10-06 Phi-2 LoRA Text Tower
- **Owner**: Model Engineer
- **Summary**: Added `phi2_lora` tower implementation (`src/model/towers/phi2.py`) using transformers + LoRA with registry integration. Baseline config updated to use `sshleifer/tiny-gpt2` for smoke runs.
- **Notes**: Tests are skipped when PyTorch/transformers are unavailable (current macOS Python 3.13 build). Full validation pending official PyTorch wheels; document fallback behavior in release notes.

## 2025-10-06 Distil-Whisper Audio Tower
- **Owner**: Model Engineer
- **Summary**: Implemented `distil_whisper` audio tower (`src/model/towers/whisper.py`) loading Whisper checkpoints via transformers; baseline config now points to `openai/whisper-tiny` for smoke runs.
- **Notes**: Similar to text tower, tests skip if torch/transformers are missing. Replace mean-pooling placeholder in future once feature pipeline confirmed.
