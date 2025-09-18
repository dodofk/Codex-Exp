# Dataset Shortlist – Checkpoint #1 (2025-09-18)

| Priority | Dataset | Role | Score | Key Rationale | Compliance Notes |
|----------|---------|------|-------|---------------|------------------|
| 1 | FLEURS / XTREME-S | Primary evaluation corpus (multilingual speech↔text) | 16 | High language overlap with target benchmarks; published checksums; manageable licensing | CC-BY attribution required in README/manifest |
| 2 | CoVoST 2 | Core training corpus (speech↔text) | 15 | Parallel speech-text pairs aligned with paper; CC0 license; complements FLEURS languages | Maintain volunteer consent reference; scrub incidental PII |
| 3 | MuST-C v2 | Transfer/generalization dataset | 12 | Adds TED domain diversity and longer utterances; aligns with paper’s augmentation | Internal use only (CC BY-NC-ND); no external model/data release without FBK approval |
| 4 | VoxPopuli | Large-scale multilingual speech for robustness | 12 | Provides varied accents/domains; supports zero-shot evaluation | External artifacts must inherit CC BY-SA 4.0; add share-alike notice |

## Reserves / Optional Datasets
- **Multilingual LibriSpeech (Score 14)** – Smaller but public domain; useful for clean speech sanity checks.
- **How2 / How2QA, AudioCaps, Clotho v2 (Score 11)** – Retain for cross-modal enrichment; ingest only derived features per compliance notes.

## Action Items
- Update `docs/notes/datasets/dataset-manifest.md` to reflect shortlist status (done).
- Present shortlist at Checkpoint #1 review and capture approvals in `.code/agents/director/` notes.
- Align Phase 3 kickoff agenda with ingestion order (FLEURS/CoVoST first, MuST-C/VoxPopuli after compliance-driven setup).
