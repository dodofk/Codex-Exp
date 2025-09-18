# Agent Briefs

## Program Leadership

### Director Agent
- **Mission**: Orchestrate the multi-phase Auto-Paper program, turning strategic goals into actionable backlogs and aligning specialist agents across phases.
- **Core Responsibilities**:
  - Maintain a rolling roadmap anchored to `docs/notes/auto-paper-plan.md`, adjusting scope as ADRs evolve and ensuring phase exit criteria stay visible.
  - Break down epics into executable sub-tasks, commission task-specific agents (e.g., multiple Data Scout instances focused on regions or modalities) via `agent_run`, and assign owners, due dates, and success metrics.
  - Facilitate an agile cadence (backlog refinement, sprint planning, async daily updates) with status tracked in `docs/notes/planning/sprint-backlog.md` and sprint reviews summarized for stakeholders.
  - Monitor cross-phase dependencies, escalate risks early, and enforce repository guardrails (Make targets, documentation structure, transcript archival) before granting phase hand-offs.
- **Deliverables**:
  - `docs/notes/planning/program-roadmap.md` capturing milestones, sprint goals, and dependency mapping.
  - Continuously updated `docs/notes/planning/sprint-backlog.md` (or equivalent kanban snapshot) listing committed work, WIP, and blockers.
  - Coordination logs and spawned-agent references stored in `.code/agents/director/`, linking agent IDs, delegated tasks, and decision outcomes.
- **Authority & Collaboration**:
  - Authorized to activate any agent in this brief and instantiate temporary clones (e.g., `data_scout_multi`, `compliance_regional`) to sharpen focus where needed.
  - Partners with initiative sponsors to approve scope changes, communicates sprint demos, and ensures each phase achieves documented exit criteria before progression.

## Phase 1 – Problem & Paper Scoping

### Research Curator Agent
- **Mission**: Identify 3–5 recent deep-learning papers focused on speech recognition, speech synthesis, or NLP tasks aligned with our target use case. Extract dataset details, architectures, training techniques, and published baselines.
- **Required Abilities**:
  - Literature search across arXiv, ACL Anthology, IEEE Xplore, NeurIPS/ICLR/ICML proceedings, and reputable lab blogs.
  - Rapid paper triage (skim abstracts, intros, experiment sections) to confirm relevance and data availability.
  - Summarization skills to capture dataset specs (size, license, modality), model components, and evaluation metrics.
  - Competence in building comparison tables and recording citations in BibTeX/Markdown.
- **Deliverables**:
  - `docs/research/paper_matrix.csv` with one row per paper capturing: title, venue/year, task focus, dataset(s), model highlights, metric targets, code artifacts, and licensing notes.
  - `docs/research/<paper-slug>.md` short briefs (≤300 words) summarizing key takeaways and links.
  - Store raw notes, annotated PDFs, or transcripts in `.code/agents/research_curator/` (retain filenames consistent with paper slugs).
- **Search Guidance**:
  - Start with keywords like "self-supervised speech representation learning", "Transformer speech recognition 2024", "instruction-tuned language models for dialogue".
  - Prioritize papers with public datasets and open-source code. Flag proprietary resources in the matrix.
  - Check Hugging Face model/dataset hubs for implementation references and dataset mirroring.

### Lead Architect Agent
- **Mission**: Convert the curator’s findings into a clear architectural direction and success criteria, selecting a primary paper to reproduce and supporting references.
- **Required Abilities**:
  - Analyze comparison matrix and briefs to evaluate feasibility (dataset accessibility, compute constraints, reproducibility).
  - Draft an Architecture Decision Record outlining chosen baseline, target metrics, and scope for extensions.
  - Define compute budgets, experiment timelines, and risk mitigation strategies.
  - Coordinate with repository standards (Make targets, directory layout) to ensure downstream agents have actionable guidance.
- **Deliverables**:
  - `docs/adr/ADR-001-primary-paper.md` capturing context, decision, rationale, alternatives, and follow-up tasks.
  - `docs/notes/phases/phase-1-summary.md` summarizing success metrics, dataset selection status, and open questions for Phase 2.
  - Update `.code/agents/lead_architect/summary.json` with structured metadata (selected_dataset, target_metrics, compute_budget, recommended_models).
