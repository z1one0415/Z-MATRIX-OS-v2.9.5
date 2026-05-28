#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-1 Data Governance Verification ═══"

# Check data governance module
python3 -c "
from governance.data_source_capability_map.data_governance import DATA_SOURCE_REGISTRY, PIT_POLICIES, TTL_POLICIES, MISSING_POLICIES
# Registry exists
assert len(DATA_SOURCE_REGISTRY) >= 6, 'registry too small'
# All sources have pit_safe
for sid, s in DATA_SOURCE_REGISTRY.items():
    assert s.get('pit_safe'), f'{sid} missing pit_safe'
    assert 'usable_for_production' in s, f'{sid} missing prod flag'
# B historical pit blocked
b_hist = DATA_SOURCE_REGISTRY.get('b_historical_pit_financial',{})
assert b_hist.get('usable_for_backtest') == False, 'B hist should not be backtestable'
assert b_hist.get('status','') == 'BLOCKED_DATA_INSUFFICIENT'
# D event missing
d_evt = DATA_SOURCE_REGISTRY.get('d_event_flow_theme',{})
assert d_evt.get('usable_for_backtest') == False, 'D should not be backtestable'
assert d_evt.get('status','') == 'MISSING'
# Broker blocked
brk = DATA_SOURCE_REGISTRY.get('broker_runtime',{})
assert brk.get('usable_for_production') == False, 'broker must not be production'
assert brk.get('status','') == 'BLOCKED'
# No source production-ready
for sid, s in DATA_SOURCE_REGISTRY.items():
    assert s.get('usable_for_production') != True, f'{sid} marked production-ready!'
print('  ✅ Data source registry valid')
print('  ✅ B historical PIT blocked')
print('  ✅ D event/flow/theme missing')
print('  ✅ Broker/runtime blocked')
print('  ✅ 0 sources production-ready')
"
echo "═══ V4.0-1 Data Governance PASS ═══"
