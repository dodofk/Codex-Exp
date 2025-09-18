# Auto-Paper Implementation Plan

## Phase 1 – Problem & Paper Scoping
- Research Curator agent shortlists 3–5 recent speech/NLP papers, extracting datasets, architectures, metrics, and code links into a comparison matrix.
- Lead Architect agent defines success criteria, target metrics, and compute budgets; publishes an ADR selecting the primary paper and secondary references.

## Phase 2 – Data Discovery & Governance
- Data Scout agent catalogs candidate corpora, covering licenses, download sources, preprocessing hints, and known pitfalls.
- Compliance agent reviews legal/privacy constraints and signs off on an approved dataset manifest with checksums and storage paths.

## Phase 3 – Data Ingestion & Preprocessing
- Ingestion Engineer agent builds resumable download scripts, establishes `data/raw`, `data/interim`, and `data/processed` structure, and validates checksums.
- Preprocess Engineer agent implements normalization, tokenization, or acoustic feature extraction per paper specs, with unit tests and lineage logging.

## Phase 4 – Model Implementation
- Model Architect agent drafts a configurable model skeleton that reconciles differences between selected papers and documents optional variants.
- Model Engineer agent implements the baseline network, losses, schedulers, and shared utilities, delivering smoke tests and configuration schemas.

## Phase 5 – Training Orchestration
- Training Ops agent develops an experiment runner with checkpointing, logging, deterministic seeds, and mixed-precision toggles.
- Hyperparameter agent scripts sweeps covering reported settings plus exploratory ranges within the agreed compute budget, producing an experiment registry.

## Phase 6 – Evaluation & Analysis
- Evaluation agent reproduces reported metrics, manages validation/test splits, and checks statistical significance.
- Insight Synthesizer agent aggregates results across papers, prepares plots and tables, and highlights deviations or ablations worth reporting.

## Phase 7 – Documentation & Operations
- Docs agent maintains README, quickstarts, ADR updates, and archives agent transcripts in `.code/agents/` while summarizing outcomes in `docs/notes/`.
- MLOps agent defines CI hooks (`make lint`, `make test`, dataset checksum verification), model registry/export steps, and long-term maintenance tasks.
