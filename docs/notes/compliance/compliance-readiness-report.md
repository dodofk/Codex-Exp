# Compliance Readiness Report (Draft)

## Summary
- **Status**: Legal review completed 2025-09-18; all datasets approved with documented restrictions.
- **Approved Datasets**: FLEURS, CoVoST 2, Multilingual LibriSpeech, MuST-C v2 (internal-only distribution), VoxPopuli (share-alike condition), How2/How2QA (features only), WikiMatrix, AudioCaps, Clotho.
- **Action Required**: Add attribution/share-alike language to manifest & README; enforce internal-use restrictions where noted.

## Dataset Compliance Table
| Dataset | License | Decision | Mitigations | Notes |
|---------|---------|----------|-------------|-------|
| FLEURS | CC-BY 4.0 | Approved | Attribution in docs/manifest | None |
| CoVoST 2 | CC0 | Approved | Confirm volunteer consent statement | Maintain PII scrub |
| Multilingual LibriSpeech | Public Domain | Approved | Attribute narrators | Verify PD status |
| MuST-C v2 | CC BY-NC-ND 4.0 | Approved (internal-only) | Restrict distribution of models/datasets; include NC-ND notice | External sharing requires FBK agreement |
| VoxPopuli | CC BY-SA 4.0 | Approved with conditions | Add share-alike notice; release artifacts under CC BY-SA or keep internal | Include privacy disclaimer in docs |
| How2 / How2QA | CC-BY + YouTube ToS | Approved with conditions | Download captions/audio features; respect takedown requests | No raw video/audio distribution |
| WikiMatrix | CC-BY-SA 3.0 | Approved with conditions | Attribute and apply share-alike to redistributed subsets | Align manifest with SA notice |
| AudioCaps | CC-BY 4.0 | Approved | Handle missing YouTube clips | Monitor removal requests |
| Clotho v2 | CC-BY 4.0 | Approved | Verify consent statements | Align with AudioCaps taxonomy |

## Next Steps
- Record legal meeting outcomes (MuST-C, VoxPopuli) and update decisions column accordingly.
- Finalize attribution block for approved datasets (use cheat sheet template).
- Coordinate with Data Scout to ensure manifest reflects compliance statuses.
- Archive legal meeting transcript in `.code/agents/compliance_steward/`.
