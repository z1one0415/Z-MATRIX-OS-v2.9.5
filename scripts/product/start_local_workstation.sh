#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

load_dotenv() {
  local env_file="$ROOT/.env"
  [[ -f "$env_file" ]] || return 0
  while IFS='=' read -r raw_key raw_value || [[ -n "$raw_key" ]]; do
    local key
    key="$(printf '%s' "$raw_key" | tr -d '[:space:]')"
    [[ -z "$key" || "$key" == \#* ]] && continue
    case "$key" in
      Z_MATRIX_PRODUCT_HOST|Z_MATRIX_PRODUCT_PORT|Z_MATRIX_WORKSPACE_ID|Z_MATRIX_COCKPIT_PUBLIC_ROOT|Z_MATRIX_VENDOR_ROOT|TUSHARE_TOKEN|DEEPSEEK_API_KEY|ZMATRIX_BACKEND_HOST|ZMATRIX_BACKEND_PORT)
        [[ -n "${!key:-}" ]] && continue
        local value="$raw_value"
        value="${value%$'\r'}"
        if [[ "${value:0:1}" == '"' && "${value: -1}" == '"' ]] || [[ "${value:0:1}" == "'" && "${value: -1}" == "'" ]]; then
          value="${value:1:${#value}-2}"
        fi
        export "$key=$value"
        ;;
    esac
  done < "$env_file"
}

load_dotenv

BACKEND_HOST="${ZMATRIX_BACKEND_HOST:-${Z_MATRIX_PRODUCT_HOST:-127.0.0.1}}"
BACKEND_PORT="${ZMATRIX_BACKEND_PORT:-${Z_MATRIX_PRODUCT_PORT:-8765}}"
COCKPIT_HOST="${ZMATRIX_COCKPIT_HOST:-127.0.0.1}"
COCKPIT_PORT="${ZMATRIX_COCKPIT_PORT:-5173}"
BACKEND_URL="http://${BACKEND_HOST}:${BACKEND_PORT}"
COCKPIT_PUBLIC_ROOT="${Z_MATRIX_COCKPIT_PUBLIC_ROOT:-apps/cockpit_web/public/api/cockpit}"
VENDOR_ROOT="${Z_MATRIX_VENDOR_ROOT:-data/research_db/market_data/vendor/tushare_5y}"
WORKSPACE_ID="${Z_MATRIX_WORKSPACE_ID:-ws_personal_z_prime}"

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
export VITE_ZMATRIX_PRODUCT_READINESS_URL="${BACKEND_URL}/api/product/readiness.json"
export VITE_ZMATRIX_OPERATOR_ACTIONS_URL="${BACKEND_URL}/api/product/operator_actions.json"
export VITE_ZMATRIX_RESEARCH_STATUS_URL="${BACKEND_URL}/api/product/research_status.json"
export VITE_ZMATRIX_RESEARCH_EVIDENCE_INDEX_URL="${BACKEND_URL}/api/product/research_evidence_index.json"
export VITE_ZMATRIX_REPORT_EXPORT_STATUS_URL="${BACKEND_URL}/api/product/report_export_status.json"
export VITE_ZMATRIX_DATA_QUALITY_STATUS_URL="${BACKEND_URL}/api/product/data_quality_status.json"
export VITE_ZMATRIX_COCKPIT_MANIFEST_URL="${BACKEND_URL}/api/product/cockpit_manifest.json"
export VITE_ZMATRIX_AGENT_BRIDGE_URL="${BACKEND_URL}/api/product/agent_bridge.json"
export VITE_ZMATRIX_AGENT_DRAFT_URL="${BACKEND_URL}/api/product/agent_draft.json"
export VITE_ZMATRIX_HOLDINGS_PACKET_URL="${BACKEND_URL}/api/cockpit/holdings_packet.json"
export VITE_ZMATRIX_SELECTION_PACKET_URL="${BACKEND_URL}/api/cockpit/selection_packet.json"
export VITE_ZMATRIX_HISTORY_PACKET_URL="${BACKEND_URL}/api/cockpit/history_packet.json"
export VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL="${BACKEND_URL}/api/cockpit/control_compass_packet.json"
export VITE_ZMATRIX_DAYAN_ASK_PACKET_URL="${BACKEND_URL}/api/cockpit/dayan_ask_packet.json"

echo "=== Z-MATRIX Local Workstation ==="
echo "Backend: ${BACKEND_URL}"
echo "Cockpit: http://${COCKPIT_HOST}:${COCKPIT_PORT}"
echo "Safety: no alpha claim, no promotion, broker blocked, real trade blocked"

PYTHONPATH=. python3 scripts/product/start_backend_service.py \
  --host "$BACKEND_HOST" \
  --port "$BACKEND_PORT" \
  --public-root "$COCKPIT_PUBLIC_ROOT" \
  --vendor-root "$VENDOR_ROOT" \
  --workspace-id "$WORKSPACE_ID" &
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
