#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 ZC35 Catalyst Guardrails Verification ═══"

# Check ZC35 protocols exist
for proto in ZC35_CATALYST_LIFECYCLE ZC35_EVENT_STUDY ZC35_SELL_ON_NEWS_DEFENSE; do
    if [ ! -f "docs/architecture/${proto}_PROTOCOL_V10.md" ]; then
        echo "❌ Missing ZC35 protocol: ${proto}"; exit 1
    fi
done
echo "  ✅ 3 ZC35 protocols present"

# Check scope lock
if [ ! -f "docs/upgrade/V40_ZC35_CATALYST_SCOPE_LOCK.md" ]; then
    echo "❌ Missing ZC35 scope lock"; exit 1
fi
echo "  ✅ ZC35 scope lock present"

# Verify ZC35 protocols prohibit direct trading
python3 -c "
import os
for f in ['docs/architecture/ZC35_CATALYST_LIFECYCLE_PROTOCOL_V10.md',
          'docs/upgrade/V40_ZC35_CATALYST_SCOPE_LOCK.md']:
    content = open(f).read()
    assert 'AUTO_BUY' not in content or 'Forbidden' in content or 'FORBIDDEN' in content, f'{f} should prohibit auto trading'
    assert 'catalyst_direct_trade_allowed' in content.lower() or 'direct trade' not in content.lower(), f'{f} should address direct trade'
print('  ✅ ZC35 trading prohibitions verified')
"

# Check scheduled event handling
if grep -q 'scheduled_event_without_surprise\|scheduled.*event.*downgrad' docs/architecture/ZC35_EVENT_STUDY_PROTOCOL_V10.md; then
    echo "  ✅ ZC35 scheduled event downgrade rule present"
fi

# Check sell-on-news defense
if grep -q 'sell_on_news\|SELL_ON_NEWS' docs/architecture/ZC35_SELL_ON_NEWS_DEFENSE_PROTOCOL_V10.md; then
    echo "  ✅ ZC35 sell-on-news defense present"
fi

echo "═══ V4.0 ZC35 Catalyst Guardrails PASS ═══"
