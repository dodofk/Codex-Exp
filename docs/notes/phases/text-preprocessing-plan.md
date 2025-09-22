# Text Preprocessing Plan (Normalization & Tokenization)

- **Status**: Draft v0.1
- **Last Updated**: 2025-09-19
- **Owner**: Preprocess Engineer
- **Due Date**: 2025-09-26
- **Related Work**: `docs/notes/phases/preprocess-spec.md`, Sprint Backlog W39, ADR-001 (token compatibility)

## Objectives
- Deliver deterministic text normalization across supported corpora (FLEURS, CoVoST 2, MuST-C, VoxPopuli, WikiMatrix) to align with audio pipeline lineage.
- Produce SentencePiece tokenizers aligned with ADR-001 (PaLM-compatible vocabulary/unk conventions) and fallback ADR-002.
- Package normalized transcripts, vocabulary metadata, and tokenizer artifacts in `data/processed/<dataset>/<version>/text/` with lineage coverage.
- Ship regression tests and CLI/worker integration hooks so text jobs run alongside audio preprocessing by 2025-09-26.

## Scope & Assumptions
- Includes supervised/ASR transcripts, MT targets, and bilingual corpora already cleared in the dataset manifest.
- Excludes multilingual LM pretraining corpora not in manifest, detokenization for evaluation, and morphology heuristics beyond Unicode & punctuation rules.
- Assume SentencePiece (v0.1.99+) available via existing requirements; no GPU required for tokenizer training.
- Coordination with ingestion team for transcript path conventions (`data/raw/<dataset>/<lang>/<split>/transcript.*`).

## Data Inventory & Coverage

| Dataset | Text Source | Languages (priority) | Notes |
|---------|-------------|----------------------|-------|
| FLEURS | Prompt + answer transcripts | 102 languages, primary focus on en, fr, de, es, zh, hi, id | Balanced prompts; mixed scripts; includes accent marks. |
| CoVoST 2 | Crowd-sourced translations aligned to Common Voice | 21 source → 15 target languages; prioritize en→de/fr/es/zh, de→en | Lower-case bias; inconsistent punctuation. |
| MuST-C v2 | TED talk subtitles | 8 translation pairs (en→xx) | Contains markup (`<unk>`, appl.) and time stamps. |
| VoxPopuli | Parliamentary transcripts | 15 EU languages | Formal register; numbers + abbreviations. |
| WikiMatrix | Sentence-aligned Wikipedia pairs | 85+ pairs, focus on en↔fr/de/es/zh/hi | Variation in whitespace and wiki markup remnants. |

## Normalization Strategy

### Core Pipeline (applies to all languages)
- Unicode normalization to NFC followed by compatibility casefold where approved (skip for scripts where casing not defined).
- Strip control characters and BOM, collapse internal whitespace to single spaces, and canonicalize newlines to `\n`.
- Normalize punctuation via mapping table (curly quotes → straight, ellipsis → `...`, em dash → ` — ` policy) maintained in `config/normalize/punctuation.json`.
- Expand ASCII fractions and standardize numeric separators (`,` vs `.`) via locale-aware rules.
- Preserve language tags and markup required for alignment; drop residual HTML entities through `html.unescape`.

### Language-Specific Overlays
- Build per-language rule sets in `config/normalize/<lang>.yaml` covering:
  - Script-specific spacing (e.g., remove spaces before Japanese punctuation, enforce thin spaces in French optional).
  - Accent retention policy (retain diacritics; only strip if dataset variant mixes accentless duplicates, log warnings).
  - Token-preserving substitutions (e.g., `l'` contractions in French, Hindi Nukta normalization).
- Provide dataset-specific hooks to excise ingestion artifacts (MuST-C `<unk>`, `[MUSIC]`, `[APPLAUSE]`; CoVoST language codes in CSV headers).
- Document rule precedence: dataset overrides language overrides core.

### Implementation Tasks
1. `src/preprocess/text_normalizer.py`: pure-Python pipeline (generators) implementing core + overlay rules with `NormaliseOptions` dataclass.
2. Extend `PreprocessConfig` to accept `text_input_glob`, `text_output_format`, and ordered `text_steps` (list of step configs akin to audio).
3. CLI additions: `preprocess text-plan <config>` to print normalization decisions; `preprocess run --text-only` flag for workers.
4. Introduce lineage entries (`step="text_normalize"`) capturing rule hashes, original checksum, and character deltas.
5. Add sample configs (`config/preprocess/fleurs_text.json`, `covost2_text.json`) referencing shared rule files.

## Tokenization Strategy

### Model Selection
- SentencePiece BPE with 32k vocab for high-resource languages; 8k–16k for low-resource to prevent over-segmentation.
- Shared multilingual model for families needing code-switch handling: e.g., single model for Romance languages (`en/fr/es/it/pt`) and one for Indic languages (`hi/te/ta`) pending Unicode overlap analysis.
- Configure `<unk>`, `<s>`, `</s>` IDs to match ADR-001 (0,1,2), ensure compatibility with existing feature consumers.