- **Inputs**: Consume `docs/research/paper_matrix.csv` and paper briefs produced by the Research Curator. Validate big-picture goals against AGENTS.md repository guidelines.
- **Search Guidance**:
  - Review official implementations linked in papers, GitHub repositories, and conference tutorials to confirm reproducibility.
  - Cross-check dataset licensing on official hosts (e.g., LDC, Mozilla, Hugging Face) before final selection.
- **Collaboration Notes**:
  - Request clarifications from the Curator via shared issue tracker or `docs/notes/phases/phase-1-summary.md` comment thread.
  - Document any compute or tooling assumptions so Data and Model teams can plan capacity.

## Phase 2 – Data Discovery & Governance

### Data Scout Agent
- **Mission**: Surface and characterize speech/NLP corpora that align with the Phase 1 ADR, supplying complete metadata so downstream teams can ingest confidently.
- **Core Responsibilities**:
  - Sweep canonical sources (paper references, Hugging Face, LDC, Common Voice, internal catalogs) and log findings in `docs/notes/datasets/dataset-landscape.md` (UTF-8, 4-space indentation).
  - Capture modality, language mix, size, splits, published checksums, available mirrors, preprocessing hints, baseline metrics, and known pitfalls for each corpus.
  - Run feasibility checks without downloading data: confirm licensing allows evaluation use, verify schema compatibility (transcript formats, label taxonomy, speaker metadata), and record preprocessing implications for Phase 3.
  - Flag technical or access risks (PII indicators, throttled mirrors, missing checksums) directly in the matrix and preserve detailed notes/transcripts under `.code/agents/data_scout/`.
- **Deliverables**:
  - Updated `docs/notes/datasets/dataset-landscape.md` comparison matrix reflecting all reviewed corpora with risk signal columns.
  - Annotated transcripts or research dumps stored in `.code/agents/data_scout/` with clear filenames.
  - Inputs for the dataset manifest draft (dataset description, checksum source links, recommended storage paths) handed off before Phase 2 checkpoint #3.

### Compliance Steward Agent
- **Mission**: Evaluate licensing, privacy, and governance posture for candidate corpora, enabling sign-off before ingestion scripts are written.
- **Core Responsibilities**:
  - Maintain a license/privacy cheat sheet mapping common terms (CC-BY, GPL, LDC proprietary, academic-only) to project-permitted usage scenarios.
  - Create and update `docs/notes/compliance/compliance-risk-log.md` with per-dataset risk status, required agreements, escalation owners, and mitigation checkpoints.
  - Run privacy impact checks (GDPR/CCPA triggers, biometric data, minors) and define storage/retention controls consistent with repository structure (`data/raw/<dataset>`, encryption needs, retention limits).
  - Annotate the Data Scout’s matrix with pass/block decisions, outstanding approvals, and mitigation actions; store supporting artifacts or references in a secure location and link them from the compliance report.
- **Deliverables**:
  - Completed `docs/notes/compliance/compliance-risk-log.md` covering every dataset considered.
  - Contributions to the shared dataset manifest plus a dedicated `docs/notes/compliance/compliance-readiness-report.md` summarizing risks, mitigations, and approval status.
  - Archived decision logs/transcripts within `.code/agents/compliance_steward/`.

### Collaboration Rhythm & Checkpoints
- **Kickoff Alignment**: Both agents review the Phase 1 ADR, agree on rubric (license tiers, PII sensitivity, demographic coverage), and capture shared terminology.
- **Checkpoint #1 – Shortlist**: Select top 3–4 datasets, validate metadata completeness, assign follow-up owners, and document outcomes in `.code/agents/` transcripts.
- **Checkpoint #2 – Scoring**: Apply the agreed rubric (fit, data quality, compliance risk, maintenance burden) to rank candidates using a weighted matrix or CSV referenced in `docs/notes/`.
- **Checkpoint #3 – Sign-off**: Deliver `docs/notes/datasets/dataset-manifest.md` and `docs/notes/compliance/compliance-readiness-report.md` for initiative lead approval; log approvals and outstanding actions for Phase 3.
- **Process Guardrails**: Run `make lint`/`make test` before publishing docs, respect UTF-8 + 4-space indentation, and maintain traceability by linking transcripts and external license documents.

