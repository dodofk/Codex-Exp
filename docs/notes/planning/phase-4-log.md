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

## 2025-10-06 Phi-2 LoRA Text Tower
- **Owner**: Model Engineer
- **Summary**: Added `phi2_lora` tower implementation (`src/model/towers/phi2.py`) using transformers + LoRA with registry integration. Baseline config updated to use `sshleifer/tiny-gpt2` for smoke runs.
- **Notes**: Tests are skipped when PyTorch/transformers are unavailable (current macOS Python 3.13 build). Full validation pending official PyTorch wheels; document fallback behavior in release notes.

## 2025-10-06 Distil-Whisper Audio Tower
- **Owner**: Model Engineer
- **Summary**: Implemented `distil_whisper` audio tower (`src/model/towers/whisper.py`) loading Whisper checkpoints via transformers; baseline config now points to `openai/whisper-tiny` for smoke runs.
- **Notes**: Similar to text tower, tests skip if torch/transformers are missing. Replace mean-pooling placeholder in future once feature pipeline confirmed.
