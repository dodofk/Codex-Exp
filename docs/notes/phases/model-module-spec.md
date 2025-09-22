# Model Module Interface Specification (Phase 4)

Last updated: 2025-09-21

## Goals
- Provide a stable set of Python interfaces for the Phase 4 dual-encoder retrieval stack so multiple engineers can work in parallel without merge churn.
- Support macOS + CPU-only development while leaving clear extension points for GPU acceleration and alternative model backbones.
- Align code structure with *Transforming LLMs into Cross-modal and Cross-lingual Retrieval Systems* (see `docs/research/LLM_Retrieval.pdf`) and ADR decisions (`docs/adr/ADR-001-primary-paper.md`, `docs/adr/ADR-002-fallback-modalities.md`).

## Target Directory Layout
```
src/model/
  __init__.py
  interfaces.py          # Protocols / dataclasses describing component contracts
  registries.py          # (planned) registration helpers for text/audio towers
  configs.py             # Config loader implementing ModelConfig/TrainingConfig
  trainer.py             # Training loop orchestrating towers + losses
  cli.py                 # Entry point for training/eval commands
  losses.py              # (planned) contrastive objectives + utilities
  evaluation.py          # (planned) retrieval metrics + reporting hooks
```

Kickoff deliverables now include `configs.py`, which houses the structured configuration loader (`TrainingConfig`). Other files will land incrementally as implementation work proceeds.

## Key Interfaces (live in `src/model/interfaces.py`)

| Interface | Purpose | Notes |
|-----------|---------|-------|
| `ModelConfig` | Strongly typed representation of the hierarchical YAML configuration (dataset shards, towers, optimizer, logging). | Backed by Pydantic; supports `from_path` factory. |
| `TextTower` | Encapsulates the text encoder (embedding generation, optional adapter loading). | Must expose `embed_text(batch: Batch) -> Tensor`, `to(device)`, `parameters()`. |
| `AudioTower` | Wraps audio encoder operating on Phase 3 preprocessed features. | Mirrors `TextTower` surface; ingest feature tensors rather than raw audio. |
| `ProjectionHead` | Projects tower embeddings into a shared retrieval space and applies temperature scaling. | Keeps learnable temperature optional for CPU stability. |
| `RetrievalModel` | Combines towers + projection head; provides unified `forward` returning logits and embeddings. | Composition-only—no direct optimizer logic. |
| `LossComputer` | Computes InfoNCE + auxiliary losses. | Receives embeddings/logits and returns scalar loss + diagnostics. |
| `TrainerHooks` | Optional lifecycle callbacks (on_batch_end, on_epoch_end) to simplify experiment logging. | Keeps default no-op implementations. |

All towers/head implementations should inherit from lightweight `Configurable` mixins that accept structured configs rather than ad-hoc kwargs.

## CPU-First Constraints
- Default device is `torch.device("cpu")`. GPU-specific code must be guarded (`if self.device.type != "cuda": ...`).
- Mixed precision defaults to off; enabling requires explicit config toggle and unit tests.
- Large models (e.g., 7B) must support quantized or LoRA variants to stay within macOS memory limits.
- Training loops must accept a `max_tokens_per_batch` override so contributors can downsize workloads when running locally.

## Configuration Expectations
- YAML schema stored under `config/model/`. Example keys:
  ```yaml
  text_tower:
    name: qwen3
    checkpoint: hf://Qwen/Qwen3-0.6B
    enable_lora: false
    max_length: 256
  audio_tower:
    name: distil_whisper
    checkpoint: hf://distil-whisper-small.en
    feature_source: data/processed/fleurs/smoke/features
  projection_head:
    dim: 768
    temperature_init: 0.07
  optimizer:
    name: adamw
    lr: 5e-5
  training:
    epochs: 3
    batch_size: 16
    max_tokens_per_batch: 4096
    gradient_checkpointing: true
  dataset:
    root: data/processed/fleurs/smoke
    manifest_glob: "manifest/train*.jsonl"
    batch_size: 16
    shuffle: true
    seed: 13
  evaluation:
    metrics: [recall_at_1, mrr, bleu]
  ```
- Config loader (`TrainingConfig` in `src/model/configs.py`) now supports overrides; CLI exposes `--override` along with dataset flags (`--dataset-root`, `--dataset-manifest-glob`, etc.), JSONL logging, and resume controls for ablation workflows.

## Data Contracts
- Audio tower consumes `.npy` feature tensors produced by Phase 3 (see `docs/notes/phases/preprocess-spec.md`).
- Text tower expects token IDs produced by SentencePiece/Tokenizer pipeline (to be defined in Sprint-0).
- Training batches should carry metadata (language tags, sample IDs) so metrics can emit per-language breakdowns aligned with paper goals.

## Evaluation & Telemetry Hooks
- Reuse `telemetry` package for logging loss curves, throughput, and metric values.
- Provide adapters to emit structured logs to JSONL (`data/logs/model/<run-id>/metrics.jsonl`) for QA smoke comparison.
- Summaries of BLEU/recall metrics aggregated via `scripts/model_telemetry_summary.py` (writes `data/telemetry/model_summary.json`).
- Ensure evaluation entry points can run on small shards (e.g., `fleurs_smoke`) within <10 minutes on CPU.
- CLI evaluation writes JSONL records (train + `eval_complete`) including recall@1, MRR, and corpus BLEU computed via SacreBLEU.

## Deliverables for Sprint-0
1. `src/model/interfaces.py` populated with Protocols/dataclasses reflecting the table above. ✅
2. `src/model/configs.py` delivering `TrainingConfig` loader, with baseline config under `config/model/baseline.yaml`. ✅
3. Training loop + CLI scaffolding (`src/model/trainer.py`, `src/model/cli.py`) ✅
4. Tower registries + baseline implementations (`identity`, `qwen3`, `phi2_lora`, `distil_whisper`). ✅
5. Dataset loader reading manifest shards from `data/processed/<dataset>` with batching + padding logic. ✅
6. CLI (`model.cli`) supports dataset overrides, JSONL logging, and resume workflow for multi-epoch runs. ✅

## Open Questions
- Final choice of text tower baseline (Qwen3 vs. larger Phi-2/PaLM derivatives). Decision pending benchmark on macOS hardware.
- Location for experiment manifests (`docs/notes/phases/phase-4-log.md` vs. dedicated `experiments/` directory).
- Whether to adopt Hydra vs. straight YAML + Pydantic for configuration composition.

Please append updates to this document as interfaces evolve and mark dated entries to keep change history clear.
