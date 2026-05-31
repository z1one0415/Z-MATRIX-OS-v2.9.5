#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-G16 v8 AutoCase Memory Verification ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/research_db/zg16/
PYTHONPATH=. python3 -m pytest -q tests/agent/
bash scripts/verify_zg16_v6_cockpit_read_model.sh
bash scripts/verify_zg16_v5_e2e_stub.sh
bash scripts/verify_z_agent_kernel.sh

echo ""
echo "═══ Runtime Ledger Empty Check ═══"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
 if [ -f "$f" ] && [ -s "$f" ]; then echo "FAIL: $f not empty"; exit 1; fi
done
echo "✅ All runtime ledgers EMPTY"

PYTHONPATH=. python3 -c "
from pathlib import Path
extra = ['autocaseforge_main_write=True', 'memory_main_write=True', 'researchdb_main_write=True']
forbidden = ['external_api=True','shadowbroker_deployed=True','production_allowed=True','trade_allowed=True','verdict_allowed=True'] + extra
for p in Path('zmatrix/research_db').rglob('*.py'):
    for t in forbidden:
        assert t not in p.read_text('utf-8','ignore'), f'{t} in {p}'
print('✅ forbidden scan PASS')
"
echo "═══ Z-G16 v8 AutoCase Memory PASS ═══"
