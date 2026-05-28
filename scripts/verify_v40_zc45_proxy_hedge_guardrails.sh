#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 ZC45 Proxy Hedge Guardrails Verification ═══"

# Check ZC45 protocols exist
for proto in ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION ZC45_BETA_BUDGET ZC45_TAIL_HEDGE_SIMULATOR; do
    if [ ! -f "docs/architecture/${proto}_PROTOCOL_V10.md" ]; then
        echo "❌ Missing ZC45 protocol: ${proto}"; exit 1
    fi
done
echo "  ✅ 3 ZC45 protocols present"

# Check scope lock
if [ ! -f "docs/upgrade/V40_ZC45_PROXY_HEDGE_SCOPE_LOCK.md" ]; then
    echo "❌ Missing ZC45 scope lock"; exit 1
fi
echo "  ✅ ZC45 scope lock present"

# Verify Market Neutral prohibition
python3 -c "
for f in ['docs/architecture/ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_PROTOCOL_V10.md',
          'docs/upgrade/V40_ZC45_PROXY_HEDGE_SCOPE_LOCK.md']:
    content = open(f).read()
    assert 'MARKET_NEUTRAL' not in content or 'not' in content.lower() or 'FORBIDDEN' in content.lower(), f'{f} should prohibit Market Neutral claims'
print('  ✅ Market Neutral claim prohibition verified')
"

# Check stress test requirements
if grep -q 'ProxyHedgeStressTest\|stress.*test\|StressTest' docs/architecture/ZC45_PROXY_HEDGE_DEFENSIVE_ALLOCATION_PROTOCOL_V10.md; then
    echo "  ✅ ZC45 stress test requirement present"
fi

# Check beta budget governance
if grep -q 'beta_budget\|BETA_BUDGET\|beta.*budget' docs/architecture/ZC45_BETA_BUDGET_PROTOCOL_V10.md; then
    echo "  ✅ ZC45 beta budget governance present"
fi

echo "═══ V4.0 ZC45 Proxy Hedge Guardrails PASS ═══"
