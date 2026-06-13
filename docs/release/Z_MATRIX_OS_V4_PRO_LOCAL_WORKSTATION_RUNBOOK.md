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

Optional for local LLM bridge configuration:

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
http://127.0.0.1:8765/api/product/agent_bridge.json
http://127.0.0.1:8765/api/cockpit/holdings_packet.json
```

## 6. Start Local Workstation

The combined local startup command is:

```bash
bash scripts/product/start_local_workstation.sh
```

It starts the local backend, waits for `/health`, exports the cockpit runtime URLs, and starts the cockpit dev server in the foreground. Stop it with `Ctrl-C`; the backend process is cleaned up by the script.

## 7. Start Cockpit Manually

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

## 8. Vendor Data Dry Plan

```bash
PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py \
  --symbols 601899,002472,300750 \
  --end-date 20260613 \
  --years 5 \
  --endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic \
  --dry-plan
```

Remove `--dry-plan` only after `.env` contains a local token and the user intentionally wants local vendor files under the ignored vendor store.

## 9. Product Readiness

```bash
PYTHONPATH=. python3 scripts/product/check_product_readiness.py
```

Expected state:

```text
Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS
```

This checks install/start files, backend status, cockpit packets, research status, Hermes bridge status, operator actions, and hard safety states.

## 10. Product Smoke

```bash
bash scripts/verify_z_matrix_product_smoke.sh
```

This verifies:

- product runtime imports;
- backend status;
- product readiness;
- cockpit packet export;
- vendor dry plan;
- product runtime tests;
- market data baseline;
- agent kernel;
- V4 final hard gates;
- cockpit frontend tests;
- cockpit frontend build.
- research report export.
- local workstation package build.

## 11. Export Research Report Pack

```bash
PYTHONPATH=. python3 scripts/product/export_research_report_pack.py
```

Default output:

```text
build/research_report_exports/Z-MATRIX-research-report-pack
```

The export contains research docs, audit docs, selected runtime report manifests, a report export manifest, and checksums. It does not include raw vendor data, private account data, or real secrets.

## 12. Build Local Workstation Package

```bash
PYTHONPATH=. python3 scripts/product/build_local_workstation_package.py
```

Default output:

```text
build/product_packages/Z-MATRIX-OS-V4-PRO-local-workstation
```

The output directory is ignored by Git. The package includes runtime entrypoints, cockpit build output, cockpit packets, a source snapshot, a product manifest, and checksums. It does not include raw vendor data, private account data, or real secrets.

## 13. Safety State

The local product preview is a research workstation. It keeps these states blocked:

- alpha claim;
- promotion;
- broker runtime;
- real trade;
- direct agent mutation;
- secret storage in git.

If any of these states becomes ambiguous, the build is not a product RC.
