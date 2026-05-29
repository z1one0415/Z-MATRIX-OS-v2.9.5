#!/usr/bin/env bash
# allowlist: forbidden-token-definition
set -euo pipefail
echo "═══ V4.0 FINAL-HARDGATES Hardening-B Verification ═══"

PYTHONPATH=. python3 -m compileall zmatrix tests scripts 2>&1 | tail -1

echo "[1] Run hardening pytest suite"
PYTHONPATH=. python3 -m pytest -q tests/v40_hardening/ 2>&1
echo "  ✅ hardening pytest suite PASS"

echo "[2] Dispatcher real_trade_allowed forbidden pattern scan"
python3 -c "
from pathlib import Path
text = Path('zmatrix/scoring/dispatcher.py').read_text(encoding='utf-8')
for bad in ['real_trade_allowed=r_mode','real_trade_allowed=d_mode','real_trade_allowed=True','real_trade_allowed = True']:
    assert bad not in text, f'FORBIDDEN: {bad}'
print('  ✅ Dispatcher clean')
"

echo "[3] Acceptance matrix + Content asset truth check"
PYTHONPATH=. python3 -m pytest -q tests/hardening_c2/test_truth_matrix_consistency.py tests/hardening_c2/test_asset_matrix_truth_sync.py 2>&1 | tail -1

echo "[4] Module split verification"
python3 -c "
from zmatrix.zc40.limit_board_fillability import LimitBoardFillabilityGate as L1
from zmatrix.runtime.batch3_gates import LimitBoardFillabilityGate as L2
assert L1 is L2
print('  ✅ Module split + shim delegates correctly')
"

echo "═══ V4.0 FINAL-HARDGATES Hardening-B PASS ═══"
