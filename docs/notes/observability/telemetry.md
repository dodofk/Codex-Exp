# Telemetry & Observability Notes

## Local Logging
- Ingestion, Hugging Face loader, and preprocessing write events to
  `data/raw/<dataset>/logs/events.jsonl` and `telemetry.jsonl`.
- `scripts/telemetry_aggregate.py` summarizes counts for dashboards.

## OpenTelemetry Stubs
- Set `OTEL_EXPORTER_CONSOLE=1` to mirror events to stdout (batched spans via
  console exporter). Future work: replace with OTLP exporter to Cloud Logging or ELK.
- `telemetry.exporter.init_tracer(service_name="auto-paper")` hooks can be called from
  worker start-up scripts to push spans if OpenTelemetry libs are present.

## Next Steps
- Wire console exporter output into log shipper (Fluent Bit / filebeat).
- Define alert thresholds (e.g., ingestion failures >0, preprocess duration >1h).
- Create Grafana dashboard sourcing aggregated events from log pipeline.
