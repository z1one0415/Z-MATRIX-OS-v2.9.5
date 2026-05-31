#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 Full Stub Integration Verification ═══"
echo "=== 1. Compileall ==="
python3 -m compileall -q zmatrix tests scripts
echo "=== 2. Research DB tests ==="
PYTHONPATH=. python3 -m pytest -q tests/research_db/
echo "=== 3. Agent tests ==="
PYTHONPATH=. python3 -m pytest -q tests/agent/

echo "=== 4. Explicit Stage Verify Chain ==="
for vs in verify_zg16_v8_autocase_memory verify_zg16_v6_cockpit_read_model verify_zg16_v5_e2e_stub verify_zg16_v4_skill_invocation verify_zg16_v3_query_bridge verify_zg16_v2_data_governance verify_zg16_v12_stub verify_z_agent_kernel; do
    echo "--- $vs ---"
    bash "scripts/${vs}.sh" || { echo "FAIL: $vs"; exit 1; }
done

echo ""
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
        for token in forbidden:
            assert token not in p.read_text("utf-8","ignore"), f"{token} in {p}"
print("✅ Full forbidden scan PASS")
PYEOF
echo "═══ Z-G16 Full Stub Integration PASS ═══"
