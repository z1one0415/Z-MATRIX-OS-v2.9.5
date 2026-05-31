#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 Full Stub Integration Verification ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/zg16/
PYTHONPATH=. python3 -m pytest -q tests/agent/
bash scripts/verify_zg16_v8_autocase_memory.sh
bash scripts/verify_zg16_v6_cockpit_read_model.sh
bash scripts/verify_zg16_v5_e2e_stub.sh
bash scripts/verify_zg16_v4_skill_invocation.sh
bash scripts/verify_zg16_v3_query_bridge.sh
bash scripts/verify_zg16_v2_data_governance.sh
bash scripts/verify_zg16_v12_stub.sh
bash scripts/verify_z_agent_kernel.sh

echo ""
echo "═══ Full Runtime Ledger Empty Check ═══"
for dir in data/research_db/agent/ledgers data/research_db/governance; do
 for f in "$dir"/*; do
 [ ! -f "$f" ] && continue
 if [ -s "$f" ] && [ "$(basename "$f")" != "data_source_attribution_ledger.csv" ]; then
 echo "FAIL: runtime ledger not empty: $f ($(wc -c < "$f") bytes)"
 exit 1
 fi
 done
done
echo "✅ All runtime & governance ledgers EMPTY"

PYTHONPATH=. python3 -c "
from pathlib import Path
forbidden = ['external_api=True','external_api_used=True','shadowbroker_deployed=True',
 'production_allowed=True','trade_allowed=True','verdict_allowed=True',
 'broker_order_allowed=True','real_trade_allowed=True',
 'autocaseforge_main_write=True','memory_main_write=True','researchdb_main_write=True']
for root in ['zmatrix/research_db','zmatrix/agent']:
 for p in Path(root).rglob('*.py'):
 for t in forbidden:
 assert t not in p.read_text('utf-8','ignore'), f'{t} in {p}'
print('✅ Full forbidden scan PASS')
"
echo "═══ Z-G16 Full Stub Integration PASS ═══"
