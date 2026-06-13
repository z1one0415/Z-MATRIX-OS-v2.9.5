#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "=== Z-MATRIX Product Smoke ==="

tmp_root="$(mktemp -d)"
tmp_plan="$tmp_root/vendor_dry_plan.json"
tmp_package="$tmp_root/product_package"
trap 'rm -rf "$tmp_root"' EXIT

echo "[1] Python product runtime compile"
python3 -m compileall -q zmatrix/product_runtime tests/product_runtime scripts/product
bash -n scripts/product/start_local_workstation.sh

echo "[2] Backend health check"
PYTHONPATH=. python3 scripts/product/start_backend_service.py --check >/tmp/zmatrix_product_backend_status.json

echo "[3] Cockpit packet export"
PYTHONPATH=. python3 scripts/cockpit/export_all_packets.py >/tmp/zmatrix_cockpit_packet_export.json

echo "[4] Local vendor dry plan"
PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py \
  --symbols 601899,002472,300750 \
  --end-date 20260613 \
  --years 5 \
  --endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic \
  --dry-plan >"$tmp_plan"

echo "[5] Product runtime tests"
PYTHONPATH=. python3 -m pytest -q tests/product_runtime/

echo "[6] Market data baseline"
bash scripts/verify_research_db_phase3a_market_baseline.sh

echo "[7] Agent kernel"
bash scripts/verify_z_agent_kernel.sh

echo "[8] V4 final hard gates"
bash scripts/verify_v40_final_hardgates.sh

echo "[9] Cockpit frontend tests"
npm --prefix apps/cockpit_web test

echo "[10] Cockpit frontend build"
npm --prefix apps/cockpit_web run build

echo "[11] Product package build"
PYTHONPATH=. python3 scripts/product/build_local_workstation_package.py \
  --output-dir "$tmp_package" \
  --no-archive >/tmp/zmatrix_product_package_manifest.json

echo "=== Z-MATRIX Product Smoke PASS ==="