### Training Pipeline
- Script `scripts/train_sentencepiece.py`: accepts normalized corpus glob(s), vocab size, model prefix, and optional character coverage.
- Stage training data in `data/interim/<dataset>/normalized/*.txt` to isolate deterministic snapshots (sorted, one sentence per line, deduped).
- Enforce reproducibility: set `sentencepiece.SentencePieceTrainer.SetRandomGeneratorSeed(20250919)` and version metadata in model.
- Store outputs under `artifacts/tokenizers/<dataset>/<lang>/` with `.model`, `.vocab`, checksum manifest, and README snippet.
- Register artifact metadata in `docs/notes/phases/tokenizer-inventory.md` (new file, follow manifest style) for future audits.

### Integration & Usage
- Update `src/preprocess/pipeline.py` (or new `text_pipeline.py`) to optionally tokenize normalized files, emitting token ID arrays serialized to `.npz` or `.jsonl` with `tokens` and `attention_mask` fields.
- Provide Python helper `encode_text_batch` exposing `SentencePieceProcessor` with caching for worker reuse.
- Ensure workers can queue `text_tokenize` jobs post-normalization via Prefect flow; workspace-run will schedule after audio completes to reuse ingestion metadata.

## Directory & Artifact Layout
- Normalized transcripts: `data/processed/<dataset>/<version>/text/<lang>/<split>.normalized.jsonl`
  - Each line: `{ "id": str, "text": str, "lang": str, "source": str, "normalized": bool, "rules_version": str }`
- Token IDs: `data/processed/<dataset>/<version>/text/<lang>/<split>.tokens.npz`
- Tokenizer models: `artifacts/tokenizers/<dataset>/<lang>/<model_name>.model`
- Lineage: `data/processed/<dataset>/<version>/lineage.jsonl` entries for normalization + tokenization with rule hash/vocab hash.

## Testing & Validation Plan
- Unit tests (`tests/preprocess/test_text_normalizer.py`) covering core rules, language overrides, and dataset edge cases with golden fixtures.
- Property-based fuzz tests via Hypothesis to guarantee idempotence (`normalise(normalise(x)) == normalise(x)`) and whitespace invariants.
- Tokenizer smoke test (`tests/preprocess/test_tokenizer_training.py`) that trains on miniature corpus and validates vocabulary size, reserved IDs, and deterministic output.
- Integration test hooking into CLI: run `uv run preprocess run --config config/preprocess/fleurs_text.json --limit 5` in CI once text artifacts stored locally (guarded by mark `@pytest.mark.text`).
- Validation metrics logged to `logs/text/` summarizing character deltas, OOV rate pre/post tokenization, and sentence count parity with raw corpus.

## Observability & Compliance
- Extend telemetry schema to capture normalization warnings (e.g., stripped control chars, unresolved HTML entities) with counts per language.
- Compliance hooks: redact inline PII patterns before normalization (delegate to `compliance.filters` module when available) and record counts in lineage metadata.
- Ensure manifests/README include updated license notices when normalized text stored (e.g., CoVoST attribution requirement).

## Milestones & Timeline
- **2025-09-20**: Finalize rule inventory & punctuation map; stub config files committed.
- **2025-09-22**: Implement normalizer library + unit tests; sample run on FLEURS (en/fr) stored under `data/processed/fleurs/dev/text/`.
- **2025-09-24**: Deliver tokenizer training script + deterministic smoke test; produce draft artifact for FLEURS English.
- **2025-09-25**: Wire CLI/worker integration and lineage logging; update documentation.
- **2025-09-26**: Complete regression suite, publish tokenizer inventory doc, handoff demo of ingest→normalize→tokenize flow.

## Risks & Mitigations
- **Non-Latin scripts handling**: risk of incorrect spacing (Thai, Chinese). → Validate with linguist consultant; add dataset-specific tests using community samples.
- **Tokenizer drift**: incremental dataset updates could change models. → Require frozen corpora snapshot and checksum gating before retraining.
- **Performance**: SentencePiece training slow for >10M sentences. → Batch by language, reuse tokenizers, and parallelize with existing Prefect flow using chunked corpora.
- **Library availability**: sentencepiece wheel often missing on ARM runners. → Build from source in CI container and cache wheel; fallback to Docker training if needed.

## Open Questions
- Should we ship shared multilingual tokenizer or language-specific for all corpora? Need model consumers decision by 2025-09-21.
- Do we retain casing for tasks requiring truecasing (e.g., MuST-C)? Consider feature flag per dataset.
- What storage quota applies to tokenizer artifacts in `artifacts/`? Ops to confirm budget before 2025-09-24.
- Alignment with downstream evaluation: do we export detokenized text for BLEU scripts? Pending response from evaluation team.
