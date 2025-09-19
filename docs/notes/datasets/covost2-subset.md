# CoVoST 2 Subset Plan

- **Goal**: ingest only the English→French split for prototyping due to limited storage.
- **Approach**:
  1. Use the Hugging Face loader to materialize the split slice:
     ```bash
     make hf-download HF_ARGS="--dataset facebook/covost2 --config en_fr --split train[:1%] --output data/raw/covost2/en_fr_subset"
     ```
  2. For raw HF files, create a config (e.g., `config/ingestion/covost2-en-fr.json`) listing only the
     desired tarballs and use `make worker-run DATASET=covost2 ARGS="--artifact <filename>"`.
- **Example**:
  ```bash
  make data-download DATASET=covost2 ARGS="--artifact README.md"
  ```
  Replace `README.md` with the actual tarball (e.g., `train_en_fr.tar.gz`) once
  ready; checksum values should come from the official manifest.

Track additional subset manifests here as they are curated.