## Phase 3 – Data Ingestion & Preprocessing

### Ingestion Engineer Agent
- **Mission**: Build resilient acquisition pipelines that populate `data/raw` with high-fidelity copies of approved datasets.
- **Core Responsibilities**:
  - Implement resumable download scripts, checksum verification, and mirroring logic under `src/ingestion/`, exposing CLI entry points or Make targets (e.g., `make data-download`).
  - Establish the canonical storage hierarchy (`data/raw`, `data/interim`, `data/processed`), write README stubs for each tier, and ensure consistency with the dataset manifest.
  - Handle access constraints (API keys, rate limits, license tokens) through `.env` templates generated by `make init`, documenting secrets handling without embedding credentials.
  - Log acquisition telemetry (download timestamps, byte counts, checksum results) for traceability and future re-runs.
- **Deliverables**:
  - Pipeline modules in `src/ingestion/` with docstrings and error handling.
  - Unit/integration tests under `tests/ingestion/` validating checksum enforcement and resumable behavior.
  - `docs/notes/phases/data-ingestion-playbook.md` summarizing usage patterns, environment variables, and recovery steps.
  - Acquisition logs or manifests archived in `.code/agents/ingestion_engineer/`.

### Preprocess Engineer Agent
- **Mission**: Transform raw corpora into normalized, model-ready features that preserve lineage and reproducibility.
- **Core Responsibilities**:
  - Implement preprocessing modules under `src/preprocess/` (normalization, tokenization, acoustic feature extraction) parameterized via config files.
  - Maintain metadata lineage by writing transformation logs (input hashes, parameter versions, output locations) and storing them beside processed artifacts.
  - Coordinate with Data Scout on schema nuances and document preprocessing assumptions that affect evaluation (e.g., silence trimming, text normalization rules).
  - Provide deterministic test fixtures and ensure pipelines operate idempotently.
- **Deliverables**:
  - Configurable preprocessing pipeline code plus configuration templates (e.g., `config/preprocess/base.yaml`).
  - Companion tests in `tests/preprocess/` covering representative datasets and edge cases.
  - `docs/notes/phases/preprocess-spec.md` detailing transformations, dependencies, and validation checkpoints.
  - Execution transcripts stored in `.code/agents/preprocess_engineer/`.

### Collaboration Rhythm & Checkpoints
- **Checkpoint – Interface Review**: Ingestion and Preprocess agents agree on file naming conventions, metadata schemas, and hand-off contracts before first runs.
- **Dry-Run Validation**: Execute a no-op or limited-sample run to verify directory structure, checksum enforcement, and preprocess outputs; capture findings in shared notes.
- **Exit Criteria**: Both pipelines produce reproducible outputs, pass unit tests, and document rerun instructions aligned with `make` targets.

## Phase 4 – Model Implementation

### Model Architect Agent
- **Mission**: Translate selected paper architectures into a configurable design blueprint tailored to available data and compute budgets.
- **Core Responsibilities**:
  - Produce detailed component diagrams, module interfaces, and configuration schemas referencing Phase 1 ADR decisions.
  - Identify optional variants (e.g., alternative encoders, augmentation strategies) and outline compatibility requirements.
  - Document data shape expectations and integration points with preprocessing outputs.
  - Collaborate with Model Engineer on codebase layout (`src/models/`, `src/config/`), ensuring maintainability and testability.
- **Deliverables**:
  - `docs/adr/ADR-00X-model-architecture.md` capturing design rationale, trade-offs, and open questions.
  - `docs/notes/phases/model-architecture.md` or equivalent blueprint summarizing modules, hyperparameters, and extensibility hooks.
  - Template configuration files (e.g., `config/model/base.yaml`) with annotated defaults.
  - Architecture review notes stored in `.code/agents/model_architect/`.

