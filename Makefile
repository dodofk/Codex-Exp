PYTHON ?= python3
PYTHONPATH ?= src
DATASET ?= fleurs
CONFIG ?= config/ingestion/$(DATASET).json
ARGS ?=
HF_ARGS ?= --dataset facebook/covost2 --config en_fr --split train[:1%] --output data/raw/hf-demo

.PHONY: preprocess-plan preprocess-run

preprocess-plan:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m preprocess.cli config/preprocess/$(DATASET).json --plan

preprocess-run:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m preprocess.cli config/preprocess/$(DATASET).json
HF_ARGS ?= --dataset facebook/covost2 --config en_fr --split train[:1%] --output data/raw/hf-demo

.PHONY: queue-prefect-deploy queue-prefect-run

queue-prefect-deploy:
	@echo "Deploying flow ingest_preprocess_flow as auto-paper-ingest-preprocess/prod"
	uv run prefect work-pool create ingestion --type process || true
	uv run prefect deploy scripts/prefect_flows.py:ingest_preprocess_flow \
		--name auto-paper-ingest-preprocess/prod --pool ingestion

queue-prefect-run:
	@echo "Launching one-off Prefect run for dataset=$(DATASET)"
	uv run prefect deployment run auto-paper-ingest-preprocess/prod \
		--params '{"dataset":"$(DATASET)","config_path":"$(CONFIG)","preprocess_config":"config/preprocess/$(DATASET).json"}'

.PHONY: preprocess-plan preprocess-run

preprocess-plan:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m preprocess.cli config/preprocess/$(DATASET).json --plan

preprocess-run:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m preprocess.cli config/preprocess/$(DATASET).json

.PHONY: data-plan data-download data-verify

data-plan:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.cli $(CONFIG) --plan $(ARGS)

data-download:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.cli $(CONFIG) $(ARGS)

data-verify:
	@echo "Checksum verification baked into data-download; customize as needed."

.PHONY: hf-download

hf-download:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.hf_loader $(HF_ARGS)

.PHONY: worker-plan worker-run enqueue-demo

worker-plan:
	@echo '{"dataset":"$(DATASET)", "config_path":"$(CONFIG)"}' > /tmp/ingestion-payload.json
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.worker --payload /tmp/ingestion-payload.json --plan $(ARGS)

worker-run:
	@echo '{"dataset":"$(DATASET)", "config_path":"$(CONFIG)"}' > /tmp/ingestion-payload.json
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.worker --payload /tmp/ingestion-payload.json --run $(ARGS)

enqueue-demo:
	@echo '{"dataset":"$(DATASET)", "config_path":"$(CONFIG)", "artifacts":["README.md"]}' > /tmp/ingestion-payload.json
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.worker --payload /tmp/ingestion-payload.json --plan

.PHONY: hf-download

hf-download:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.hf_loader $(HF_ARGS)

.PHONY: telemetry-model-summary

telemetry-model-summary:
	uv run python scripts/model_telemetry_summary.py --log-dir data/logs/model --output data/telemetry/model_summary.json
