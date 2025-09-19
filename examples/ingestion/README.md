# Ingestion Examples

Quick command references for running the Phase 3 ingestion tooling.

## FLEURS five-language subset

1. Inspect the download plan (safe, no network writes):
   ```bash
   PYTHONPATH=src python -m ingestion.cli config/ingestion/fleurs_dev.json --plan
   ```

2. Download the artifacts defined in `fleurs_dev.json`:
   ```bash
   PYTHONPATH=src python -m ingestion.cli config/ingestion/fleurs_dev.json
   ```

3. Run through the worker wrapper (mirrors queue behaviour):
   ```bash
   PYTHONPATH=src python -m ingestion.worker --payload-json '{"dataset":"fleurs","config_path":"config/ingestion/fleurs_dev.json"}' --run
   ```

   Or use the helper script (plans by default, add `--plan` to skip download):
   ```bash
   PYTHONPATH=src python scripts/enqueue_ingestion.py fleurs --config config/ingestion/fleurs_dev.json
   ```

Environment variables required for protected datasets are documented in
`.env.ingestion.example`. Copy it to `.env.ingestion`, populate the values you
need, and keep the file out of version control.

## Hugging Face subset helper (CoVoST 2 example)

Pull a small English→French slice via the Hugging Face loader:

```bash
make hf-download \
  HF_ARGS="--dataset facebook/covost2 --config en_fr --split train[:1%] --output data/raw/covost2/en_fr_subset"
```

The `make hf-download` target wraps `python -m ingestion.hf_loader` and will
respect any credentials exposed through `.env.ingestion`.
