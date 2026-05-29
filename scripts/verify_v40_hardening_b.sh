#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 FINAL-HARDGATES Hardening-B Verification ═══"
PYTHONPATH=. python3 -m compileall zmatrix tests scripts 2>&1 | tail -1
PYTHONPATH=. python3 tests/v40_hardening/test_hardening_b.py
echo "  ✅ 9 hardening tests PASS"

# Dispatcher expression scan
python3 -c "
t=open('zmatrix/scoring/dispatcher.py',encoding='utf-8').read()
for b in ['real_trade_allowed=r_mode','real_trade_allowed=d_mode','real_trade_allowed=True']:
    assert b not in t, f'FORBIDDEN: {b}'
print('  ✅ Dispatcher real_trade_allowed expressions cleared')
"

# Acceptance matrix truth
python3 -c "
t=open('docs/upgrade/V40_FULL_SCOPE_ACCEPTANCE_MATRIX.md',encoding='utf-8').read()
assert 'SMOKE_PROTOTYPE' in t; assert 'NOT_APPROVED' in t; assert 'BLOCKED' in t
assert 'SMOKE_DONE' in t; assert 'NOT_DONE' in t
print('  ✅ Acceptance matrix truthful')
"

# Content asset index truth
python3 -c "
t=open('docs/upgrade/V40_CONTENT_ASSET_INDEX.md',encoding='utf-8').read()
assert 'SMOKE_PROTOTYPE' in t; assert 'REGISTRY_ONLY' in t; assert 'NOT_DONE' in t
print('  ✅ Content asset index truthful')
"

# Closeout truth report
python3 -c "
t=open('docs/release/V40_CLOSEOUT_TRUTH_REPORT.md',encoding='utf-8').read()
assert 'SMOKE_PROTOTYPE' in t; assert 'NOT_APPROVED' in t; assert 'BLOCKED' in t
print('  ✅ Closeout truth report present')
"

# Module split verification
python3 -c "
from zmatrix.zc40.limit_board_fillability import LimitBoardFillabilityGate
from zmatrix.zc45.proxy_hedge_stress import ProxyHedgeStressTest
from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
from zmatrix.strategy.multi_strategy_sleeve import MultiStrategySleeve
# Verify shim delegates correctly
from zmatrix.runtime.batch3_gates import LimitBoardFillabilityGate as LB1
from zmatrix.zc40.limit_board_fillability import LimitBoardFillabilityGate as LB2
assert LB1 is LB2
print('  ✅ All 4 modules split + shim delegates correctly')
"

# Run original 8 verify scripts (summary only)
for s in verify_v40_guardrails verify_v40_parser_scorer_split verify_v40_zc35_catalyst_guardrails verify_v40_zc45_proxy_hedge_guardrails verify_v40_final_hardgates verify_v40_batch1_failover verify_v40_batch2_research_council verify_v40_batch345_gates; do
    bash scripts/${s}.sh 2>&1 | tail -1
done

echo "═══ V4.0 FINAL-HARDGATES Hardening-B PASS ═══"
