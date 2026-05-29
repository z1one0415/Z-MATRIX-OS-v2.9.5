#!/bin/bash
# ZC35-v2.1 Audit Patch Verification
BASE="$HOME/Documents/Z-MATRIX-OS v2.9.5"
ENGINE="$BASE/zmatrix/zc35/catalyst_lifecycle.py"
TEST="$BASE/tests/test_zc35_catalyst_v2.py"
PROFILE="$BASE/data/stock_profiles/002472_双环传动_catalyst_profile.json"
PASS=0; FAIL=0

check() { if eval "$2"; then echo "  ✅ $1"; PASS=$((PASS+1)); else echo "  ❌ $1"; FAIL=$((FAIL+1)); fi; }

echo "═══ ZC35-v2.1 Audit Patch Verification ═══"
echo ""

check "1. CATALYST_TAXONOMY 中无 tradeable" \
  "! grep -q '\"tradeable\"' \"$ENGINE\""
check "2. 使用 paper_trackable 替代" \
  "grep -q 'paper_trackable' \"$ENGINE\""
check "3. compute_residual_power 有 -pre_run 下限" \
  "grep -q 'days_since_event < -pre_run' \"$ENGINE\""
check "4. compute_stack_effect 有下界保护" \
  "grep -q '\-pre_run <= days' \"$ENGINE\""
check "5. 测试路径不依赖 ~/Documents" \
  "! grep -q 'Path.home()' \"$TEST\""
check "6a. 档案含 data_status" \
  "grep -q 'LIVE_CASE_STUDY' \"$PROFILE\""
check "6b. 档案 backtest_validated=false" \
  "grep -q 'backtest_validated.*false' \"$PROFILE\""
check "6c. 档案 production_allowed=false" \
  "grep -q 'production_allowed.*false' \"$PROFILE\""
check "7a. 保持 real_trade_allowed=False" \
  "grep -c 'real_trade_allowed.*False' \"$ENGINE\" | grep -qv ':0'"
check "7b. 保持 broker_order_allowed=False" \
  "grep -c 'broker_order_allowed.*False' \"$ENGINE\" | grep -qv ':0'"

echo ""
cd "$BASE" && python3 -m pytest tests/test_zc35_catalyst_v2.py -q 2>&1 | tail -3
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "  ✅ 测试全部通过"
    PASS=$((PASS+1))
else
    echo "  ❌ 测试失败"
    FAIL=$((FAIL+1))
fi

echo ""
echo "══════════════════════════════════════"
echo "  结果: $PASS 通过 | $FAIL 失败"
echo "══════════════════════════════════════"
[ $FAIL -eq 0 ]
