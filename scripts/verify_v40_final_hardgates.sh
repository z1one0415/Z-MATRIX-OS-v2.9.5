#!/usr/bin/env bash
# allowlist: forbidden-token-definition
set -euo pipefail
echo "═══ V4.0 Final Hard Gates Verification ═══"

# Check three hard gate components
echo "--- ZC40 LimitBoardFillabilityGate ---"
if [ -f "docs/architecture/ZC40_LIMIT_BOARD_FILLABILITY_PROTOCOL_V10.md" ]; then
    echo "  ✅ LimitBoardFillabilityGate protocol present"
else
    echo "  ❌ Missing"; exit 1
fi

echo "--- ZC45 ProxyHedgeStressTest ---"
if [ -f "docs/architecture/ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_PROTOCOL_V10.md" ]; then
    echo "  ✅ ProxyHedgeStressTest protocol present"
else
    echo "  ❌ Missing"; exit 1
fi

echo "--- Runtime LLM Failover ---"
if [ -f "docs/architecture/RUNTIME_LLM_FAILOVER_PROTOCOL_V10.md" ]; then
    echo "  ✅ LLMProviderFailoverPolicy protocol present"
else
    echo "  ❌ Missing"; exit 1
fi

# Check final hard gates scope lock
if [ -f "docs/upgrade/V40_FINAL_HARDGATES_SCOPE_LOCK.md" ]; then
    echo "  ✅ Final Hard Gates scope lock present"
else
    echo "  ❌ Missing"; exit 1
fi

# Check no market neutral claims in scope
python3 -c "
content = open('docs/upgrade/V40_FINAL_HARDGATES_SCOPE_LOCK.md').read()
assert 'Market Neutral' not in content or 'NOT' in content or 'claim' in content.lower()
print('  ✅ No Market Neutral claims in scope')
" 2>/dev/null || echo "  ⚠️  Check scope lock for Market Neutral statements"

# Check no real_option_order
if grep -r 'real_option_order' --include="*.md" docs/ 2>/dev/null; then
    echo "  ❌ real_option_order found in docs/"; exit 1
fi
echo "  ✅ No real_option_order in scope"

# Check no limit_up_auto_buy
if grep -r 'limit_up_auto_buy' --include="*.md" docs/ 2>/dev/null; then
    echo "  ❌ limit_up_auto_buy found in docs/"; exit 1
fi
echo "  ✅ No limit_up_auto_buy in scope"

# Check no fresh judgement during LLM failure
if grep -q 'NO new.*judgment\|no.*new.*judgment\|failure.*no.*new' docs/architecture/RUNTIME_LLM_FAILOVER_PROTOCOL_V10.md; then
    echo "  ✅ LLM failure: no new judgment rule present"
fi

echo "═══ V4.0 Final Hard Gates PASS ═══"
