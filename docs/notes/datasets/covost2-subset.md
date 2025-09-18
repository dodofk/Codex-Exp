# CoVoST 2 Subset Plan

- **Goal**: ingest only the English→French split for prototyping due to limited storage.
- **Approach**:
  1. Create a config (e.g., `config/ingestion/covost2-en-fr.json`) listing only the
     desired tarballs.
  2. Use the Make target with `ARGS="--artifact <filename>"` to fetch a single
     archive or checksum file at a time.
- **Example**:
  ```bash
  make data-download DATASET=covost2 ARGS="--artifact README.md"
  ```
  Replace `README.md` with the actual tarball (e.g., `train_en_fr.tar.gz`) once
  ready; checksum values should come from the official manifest.

Track additional subset manifests here as they are curated.
