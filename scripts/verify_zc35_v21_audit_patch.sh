#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENGINE="$ROOT/zmatrix/zc35/catalyst_lifecycle.py"
TEST="$ROOT/tests/test_zc35_catalyst_v2.py"
PROFILE="$ROOT/data/stock_profiles/002472_双环传动_catalyst_profile.json"
SCORECARD="$ROOT/docs/rc1_audit/RC1_READINESS_SCORECARD.md"
PASS=0; FAIL=0

check() { if eval "$2"; then echo "  ✅ $1"; PASS=$((PASS+1)); else echo "  ❌ $1"; FAIL=$((FAIL+1)); fi; }

echo "═══ ZC35-v2.1 Audit Patch Fix Verification ═══"
echo ""

check "1.  catalyst_lifecycle 不含裸 tradeable" \
  "! grep -q '\"tradeable\"' \"$ENGINE\""
check "2.  catalyst_lifecycle 含 paper_trackable" \
  "grep -q 'paper_trackable' \"$ENGINE\""
check "3.  compute_residual_power 含 -pre_run 下限" \
  "grep -q 'days_since_event < -pre_run' \"$ENGINE\""
check "4.  compute_stack_effect 含 -pre_run <= days" \
  "grep -q '\-pre_run <= days' \"$ENGINE\""
check "5.  test 不含 Path.home()" \
  "! grep -q 'Path.home()' \"$TEST\""
check "6.  profile 含 LIVE_CASE_STUDY" \
  "grep -q 'LIVE_CASE_STUDY' \"$PROFILE\""
check "7.  profile 含 backtest_validated false" \
  "grep -q 'backtest_validated.*false' \"$PROFILE\""
check "8.  profile 含 cross_ticker_validated false" \
  "grep -q 'cross_ticker_validated.*false' \"$PROFILE\""
check "9.  profile 含 production_allowed false" \
  "grep -q 'production_allowed.*false' \"$PROFILE\""

ENGINE_REAL=$(grep -c "real_trade_allowed.*False" "$ENGINE" 2>/dev/null || echo 0)
if [ "$ENGINE_REAL" -gt 0 ]; then echo "  ✅ 10. engine 含 real_trade_allowed False"; PASS=$((PASS+1)); else echo "  ❌ 10. engine 含 real_trade_allowed False"; FAIL=$((FAIL+1)); fi
ENGINE_BROKER=$(grep -c "broker_order_allowed.*False" "$ENGINE" 2>/dev/null || echo 0)
if [ "$ENGINE_BROKER" -gt 0 ]; then echo "  ✅ 11. engine 含 broker_order_allowed False"; PASS=$((PASS+1)); else echo "  ❌ 11. engine 含 broker_order_allowed False"; FAIL=$((FAIL+1)); fi


echo ""
cd "$ROOT"
PYTHONPATH=. python3 -m pytest tests/test_zc35_catalyst_v2.py -q
if [ $? -eq 0 ]; then
    echo "  ✅ 12. pytest test_zc35_catalyst_v2 通过"
    PASS=$((PASS+1))
else
    echo "  ❌ 12. pytest test_zc35_catalyst_v2 失败"
    FAIL=$((FAIL+1))
fi

PYTHONPATH=. python3 -m pytest tests/test_zc35_v21_audit_patch_fix.py -q
if [ $? -eq 0 ]; then
    echo "  ✅ 13. pytest test_zc35_v21_audit_patch_fix 通过"
    PASS=$((PASS+1))
else
    echo "  ❌ 13. pytest test_zc35_v21_audit_patch_fix 失败"
    FAIL=$((FAIL+1))
fi

check "14. Scorecard 不含 RC1_BLOCKED" \
  "! grep -q 'RC1_BLOCKED' \"$SCORECARD\""
check "15. Scorecard 含 RC1_READY_RECOMMENDED" \
  "grep -q 'RC1_READY_RECOMMENDED' \"$SCORECARD\""
check "16. Scorecard 含 ZC35 excluded from RC1 scope" \
  "grep -q 'excluded from RC1 approval scope' \"$SCORECARD\""

echo ""
echo "══════════════════════════════════════"
echo "  结果: $PASS 通过 | $FAIL 失败"
echo "══════════════════════════════════════"
[ $FAIL -eq 0 ]
