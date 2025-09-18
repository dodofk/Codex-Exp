# Licensing & Privacy Cheat Sheet

## Creative Commons Overview
- **CC0 (Public Domain)** – No restrictions; attribution optional. Confirm volunteer consent (e.g., CoVoST 2 via Common Voice) and scrub incidental PII before storage.
- **CC-BY 4.0** – Requires attribution and link to license. Applicable to FLEURS, How2, AudioCaps, Clotho. Include attribution block in README, dataset manifest, and compliance report.
- **CC-BY-SA 4.0** – Attribution plus share-alike. VoxPopuli derivatives (features, models) must carry the same license or clearly identify non-distributable artifacts. Document redistribution scope.
- **CC-BY-NC-ND 4.0** – Attribution, non-commercial, and no-derivatives. MuST-C outputs limited to research; clarify whether fine-tuned models or redistributed features are considered derivatives. Engage legal before external sharing.

## Other Data Sources
- **Public Domain (LibriVox)** – Multilingual LibriSpeech assets are PD; still respect narrator credit and confirm PD statements in docs.
- **YouTube-Derived Content (How2, AudioCaps)** – Even with CC licenses, comply with YouTube Terms of Service. Avoid reposting raw video/audio; cache derived features, track takedown requests, and include contact path for removals.
- **Parliamentary Proceedings (VoxPopuli)** – Political sensitivity; note jurisdictional privacy expectations. Ensure metadata filters remove personal addresses or incidental PII.

## Privacy & Mitigation Checklist
- Hash or replace speaker identifiers before ingestion (`data/raw/<dataset>/metadata`).
- Maintain consent documentation links inside `docs/notes/compliance/compliance-risk-log.md`.
- Capture storage location & encryption requirements per dataset in the forthcoming manifest.
- Document approvals or legal consultations in `.code/agents/compliance_steward/` with timestamps.

## Attribution Template (CC-BY / CC-BY-SA)
```
Dataset: <Name>
Source: <URL>
License: CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
© Original contributors. This project uses the data for research purposes only.
```
Adjust license URL and clauses (SA, NC-ND) as needed.
