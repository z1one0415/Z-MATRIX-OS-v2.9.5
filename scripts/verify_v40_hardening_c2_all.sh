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

echo "[6] Truth report + extended forbidden scan"
python3 -c "
from pathlib import Path
t=Path('docs/release/V40_CLOSEOUT_TRUTH_REPORT.md').read_text(encoding='utf-8')
assert 'INTEGRATION_SMOKE_CANDIDATE' in t; assert 'NOT_APPROVED' in t; assert 'BLOCKED' in t
for p in Path('zmatrix').rglob('*.py'):
    c=p.read_text(encoding='utf-8',errors='ignore')
    if 'allowlist: forbidden-token-definition' in c: continue
    for f in ['real_trade_allowed=True','broker_order_allowed=True','runtime_enabled=True','auto_buy_allowed=True','auto_sell_allowed=True','production_allowed=True']:
        assert f not in c, f'FORBIDDEN {f} in {p}'
print('  ✅ Truth report + 0 forbidden flags (6 fields)')
"

echo "═══ V4.0 FINAL-HARDGATES Hardening-C2 PASS ═══"
echo "[5.5] Hardening-C2.1 Truth/Asset/Matrix Closeout"
bash scripts/verify_v40_hardening_c2_1_truth_closeout.sh

echo "[6] Truth report + extended forbidden scan"
python3 << 'PY'
from pathlib import Path
t=Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
assert "INTEGRATION_SMOKE_CANDIDATE" in t
assert "NOT_APPROVED" in t
assert "BLOCKED" in t
for p in Path("zmatrix").rglob("*.py"):
    c=p.read_text(encoding="utf-8",errors="ignore")
    if "allowlist: forbidden-token-definition" in c: continue
    for f in ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        assert f not in c, f"FORBIDDEN {f} in {p}"
print("  ✅ Truth report + 0 forbidden flags (6 fields)")
PY
