#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 FINAL-HARDGATES Hardening-C2 Full Verification ═══"

echo "[0] Compile"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

echo "[1] Hardening-B baseline"
bash scripts/verify_v40_hardening_b.sh 2>&1 | tail -1

echo "[2] C2-0 Truth Matrix"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_truth_matrix_consistency.py 2>&1 | tail -2

echo "[3] C2-1/2 Depth Modules"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_depth_modules.py 2>&1 | tail -2

echo "[4] C2-5 IRF True Chains"
PYTHONPATH=. python3 -c "
from zmatrix.irf.irf_chain import irf01_full_chain, irf03_factor_chain, irf04_execution_chain
r1=irf01_full_chain(); assert r1['export_manifest']==False; print('  ✅ IRF-01: DataForge→Council→Report→Audit chain')
r3=irf03_factor_chain(); assert r3['horizon_ready']; print('  ✅ IRF-03: Factor→Horizon→Gate→Audit chain')
r4=irf04_execution_chain(); assert r4['gate_action']=='NOT_FILLABLE'; print('  ✅ IRF-04: Execution→Gate→Preview→Audit chain')
print('  ✅ All 3 IRF chains verified')
"

echo "[5] Full integration tests"
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c_integration.py 2>&1 | tail -2

echo "[6] Truth report + forbidden scan"
python3 -c "
from pathlib import Path
t=Path('docs/release/V40_CLOSEOUT_TRUTH_REPORT.md').read_text(encoding='utf-8')
assert 'INTEGRATION_SMOKE_CANDIDATE' in t; assert 'NOT_APPROVED' in t; assert 'BLOCKED' in t
for p in Path('zmatrix').rglob('*.py'):
    c=p.read_text(encoding='utf-8',errors='ignore')
    for f in ['real_trade_allowed=True','broker_order_allowed=True','runtime_enabled=True']:
        assert f not in c, f'FORBIDDEN {f} in {p}'
print('  ✅ Truth report + 0 forbidden flags')
"

echo "═══ V4.0 FINAL-HARDGATES Hardening-C2 PASS ═══"
