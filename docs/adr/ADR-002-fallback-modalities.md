# ADR-002: Fallback Retrieval Architectures

- **Date**: 2025-09-18
- **Status**: Draft – Retained as contingency (legal cleared primary datasets)
- **Owner**: Lead Architect
- **Related ADRs**: ADR-001 (Primary Paper Selection)

## Context
ADR-001 selects “Transforming LLMs into Cross-modal and Cross-lingual Retrieval Systems” as the baseline. However, access to PaLM-family checkpoints or share-alike datasets (e.g., VoxPopuli) may be restricted by licensing outcomes currently under legal review. We need a contingency plan that preserves project momentum if we must pivot to alternative architectures or datasets.

## Proposed Alternatives
1. **SpeechCLIP (Interspeech 2022)** – Dual encoder over AudioCaps/Clotho/SpokenCOCO with CLIP-style contrastive loss. Suitable for audio-text retrieval with public checkpoints; relies on CC-BY datasets plus MSCOCO licensing for SpokenCOCO.
2. **CLAP (ICASSP 2023)** – Large-scale audio-text contrastive pretraining (AudioSet, LAION-Audio). Offers open-source checkpoints and supports fine-tuning for multilingual retrieval when paired with translation corpora.

## Decision (Pending)
- Adopt SpeechCLIP or CLAP as the fallback baseline if: (a) legal guidance blocks redistribution of models trained on MuST-C/VoxPopuli, or (b) PaLM checkpoints are unavailable for licensing reasons.
- Prioritize datasets with permissive licenses (AudioCaps, Clotho, Multilingual LibriSpeech) to minimize legal overhead.

## Rationale
- Both alternatives have open implementations and proven retrieval metrics, enabling faster pivot.
- They can integrate with existing dataset landscape entries and share preprocessing pipelines (audio feature extraction, caption normalization).
- Maintains alignment with Auto-Paper’s cross-modal objectives while avoiding NC/SA complexities if required.

## Consequences
- **Data**: If fallback triggered, update dataset manifest to deprioritize MuST-C/VoxPopuli and elevate AudioCaps/Clotho/MLS.
- **Model**: Training scripts must support CLIP-style dual encoders alongside PaLM-based architecture.
- **Evaluation**: Metrics shift toward audio-caption retrieval benchmarks (R@K, mAP) in addition to cross-lingual metrics.
- **Documentation**: Roadmap and backlog require updates; ADR-001 remains baseline but references ADR-002 for contingency.

- ## Follow-up Actions
- Monitor PaLM checkpoint availability; if licensing blocks primary plan, revisit this ADR to Accept.
- Prototype minimal SpeechCLIP training on AudioCaps once ingestion pipeline exists to estimate compute requirements.
- Coordinate with Director to add conditional milestones in program roadmap if fallback activated.
