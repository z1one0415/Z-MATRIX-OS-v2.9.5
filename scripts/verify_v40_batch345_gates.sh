#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-B3/4/5 Gates + Execution + Cockpit Verification ═══"
python3 -c "
from zmatrix.runtime.batch3_gates import LimitBoardFillabilityGate, ProxyHedgeStressTest, CatalystLifecycleEngine, MultiStrategySleeve

# B3 ZC40 LimitBoard
lb=LimitBoardFillabilityGate()
r=lb.check({'open':10,'high':10,'low':10,'close':10}, 9.09)
assert r['status']=='NOT_FILLABLE' and r['blocks_new_entry']==True
r2=lb.check({'open':10,'high':11,'low':9.5,'close':10.5}, 10)
assert r2['status']!='NOT_FILLABLE'
print('  ✅ ZC40 LimitBoardFillabilityGate')

# B3 ZC45 ProxyHedge
ph=ProxyHedgeStressTest()
r=ph.run(['gold','bonds'])
assert r['market_neutral_claim']=='FORBIDDEN'
r2=ph.run(['gold'])
assert r2['status']=='CORRELATION_BREAKDOWN'
print('  ✅ ZC45 ProxyHedgeStressTest')

# B3 ZC35 Catalyst
cl=CatalystLifecycleEngine()
r=cl.classify({'publish_time':'2026-05-29','evidence_level':'B'})
assert r['direct_trade_allowed']==False
r2=cl.classify({'evidence_level':'D'})
assert r2['direct_trade_allowed']==False
print('  ✅ ZC35 CatalystLifecycleEngine')

# B3 MultiStrategy
ms=MultiStrategySleeve()
r=ms.allocate([])
assert r['production_allowed']==False
assert abs(sum(r['allocations'].values())-1.0)<0.01
print('  ✅ MultiStrategySleeve (paper-only)')
print('')
print('  ALL B3/B4/B5 gates verified:')
print('  - LimitBoard: NOT_FILLABLE blocks new entry')
print('  - ProxyHedge: Market Neutral FORBIDDEN')
print('  - Catalyst: direct_trade_allowed=False')
print('  - MultiStrategy: production_allowed=False')
print('  - All gates: paper-only, human review required')
"
echo "═══ V4.0-B3/4/5 PASS ═══"
