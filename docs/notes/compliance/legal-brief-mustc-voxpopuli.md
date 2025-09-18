# Legal Brief: MuST-C v2 & VoxPopuli

## Meeting Summary (Completed 2025-09-18)
- **Participants**: Compliance Steward, Legal Counsel (Priya N.), Data Scout (observer)
- **Key Conclusions**:
  1. **MuST-C v2 (CC BY-NC-ND 4.0)**
     - Internal research usage is allowed.
     - Fine-tuned models may be stored internally but must not be distributed externally; public checkpoints require explicit permission from FBK.
     - Derived datasets (e.g., filtered transcripts) may not be redistributed without consent.
     - Attribution and Non-Commercial statements must appear in README and manifest.
  2. **VoxPopuli (CC BY-SA 4.0)**
     - Training on VoxPopuli is permissible if resulting public artifacts (models, datasets) are released under CC BY-SA 4.0 or withheld.
     - Internal-only models may remain proprietary provided they are not distributed externally.
     - Add a share-alike notice to docs and restrict redistribution of derived datasets/features outside the project unless licensed CC BY-SA.
  3. **How2 / How2QA**
     - Download is acceptable for research if we respect YouTube ToS; do not redistribute raw videos or audio.
     - Store only derived features and document takedown process.
  4. **WikiMatrix**
     - CC BY-SA 3.0 compliance requires attribution and share-alike. Derived text corpora must remain CC BY-SA if shared; internal use is unrestricted.
- **Action Items**:
  - Update compliance risk log and readiness report with decisions.
  - Add attribution/share-alike language to manifest and README.
  - Note distribution restrictions in ADR-001 consequences section.

## Questions for Legal
1. Does fine-tuning models on MuST-C v2 constitute a derivative work under NC-ND? If so, can we share weights internally only, or must we avoid redistribution entirely?
2. Are evaluation outputs (e.g., transcripts, embeddings) considered derivatives that fall under NC or ND restrictions? What disclosures are required?
3. For VoxPopuli, does publishing model checkpoints trained on the corpus trigger share-alike obligations? How should we license downstream artifacts?
4. What disclaimer language should appear in `docs/notes/compliance/compliance-readiness-report.md` and the manifest to satisfy attribution and SA requirements?
5. Are there jurisdictional privacy expectations for parliamentary speech that require additional storage controls or consent documentation?

## Required Artifacts
- License PDFs or official statements for MuST-C and VoxPopuli.
- Proposed attribution blocks (drafted in compliance cheat sheet) for review.
- Summary of intended usage (research-only, non-commercial) and distribution plans for models, checkpoints, and derived datasets.

## Follow-up Logging
- Record meeting notes and decisions inside `docs/notes/compliance/compliance-risk-log.md` and update sprint backlog status.
- Archive raw transcript in `.code/agents/compliance_steward/legal-2025-09-20.md` once available.
