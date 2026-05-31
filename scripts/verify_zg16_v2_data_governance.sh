#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-G16 v2 Data Governance Verification ═══"

python3 -m compileall -q zmatrix tests scripts

echo "--- Event Layer ---"
PYTHONPATH=. python3 -m pytest -q tests/research_db/event_layer/

echo "--- Source Health ---"
PYTHONPATH=. python3 -m pytest -q tests/research_db/source_health/

echo ""
bash scripts/verify_z_agent_kernel.sh
bash scripts/verify_zg16_v12_stub.sh

echo ""
echo "═══ Runtime Ledger Empty Check ═══"
LEDGER_DIRS=("data/research_db/agent/ledgers" "data/research_db/governance")
for dir in "${LEDGER_DIRS[@]}"; do
    for f in "$dir"/*; do
        if [ -f "$f" ] && [ -s "$f" ]; then
            size=$(wc -c < "$f" | tr -d ' ')
            if [ "$size" -gt 0 ] && [ "$(basename "$f")" != "data_source_attribution_ledger.csv" ]; then
                echo "FAIL: $f not empty ($size bytes)"
                exit 1
            fi
        fi
    done
done
echo "✅ All runtime ledgers EMPTY"

python3 <<'PY'
from pathlib import Path

forbidden = [
 "external_api=True","shadowbroker_deployed=True","production_allowed=True",
 "trade_allowed=True","verdict_allowed=True","broker_order_allowed=True",
 "real_trade_allowed=True","auto_buy_allowed=True","auto_sell_allowed=True",
]

roots = ["zmatrix/research_db","zmatrix/runtime"]
for root in roots:
    for p in Path(root).rglob("*.py"):
        text = p.read_text("utf-8",errors="ignore")
        for token in forbidden:
            assert token not in text, f"FORBIDDEN: {token} in {p}"
print("✅ Data governance forbidden scan PASS")
PY

echo "═══ G16-2 Data Governance PASS ═══"
