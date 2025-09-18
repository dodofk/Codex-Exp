# Dataset Landscape

| Dataset | Phase | Modality | Languages | Size (hrs/utt) | Splits Available | License | Checksums Published | Download Source | Notes / Known Pitfalls | Risk Flags | License Score | Modality Score | Language Score | Quality Score | Accessibility Score | Privacy Score | Total |
|---------|-------|----------|-----------|----------------|------------------|---------|---------------------|-----------------|------------------------|-----------|---------------|----------------|----------------|---------------|------------------|---------------|-------|
| FLEURS / XTREME-S | 2 | Speech ↔ Text | 102 (21 train focus) | ≈12 hrs/lang | train/dev/test | CC-BY 4.0 | Yes (per language tarballs) | Hugging Face `google/fleurs`, TFDS `xtreme_s` | Read speech; mismatch vs. noisy domains; large disk footprint (~350 GB) | License attribution required; review regional consent terms | 3 | 3 | 3 | 2 | 2 | 3 | 16 |
| CoVoST 2 | 2 | Speech ↔ Text | 21 source, 15 target | ≈430 hrs total | train/valid/test | CC0 (public domain) | Hashes via HF dataset card | Hugging Face `facebook/covost2` | Derived from Common Voice; varying audio quality | Confirm speaker consent scope; ensure CC0 compliance | 3 | 3 | 2 | 2 | 2 | 3 | 15 |
| MuST-C v2 | 2 | Speech ↔ Text | 14 | ≈2500 hrs total | train/dev/test | CC BY-NC-ND 4.0 | Yes (per release tarball) | FBK `https://ict.fbk.eu/must-c` | Non-commercial clause; talk transcripts may include disfluencies | Non-commercial restriction; derivative limitations | 1 | 3 | 2 | 3 | 1 | 2 | 12 |
| VoxPopuli | 2 | Speech ↔ Text | 23 | ≈4000 hrs total | train/dev/test | CC BY-SA 4.0 | Provided (md5) | Hugging Face `facebook/voxpopuli` | Parliamentary data; long recordings; large storage (≈1.8 TB) | Share-alike obligations; parliamentary privacy review | 1 | 3 | 2 | 3 | 1 | 2 | 12 |
| Multilingual LibriSpeech | 2 | Speech ↔ Text | 8 | ≈45 hrs/lang | train/dev/test | Public domain (LibriVox) | Yes (official release) | OpenSLR `https://openslr.org/94/` | Derived from audiobooks; accent variety limited | Verify redistribution terms; check speaker attribution | 3 | 2 | 2 | 2 | 2 | 3 | 14 |
| How2 / How2QA | 2 | Video + Speech ↔ Text | 2 (en/es) | ≈79k clips (~300 hrs) | train/dev/test | CC BY 4.0 | Provided (md5) | LDC & How2 repo | YouTube-derived; video download quotas | Potential TOS takedown; ensure captions comply | 2 | 3 | 1 | 2 | 1 | 2 | 11 |
| AudioCaps | 2 | Audio ↔ Text | en | 46k clips (~46 hrs) | train/val/test | CC BY 4.0 | Provided (csv hashes) | AudioSet subset via KU Leuven | Contains environmental sounds; relies on YouTube IDs | YouTube availability risk; minors in audio? | 2 | 2 | 1 | 2 | 2 | 2 | 11 |
| Clotho v2 | 2 | Audio ↔ Text | en (captions) | 6974 clips (~15 hrs) | dev/val/eval | CC BY 4.0 | Provided (md5) | Zenodo `https://zenodo.org/record/4783391` | Crowdsourced captions; limited clip length | Verify consent statements; evaluate crowdworker privacy | 2 | 2 | 1 | 2 | 2 | 2 | 11 |

## Research Log
- 2025-09-18: Data Scout Alpha drafted initial column schema and source list.
- 2025-09-18: Data Scout Alpha logged FLEURS baseline entry and verified CC-BY license.
- 2025-09-18: CoVoST 2, MuST-C v2, VoxPopuli, Multilingual LibriSpeech, How2, AudioCaps, Clotho profiled with preliminary metadata.
- 2025-09-18: Applied shortlist scoring rubric; total scores added for quick ranking (FLEURS 16, CoVoST 2 15, MLS 14, MuST-C 12, VoxPopuli 12, optional sets 11).
- 2025-09-18: Shortlist summary published (`docs/notes/datasets/shortlist-summary.md`) for Checkpoint #1 review.
- 2025-09-18: Added storage size estimates and checksum source URLs to dataset manifest.