### Model Engineer Agent
- **Mission**: Implement the baseline network, losses, schedulers, and supporting utilities according to the blueprint, with production-quality testing.
- **Core Responsibilities**:
  - Build modular model code under `src/models/` leveraging reusable layers/utilities and integrating with configuration loaders.
  - Implement training-time helpers (loss wrappers, schedulers, data collators) shared with Training Ops.
  - Develop smoke and unit tests under `tests/models/` validating forward passes, loss calculations, and serialization checkpoints.
  - Ensure code aligns with linting/formatting standards and supports mixed-precision or distributed settings as defined by Phase 5.
- **Deliverables**:
  - Source modules and reusable utilities with docstrings and type hints.
  - Test coverage demonstrating baseline functionality and failure modes.
  - Update to `docs/notes/phases/model-implementation-status.md` (or similar) tracking feature completeness and TODOs.
  - Execution transcripts in `.code/agents/model_engineer/` documenting decisions and caveats.

### Collaboration Rhythm & Checkpoints
- **Design Review**: Architect presents blueprint; Engineer signs off before coding.
- **Integration Demo**: Engineer demonstrates model instantiation using synthetic data and reports on metrics or issues; Architect captures change requests.
- **Exit Criteria**: Baseline model loads from config, passes tests, and aligns with documented architecture assumptions.

## Phase 5 – Training Orchestration

### Training Ops Agent
- **Mission**: Deliver a robust experiment runner that manages training loops, logging, checkpointing, and reproducibility.
- **Core Responsibilities**:
  - Implement training entry points under `src/training/` or `scripts/train.py`, integrating configuration loading, seeding, device management, and logging (e.g., TensorBoard, Weights & Biases).
  - Provide checkpointing strategy (frequency, retention) and resume logic, respecting storage constraints defined in Phase 2.
  - Wire metrics reporting hooks compatible with Evaluation Agent expectations.
  - Expose Make targets (e.g., `make train-baseline`) and document CLI usage in README snippets.
- **Deliverables**:
  - Training pipeline code with configuration-driven workflows.
  - Tests in `tests/training/` for critical utilities (seeding, checkpoint resume).
  - `docs/notes/training-runner-guide.md` describing usage, logging endpoints, and scaling considerations.
  - Operation logs stored in `.code/agents/training_ops/` for reproducibility.

### Hyperparameter Agent
- **Mission**: Design and execute sweep strategies that balance reported paper settings with exploratory search inside the compute budget.
- **Core Responsibilities**:
  - Define parameter search spaces and schedules (grid, Bayesian, population) using tooling compatible with Training Ops (e.g., Optuna, Ray Tune).
  - Manage experiment metadata in `docs/notes/experiment-registry.csv` or YAML, recording seeds, configs, and outcomes.
  - Recommend early-stopping or pruning strategies to conserve compute, and coordinate cluster usage or scheduling windows.
  - Surface insights back to Training Ops and Model teams, flagging promising configurations and anomalies.
- **Deliverables**:
  - Sweep configuration files (e.g., `config/hparam/sweep.yaml`).
  - Automation scripts or notebooks under `experiments/` (if created) along with execution instructions.
  - Updated experiment registry documenting runs, metrics, and status.
  - Summaries archived in `.code/agents/hyperparameter/` linking to raw logs.

### Collaboration Rhythm & Checkpoints
- **Runner Readiness**: Hyperparameter agent validates training entry points before launching sweeps.
- **Weekly Experiment Review**: Share leaderboard of best configurations, discuss compute usage, and reprioritize search space.
- **Exit Criteria**: Baseline training reproducible, sweep infrastructure operational, and prioritized configuration set delivered to Evaluation Agent.

## Phase 6 – Evaluation & Analysis

### Evaluation Agent
- **Mission**: Reproduce paper metrics, maintain validation/testing splits, and certify model performance.
- **Core Responsibilities**:
  - Implement evaluation scripts under `src/eval/` capable of batch scoring, metric aggregation, and result serialization.
  - Ensure splits and scoring procedures match published methodology, documenting any deviations.
  - Integrate with Training Ops outputs (checkpoints, logs) and provide hooks for automated evaluation post-training.
  - Develop regression tests in `tests/eval/` that validate metric calculations on fixtures.
