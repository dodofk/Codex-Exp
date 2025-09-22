#!/usr/bin/env bash
set -euo pipefail

# Spin up local Redis + Prefect server for Phase 3 development.
# Requires Docker and uv (for Prefect CLI).

REDIS_CONTAINER=${REDIS_CONTAINER:-auto-paper-redis}
PREFECT_API_URL=${PREFECT_API_URL:-http://127.0.0.1:4200/api}

echo "Launching Redis container (${REDIS_CONTAINER})..."
if ! docker ps --format '{{.Names}}' | grep -q "^${REDIS_CONTAINER}$"; then
  docker run -d --rm --name "${REDIS_CONTAINER}" -p 6379:6379 redis:7-alpine >/dev/null
else
  echo "Redis already running"
fi

echo "Starting Prefect server (prefect server start)"
export PREFECT_API_URL
uv run prefect server start --host 0.0.0.0 --port 4200 > /tmp/prefect-server.log 2>&1 &
PREFECT_PID=$!
echo "Prefect server listening at ${PREFECT_API_URL} (PID ${PREFECT_PID})"
echo "Logs: tail -f /tmp/prefect-server.log"
echo "Run 'make queue-prefect-deploy' then 'uv run prefect worker start --pool ingestion' to register flows."
