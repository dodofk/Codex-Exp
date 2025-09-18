# Sprint Backlog

## Sprint Summary
- **Sprint ID**: 2025-W38
- **Dates**: 2025-09-18 → 2025-09-29
- **Sprint Goal**: Maintain Phase 1 research resilience while launching Phase 2 dataset discovery toward shortlist + compliance readiness.
- **Velocity Target**: 26 points (Director, Data Scout, Compliance Steward, Research Curator, Lead Architect).

## Committed Work
| Item | Phase | Owner | Story Points | Status | Definition of Done |
|------|-------|-------|--------------|--------|--------------------|
| Catalogue top candidate corpora | Phase 2 | Data Scout Alpha | 5 | Complete | Landscape populated; shortlist summarized in `docs/notes/datasets/shortlist-summary.md` |
| Draft license & privacy cheat sheet | Phase 2 | Compliance Steward | 3 | Complete | Cheat sheet published; referenced in risk log |
| Build dataset landscape matrix skeleton | Phase 2 | Data Scout Alpha | 2 | Complete | Markdown table structure committed with placeholder columns |
| Schedule kickoff + capture notes | Phase 2 | Director | 2 | Complete | Kickoff agenda + notes appended to `.code/agents/director/` transcript |
| Create compliance risk log template | Phase 2 | Compliance Steward | 3 | Complete | `docs/notes/compliance/compliance-risk-log.md` created with initial entries |
| Define Phase 2 checkpoints & invitations | Phase 2 | Director | 2 | In Progress | Calendar invites sent; backlog updated with checkpoint tasks |
| Outline dataset manifest draft | Phase 2 | Data Scout Alpha | 3 | Complete | Manifest populated with storage estimates, checksum URLs, license conditions |
| Schedule legal review for MuST-C/VoxPopuli | Phase 2 | Compliance Steward | 2 | Complete | Meeting held 2025-09-18; outcomes logged |
| Refresh backup research papers | Phase 1 | Research Curator | 4 | Complete | 2 alternative papers appended to `docs/research/paper_matrix.csv` with viability notes |
| Align backup paper implications | Phase 1 ↔ Phase 2 | Lead Architect | 2 | In Progress | ADR addendum drafted covering fallback dataset paths |

## Daily Updates
| Date | Agent | What Happened | Blockers | Next Steps |
|------|-------|---------------|----------|-----------|
| 2025-09-18 | Director | Created sprint backlog, issued kickoff agenda, confirmed agent availability | None | Finalize rubric doc for review |
| 2025-09-18 | Director | Drafted Phase 3 kickoff agenda and W39 sprint shell | Pending legal outcomes before activating | Coordinate with Compliance & Eng leads post-meeting |
| 2025-09-18 | Director | Approved Phase 2 exit, activated Phase 3 kickoff + W39 sprint prep | None | Share roadmap update + kickoff invite |
| 2025-09-18 | Data Scout Alpha | Identified candidate source list (paper citations, Hugging Face, LDC) | Awaiting compliance cheat sheet for license tiers | Draft matrix columns and begin populating metadata |
| 2025-09-18 | Data Scout Alpha | Added CoVoST2, MuST-C v2, VoxPopuli, MLS, How2, AudioCaps, Clotho entries to landscape | Need storage estimates for How2 video component | Gather checksum info + start manifest outline |
| 2025-09-18 | Data Scout Alpha | Added storage estimates + checksum URLs to manifest; opened VoxPopuli/MuST-C transcripts | Waiting on confirmation of WikiMatrix checksum manifest | Validate links, continue manifest population for optional datasets |
| 2025-09-18 | Data Scout Alpha | Drafted shortlist scoring rubric and saved at `docs/notes/datasets/shortlist-rubric.md` | Need compliance input on weighting license risk | Apply rubric during shortlist checkpoint prep |
| 2025-09-18 | Data Scout Alpha | Applied rubric scores (FLEURS 16, CoVoST 15, MLS 14, MuST-C/VoxPopuli 12, optional datasets 11) | Need Director sign-off on shortlist | Prep Checkpoint #1 deck with scores + rationale |
| 2025-09-18 | Data Scout Alpha | Published shortlist summary with top four datasets + reserves (`docs/notes/datasets/shortlist-summary.md`) | Await Checkpoint #1 approval | Coordinate with Director for review session |
| 2025-09-18 | Compliance Steward | Reviewed Phase 1 ADR; outlined compliance artifacts required | Needs dataset list from Data Scout | Draft cheat sheet structure and risk log headings |
| 2025-09-18 | Compliance Steward | Published licensing cheat sheet and populated risk log for new datasets | Awaiting legal input on MuST-C ND clause, VoxPopuli SA | Schedule consult with legal; draft outreach summary |
| 2025-09-18 | Compliance Steward | Drafted legal brief for MuST-C/VoxPopuli review (agenda + questions) | Need confirmation of meeting slot | Send invite, log outcomes in compliance risk log |
| 2025-09-18 | Compliance Steward | Confirmed legal consult for 2025-09-20 10:00 PT; shared pre-read packet | Awaiting counsel feedback post-meeting | Capture decisions in risk log + readiness report draft |
| 2025-09-18 | Compliance Steward | Held legal session; cleared MuST-C (internal use) & VoxPopuli (share-alike) with documented restrictions | Need to propagate notices to manifest/README | Update readiness report & close compliance tasks |
| 2025-09-18 | Research Curator | Re-opened paper search notebook, confirming availability of secondary datasets | Pending director guidance on priority taxonomy | Refresh two candidate papers and update matrix |
| 2025-09-18 | Research Curator | Added SpeechCLIP & CLAP rows to `paper_matrix.csv`; drafted Phase 1 summary update | Need confirmation on metric targets from Lead Architect | Review ADR addendum outline once available |
| 2025-09-18 | Lead Architect | Coordinated with Curator on fallback architecture considerations | Requires updated paper matrix | Draft ADR addendum outline |
| 2025-09-18 | Lead Architect | Created ADR-001 primary paper decision doc linking baseline metrics and dataset priorities | Need legal confirmation before finalizing fallback scopes | Extend ADR addendum with compliance dependencies |
| 2025-09-18 | Lead Architect | Drafted ADR-002 fallback architecture plan pending legal guidance | Await compliance meeting results | Update roadmap once decision finalized |

## Blockers & Risks
| Description | Owner | Impact | Mitigation | Status |
|-------------|-------|--------|------------|--------|
| Access to LDC catalog may require two-week approval | Compliance Steward | High | Submit request immediately; explore Common Voice + VoxPopuli backups | Open |
| Unclear checksum hosting for older corpora | Data Scout Alpha | Medium | Contact dataset maintainers; plan to generate checksums post-ingestion | Monitoring |

## Retrospective Notes
- **Went Well**: Backlog structured before kickoff, agents confirmed roles.
- **To Improve**: Need clearer responsibility split for license escalations versus technical gating.
- **Experiments**: Trial async daily updates via sprint backlog instead of chat pings.

## Backlog Candidates
- Stand up additional Data Scout (regional focus) if shortlist lacks low-resource coverage.
- Evaluate automate-download PoC ahead of Phase 3 to de-risk API rate limiting.
- Prepare template for dataset manifest JSON export for future automation.