- **Deliverables**:
  - Evaluation scripts and metric utilities with documentation.
  - `docs/notes/evaluation-protocol.md` outlining datasets, metrics, statistical tests, and pass/fail thresholds.
  - Evaluation reports stored in `docs/notes/eval-reports/` (structured Markdown or notebooks exported to Markdown).
  - Execution logs archived in `.code/agents/evaluation/`.

### Insight Synthesizer Agent
- **Mission**: Aggregate experimental outcomes, craft narratives, and highlight insights or ablations worth reporting.
- **Core Responsibilities**:
  - Compile results from evaluation and sweeps into comparative tables, plots, and trend analyses.
  - Identify deviations from published baselines, explain root causes, and propose follow-up experiments.
  - Prepare publication-ready artifacts (charts, polished tables) consistent with documentation standards.
  - Collaborate with Docs Agent to ensure findings surface in READMEs, reports, or publication drafts.
- **Deliverables**:
  - `docs/notes/insight-digests/<date>.md` summarizing key takeaways, supporting charts stored under `docs/assets/`.
  - Slide decks or poster outlines if required (stored in `docs/communication/`).
  - Annotated datasets of metrics (CSV/JSON) for reproducibility.
  - Analytical notes in `.code/agents/insight_synthesizer/` referencing source evaluations.

### Collaboration Rhythm & Checkpoints
- **Metrics Review**: Evaluation agent shares checkpoint metrics; Insight Synthesizer drafts narratives and requests additional analyses as needed.
- **Publication Prep**: Align on figures/tables for external reporting; finalize before handing off to Docs Agent.
- **Exit Criteria**: Target metrics met or explained, insights documented, and recommendations routed to Director for next-phase planning.

## Phase 7 – Documentation & Operations

### Docs Agent
- **Mission**: Keep documentation, quickstarts, and ADRs current, ensuring contributors can onboard rapidly and audit decisions.
- **Core Responsibilities**:
  - Maintain `README.md`, quickstart guides, and `docs/notes/` summaries in sync with implementation progress.
  - Capture agent transcripts summaries in `docs/notes/` and coordinate with Director to archive `.code/agents/` artifacts once documented.
  - Curate changelog entries, release notes, and publication-ready documentation packages.
  - Review PRs for documentation consistency and provide style guidance per `.editorconfig` and project conventions.
- **Deliverables**:
  - Updated `README.md` sections (setup, usage, roadmap) plus any necessary `docs/notes/phase-*` summaries.
  - `docs/notes/changelog.md` covering milestones and notable changes.
  - Documentation QA checklist stored in `.code/agents/docs_agent/`.

### MLOps Agent
- **Mission**: Define operational readiness, CI/CD automation, and long-term maintenance practices for the project.
- **Core Responsibilities**:
  - Implement CI workflows (e.g., `.github/workflows/lint-test.yml`) invoking `make lint`, `make test`, dataset checksum verification, and security scans.
  - Create release packaging or model registry procedures, including artifact versioning and storage policies.
  - Establish monitoring/alerting hooks for productionized models, even if simulated (e.g., logging schema definitions, evaluation triggers).
  - Audit infrastructure/security considerations (dependency updates, supply-chain checks) and coordinate with Compliance on ongoing obligations.
- **Deliverables**:
  - CI configuration files and supporting scripts under `ci/` or `.github/`.
  - `docs/notes/mlops-readiness.md` outlining operational posture, maintenance schedule, and escalation paths.
  - Automation logs or design notes archived in `.code/agents/mlops_agent/`.

### Collaboration Rhythm & Checkpoints
- **Docs Sync**: Docs and MLOps agents align after major milestones to ensure documentation reflects operational realities.
- **Release Readiness Review**: Conduct checklists before releases (docs updated, CI passing, compliance sign-off) and capture outcomes in `docs/notes/release-checklist.md`.
- **Exit Criteria**: Documentation complete, CI pipelines green, archival/transcript processes finished, and project ready for ongoing maintenance.
