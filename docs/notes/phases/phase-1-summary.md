# Phase 1 Summary – Problem & Paper Scoping

- **Primary Target**: “Transforming LLMs into Cross-modal and Cross-lingual Retrieval Systems” (arXiv 2024). Focuses on aligning multilingual speech encoders with instruction-tuned LLM backbones for retrieval across modalities and languages.
- **Backup Papers**:
  - “SpeechCLIP: Integrating Speech and Text into a Shared Embedding Space” (Interspeech 2022) – CLIP-style dual encoders over AudioCaps, Clotho, SpokenCOCO.
  - “CLAP: Learning Audio Concepts from Natural Language Supervision” (ICASSP 2023) – Large-scale audio-text pretraining with AudioSet/LAION-Audio, useful for feature initialization.

## Success Criteria
- Replicate core retrieval metrics: ≥35% R@1 on FLEURS multilingual queries, ≥0.42 MRR on CoVoST2 speech↔text, and demonstrate zero-shot transfer on at least one backup dataset (AudioCaps or Clotho).
- Maintain auditable data governance (attribution, share-alike compliance, non-commercial clauses) for every dataset listed in `docs/notes/datasets/dataset-landscape.md`.
- Deliver ADR updates capturing architectural choices, compute budget (≤4×A100 80GB nodes per training run), and risk mitigations for share-alike and non-commercial clauses.

## Outstanding Questions
- Confirm availability and licensing obligations for VoxPopuli share-alike terms and MuST-C non-commercial clause prior to ingestion.
- Determine whether the primary paper’s announced code release is available; otherwise plan reproduction from hyperparameter tables.
- Evaluate if CLAP checkpoints can be integrated without violating YouTube/AudioSet ToS.

## Next Actions
- Research Curator: Ensure `docs/research/paper_matrix.csv` stays current with citation details, dataset viability notes, and links to code artifacts or pending releases.
- Lead Architect: Draft ADR addendum summarizing fallback strategies per dataset and compute budget implications.
- Director: Align Phase 2 kickoff agenda with these success criteria and track dependencies in `docs/notes/planning/program-roadmap.md`.
