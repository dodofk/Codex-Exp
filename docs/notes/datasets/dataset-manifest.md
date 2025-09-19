# Dataset Manifest (Draft)

| Dataset | Status | Storage Path | Checksum Source | License & Attribution | Preprocessing Notes | Owner |
|---------|--------|--------------|-----------------|-----------------------|---------------------|-------|
| FLEURS / XTREME-S | Proposed | `data/raw/fleurs` (~280 GB) | https://huggingface.co/datasets/google/fleurs#data-fields | CC-BY 4.0 — “© Google LLC, used under CC-BY 4.0.” Include link in README + manifest. | Per-language resampling to 16 kHz; tokenize transcripts via sentencepiece | Data Scout |
| CoVoST 2 | Discovering | `data/raw/covost2` (~120 GB) | https://huggingface.co/datasets/facebook/covost2#data-fields (`checksums.tsv`) | CC0 — reference Mozilla Common Voice contributor statement; scrub incidental PII. | Normalize punctuation, map accents; align with FLEURS language codes | Data Scout |
| Multilingual LibriSpeech | Approved | `data/raw/mls` (~160 GB) | https://www.openslr.org/94/ (MD5 list) | Public Domain — attribute narrators; retain PD notice in downstream artifacts. | Segment long chapters; verify speaker metadata | Data Scout |
| MuST-C v2 | Approved (internal-only) | `data/raw/mustc` (~500 GB) | https://ict.fbk.eu/must-c/ (MD5 list) | CC BY-NC-ND 4.0 — internal research only. Attribution: “© FBK. Licensed CC BY-NC-ND 4.0.” No external model release. | Chunk long TED talks, diarize speakers, filter applause | Compliance Steward |
| VoxPopuli | Approved (share-alike) | `data/raw/voxpopuli` (~1.8 TB) | https://huggingface.co/datasets/facebook/voxpopuli#data-fields | CC BY-SA 4.0 — add notice: “Derived artifacts must be released under CC BY-SA 4.0 or kept internal.” | Segment to ≤30s clips; anonymize metadata before storage | Compliance Steward |
| WikiMatrix | Approved | `data/raw/wikimatrix` (~90 GB) | https://github.com/facebookresearch/LASER/tree/main/tasks/WikiMatrix (SHA1) | CC-BY-SA 3.0 — attribute Wikimedia contributors; enforce share-alike on redistributed subsets. | Language pair filtering; deduplicate overlaps with training corpora | Data Scout |
| How2 / How2QA | Approved (features-only) | `data/raw/how2` | Project-provided MD5 list | CC-BY 4.0 + YouTube Terms — attribute creators and respect takedown requests; do not redistribute raw video/audio. | Download captions/audio features only; no raw video storage | Data Scout |
| AudioCaps | Approved (features-only) | `data/raw/audiocaps` | Dataset CSV MD5 fields | CC-BY 4.0 — cite KU Leuven & annotators; track YouTube removals. | Cache embeddings only; handle missing YouTube clips | Data Scout |
| Clotho v2 | Approved | `data/raw/clotho` | Zenodo checksum manifest | CC-BY 4.0 — attribute Tampere University; note crowdworker consent. | Standardize sample rate; align with AudioCaps taxonomy | Data Scout |

> Note: Complete all sections before Phase 2 checkpoint #3. Extend table as additional datasets are approved.
