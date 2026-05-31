#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 Full Stub Integration Verification ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 -m pytest -q tests/agent/
echo "═══ Runtime Ledger Empty Check ═══"
for dir in data/research_db/agent/ledgers data/research_db/governance; do
    for f in "$dir"/*; do
        [ ! -f "$f" ] && continue
        base=$(basename "$f")
        [ "$base" = "data_source_attribution_ledger.csv" ] && continue
        if [ -s "$f" ]; then echo "FAIL: $f not empty"; exit 1; fi
    done
done
echo "✅ All ledgers EMPTY"
python3 << 'PYEOF'
from pathlib import Path
forbidden = ["external_api=True","external_api_used=True","shadowbroker_deployed=True",
 "production_allowed=True","trade_allowed=True","verdict_allowed=True",
 "broker_order_allowed=True","real_trade_allowed=True",
 "autocaseforge_main_write=True","memory_main_write=True","researchdb_main_write=True"]
for root in ["zmatrix/research_db","zmatrix/agent"]:
    for p in Path(root).rglob("*.py"):
        text = p.read_text("utf-8",errors="ignore")
        for token in forbidden:
            assert token not in text, f"{token} in {p}"
print("✅ Full forbidden scan PASS")
PYEOF
echo "═══ Z-G16 Full Stub Integration PASS ═══"
