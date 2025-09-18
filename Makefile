PYTHON ?= python3
PYTHONPATH ?= src
DATASET ?= fleurs
CONFIG ?= config/ingestion/$(DATASET).json
ARGS ?=

.PHONY: data-plan data-download data-verify

data-plan:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.cli $(CONFIG) --plan $(ARGS)

data-download:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ingestion.cli $(CONFIG) $(ARGS)

data-verify:
	@echo "Checksum verification baked into data-download; customize as needed."
