#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BACKEND_HOST="${ZMATRIX_BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${ZMATRIX_BACKEND_PORT:-8765}"
COCKPIT_HOST="${ZMATRIX_COCKPIT_HOST:-127.0.0.1}"
COCKPIT_PORT="${ZMATRIX_COCKPIT_PORT:-5173}"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"

backend_pid=""

cleanup() {
  set +e
  if [[ -n "$backend_pid" ]] && kill -0 "$backend_pid" 2>/dev/null; then
    kill "$backend_pid"
    wait "$backend_pid" 2>/dev/null
  fi
  set -e
}

trap cleanup EXIT INT TERM

export VITE_ZMATRIX_PRODUCT_STATUS_URL="${BACKEND_URL}/api/product/status.json"
export VITE_ZMATRIX_OPERATOR_ACTIONS_URL="${BACKEND_URL}/api/product/operator_actions.json"
export VITE_ZMATRIX_RESEARCH_STATUS_URL="${BACKEND_URL}/api/product/research_status.json"
export VITE_ZMATRIX_AGENT_BRIDGE_URL="${BACKEND_URL}/api/product/agent_bridge.json"
export VITE_ZMATRIX_AGENT_DRAFT_URL="${BACKEND_URL}/api/product/agent_draft.json"

echo "=== Z-MATRIX Local Workstation ==="
echo "Backend: ${BACKEND_URL}"
echo "Cockpit: http://${COCKPIT_HOST}:${COCKPIT_PORT}"
echo "Safety: no alpha claim, no promotion, broker blocked, real trade blocked"

PYTHONPATH=. python3 scripts/product/start_backend_service.py \
  --host "$BACKEND_HOST" \
  --port "$BACKEND_PORT" &
backend_pid="$!"

for attempt in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS "${BACKEND_URL}/health" >/tmp/zmatrix_local_workstation_health.json 2>/dev/null; then
    break
  fi
  if [[ "$attempt" == "10" ]]; then
    echo "Backend did not become ready at ${BACKEND_URL}/health" >&2
    exit 1
  fi
  sleep 0.5
done

echo "Backend health ready."
echo "Open cockpit at http://${COCKPIT_HOST}:${COCKPIT_PORT}"

npm --prefix apps/cockpit_web run dev -- --host "$COCKPIT_HOST" --port "$COCKPIT_PORT"
