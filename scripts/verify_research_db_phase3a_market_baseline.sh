#!/usr/bin/env bash
set -euo pipefail
echo "═══ ResearchDB Phase 3-A Market Baseline Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"
python3 -m compileall zmatrix/research_db/market_data/ tests/research_db/market_data/
bash scripts/verify_research_db_phase2_master_data.sh
PYTHONPATH=. python3 -m pytest -q tests/research_db/market_data/
python3 -c "
from pathlib import Path; import subprocess
base=Path('zmatrix/research_db/market_data')
for name in ['market_schema.py','trading_calendar.py','price_bar_store.py','benchmark_registry.py','adjustment_factor_store.py','market_data_guardrail.py']:
    assert (base/name).exists(),f'missing {name}'
for p in base.rglob('*.py'):
    for f in ['real_trade_allowed=True','broker_order_allowed=True']:
        assert f not in p.read_text(),f'{f} in {p}'
r=subprocess.run(['git','ls-files'],capture_output=True,text=True)
for l in r.stdout.splitlines():
    if 'market_data/raw/' in l.lower() and not l.endswith('.gitkeep'): raise SystemExit(f'raw: {l}')
print('✅ Phase 3-A safety scan PASS')
"
test -f docs/research_db/PHASE3_SCOPE_LOCK.md && test -f docs/research_db/PHASE3_ACCEPTANCE_MATRIX.md && test -f docs/research_db/PHASE3_A_CLOSEOUT_REPORT.md
echo "═══ ResearchDB Phase 3-A Market Baseline PASS ═══"
