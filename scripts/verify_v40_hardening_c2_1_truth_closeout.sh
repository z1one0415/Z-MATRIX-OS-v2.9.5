#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 Hardening-C2.1 Truth Closeout Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts 2>&1 | tail -1
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/ 2>&1 | tail -2
python3 -c "
from pathlib import Path
t=Path('docs/release/V40_CLOSEOUT_TRUTH_REPORT.md').read_text(encoding='utf-8')
m=Path('docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md').read_text(encoding='utf-8')
assert 'INTEGRATION_SMOKE_CANDIDATE' in t; assert 'NOT_APPROVED' in t; assert 'BLOCKED' in t
assert 'DEPTH_PARTIAL' in m; assert 'INTEGRATION_SMOKE_DONE' in m
assert 'ACCEPTANCE_DONE' not in m or m.count('ACCEPTANCE_DONE')<=2
assert 'RC1_APPROVED' not in m+t; assert 'PRODUCTION_READY' not in m+t
for p in Path('zmatrix').rglob('*.py'):
    c=p.read_text(encoding='utf-8',errors='ignore')
    for f in ['real_trade_allowed=True','broker_order_allowed=True']: assert f not in c
print('  ✅ Truth matrix synchronized + 0 forbidden flags')
"
echo "═══ V4.0 Hardening-C2.1 PASS ═══"
