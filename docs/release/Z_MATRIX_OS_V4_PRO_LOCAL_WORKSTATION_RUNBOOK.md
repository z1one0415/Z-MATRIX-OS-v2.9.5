# Z-MATRIX-OS V4-PRO Local Workstation Runbook

Status: local product preview runbook
Scope: install, configure, start backend, open cockpit, run smoke

## 1. Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip pytest
npm --prefix apps/cockpit_web install
```

## 2. Configure

```bash
cp .env.example .env
```

Fill only local environment values in `.env`. Do not commit `.env`.

Required for vendor data ingestion:

```text
TUSHARE_TOKEN=
```

Optional for future agent bridge:

```text
DEEPSEEK_API_KEY=
```

## 3. Build Cockpit Packets

```bash
PYTHONPATH=. python3 scripts/cockpit/export_all_packets.py
```

The cockpit packet root is:

```text
apps/cockpit_web/public/api/cockpit
```

## 4. Check Backend

```bash
PYTHONPATH=. python3 scripts/product/start_backend_service.py --check
```

Expected state:

```text
Z_MATRIX_PRODUCT_RUNTIME_READY
```

If local vendor data has not been pulled yet, the backend can still run, but data source readiness will show local vendor manifests are missing.

## 5. Start Backend

```bash
PYTHONPATH=. python3 scripts/product/start_backend_service.py --host 127.0.0.1 --port 8765
```

Useful local endpoints:

```text
http://127.0.0.1:8765/health
http://127.0.0.1:8765/api/product/status.json
http://127.0.0.1:8765/api/cockpit/holdings_packet.json
```

## 6. Start Cockpit

Optional frontend runtime pointer:

```bash
cp apps/cockpit_web/.env.example apps/cockpit_web/.env.local
```

```bash
npm --prefix apps/cockpit_web run dev -- --port 5173
```

Open:

```text
http://127.0.0.1:5173
```

## 7. Vendor Data Dry Plan

```bash
PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py \
  --symbols 601899,002472,300750 \
  --end-date 20260613 \
  --years 5 \
  --endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic \
  --dry-plan
```

Remove `--dry-plan` only after `.env` contains a local token and the user intentionally wants local vendor files under the ignored vendor store.

## 8. Product Smoke

```bash
bash scripts/verify_z_matrix_product_smoke.sh
```

This verifies:

- product runtime imports;
- backend status;
- cockpit packet export;
- vendor dry plan;
- product runtime tests;
- market data baseline;
- agent kernel;
- V4 final hard gates;
- cockpit frontend tests;
- cockpit frontend build.

## 9. Safety State

The local product preview is a research workstation. It keeps these states blocked:

- alpha claim;
- promotion;
- broker runtime;
- real trade;
- direct agent mutation;
- secret storage in git.

If any of these states becomes ambiguous, the build is not a product RC.
