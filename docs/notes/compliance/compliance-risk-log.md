# Compliance Risk Log

| Dataset | License Summary | Privacy Considerations | Mitigation Actions | Approvals Required | Owner | Status | Notes |
|---------|-----------------|------------------------|--------------------|-------------------|-------|--------|-------|
| FLEURS / XTREME-S | CC-BY 4.0; requires attribution to Google | Metadata includes anonymized speaker IDs; multilingual voice data | Enforce attribution in docs; hash speaker IDs; monitor regional consent clauses | None | Compliance Steward | Mitigated | License text: https://huggingface.co/datasets/google/fleurs |
| CoVoST 2 | CC0 public domain; derived from Common Voice | Includes volunteer voice data; accents may reveal identity | Reiterate volunteer consent, scrub incidental PII in metadata | None | Compliance Steward | Mitigated | Dataset card: https://huggingface.co/datasets/facebook/covost2 |
| MuST-C v2 | CC BY-NC-ND 4.0 (non-commercial, no derivatives) | TED talks include named speakers; transcripts share quotes | Internal research only; no external release of fine-tuned models/datasets without FBK approval; include NC-ND attribution | None (legal cleared 2025-09-18) | Compliance Steward | Mitigated | License PDF: https://ict.fbk.eu/must-c/ |
| VoxPopuli | CC BY-SA 4.0 (share alike) | Parliamentary speech; may contain sensitive political data | Allow internal use; external artifacts must inherit CC BY-SA or be withheld; add SA notice and privacy disclaimer | None (legal cleared 2025-09-18) | Compliance Steward | Mitigated | HF card: https://huggingface.co/datasets/facebook/voxpopuli |
| Multilingual LibriSpeech | Public domain (LibriVox) | Audiobook readers named; minimal PII | Attribute narrators when available; confirm PD statements | None | Compliance Steward | Mitigated | OpenSLR entry: https://openslr.org/94/ |
| How2 / How2QA | CC BY 4.0 (video + text) + YouTube ToS | YouTube content may contain personal data | Download captions/audio features only; respect takedown requests; no redistribution of raw video/audio | None (legal cleared 2025-09-18) | Compliance Steward | Mitigated | Project page: https://github.com/srvk/how2-dataset |
| AudioCaps | CC BY 4.0 (annotations) + YouTube | Relies on YouTube audio; potential minors | Cache derived features; track removal requests; sanitize metadata | None | Compliance Steward | Mitigated | Dataset info: https://audiocaps.github.io/ |
| Clotho v2 | CC BY 4.0 (audio + captions) | Crowdsourced audio may include background speech | Confirm consent statements; align captions with privacy policy | None | Compliance Steward | Mitigated | Zenodo record: https://zenodo.org/record/4783391 |
| WikiMatrix | CC-BY-SA 3.0 | Synthetic alignments; translation noise | Attribution + share-alike for any redistributed subsets; internal use unrestricted | None (legal cleared 2025-09-18) | Compliance Steward | Mitigated | LASER repo |

- 2025-09-18: Confirm whether LDC datasets demand secure enclave storage.
- 2025-09-18: Validate whether FLEURS CC-BY permits model redistribution in downstream demos.
