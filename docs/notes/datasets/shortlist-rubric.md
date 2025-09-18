# Dataset Shortlist Rubric (Phase 2)

| Criterion | Description | Scoring (0–3) | Notes |
|-----------|-------------|---------------|-------|
| License & Compliance | Alignment with CC0/CC-BY; presence of NC/SA clauses; ease of approval | 0 = blocked; 3 = fully permissive | Compliance Steward to annotate per dataset |
| Modality Coverage | Relevance to cross-modal/cross-lingual retrieval tasks | 0 = unrelated; 3 = direct match | Data Scout to note modality gaps |
| Language Overlap | Overlap with target evaluation languages (FLEURS, CoVoST, WikiMatrix) | 0 = none; 3 = strong overlap | Reference dataset manifest |
| Data Quality & Size | Availability of clean splits, metadata, and sufficient hours/pairs | 0 = insufficient; 3 = robust | Include storage estimates, checksum status |
| Accessibility & Tooling | Ease of download, checksum availability, mirrors, rate limits | 0 = blocked; 3 = smooth | Capture ingestion considerations |
| Privacy & PII Risk | Presence of speaker IDs, minors, sensitive content | 0 = high risk; 3 = low risk | Compliance log to inform score |

## Usage
- Each dataset receives a 0–3 score per criterion; aggregate to rank candidates for Checkpoint #1.
- Record scores in `docs/notes/datasets/dataset-landscape.md` (add columns as needed) and summarize rationale in `.code/agents/data_scout/` transcripts.
- Compliance Steward reviews final scores before Checkpoint #2 to ensure mitigations align with risk tolerance.
