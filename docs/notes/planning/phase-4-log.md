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

