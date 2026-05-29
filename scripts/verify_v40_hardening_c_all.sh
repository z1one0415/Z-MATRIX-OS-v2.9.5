#!/usr/bin/env bash
# allowlist: forbidden-token-definition
set -euo pipefail
echo "═══ V4.0 FINAL-HARDGATES Hardening-C Full Integration Verification ═══"

echo "[1] Compile + Hardening-B baseline"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts 2>&1 | tail -1
bash scripts/verify_v40_hardening_b.sh 2>&1 | grep "PASS\|passed" | head -3

echo "[2] C1-C8 Integration Tests"
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c_integration.py 2>&1

echo "[3] Forbidden flags scan"
python3 -c "
from pathlib import Path
forbidden=['real_trade_allowed=True','broker_order_allowed=True','auto_buy_allowed=True','auto_sell_allowed=True','runtime_enabled=True']
for p in Path('zmatrix').rglob('*.py'):
    t=p.read_text(encoding='utf-8',errors='ignore')
    for f in forbidden:
        assert f not in t, f'FORBIDDEN {f} in {p}'
print('  ✅ 0 forbidden flags in zmatrix/')
"

echo "[4] Truth report status"
python3 -c "
t=open('docs/release/V40_CLOSEOUT_TRUTH_REPORT.md',encoding='utf-8').read()
assert 'INTEGRATION_COMPLETE_CANDIDATE' in t; assert 'NOT_APPROVED' in t; assert 'BLOCKED' in t
print('  ✅ Truth report: INTEGRATION_COMPLETE_CANDIDATE')
"

echo "═══ V4.0 FINAL-HARDGATES Hardening-C PASS ═══"
