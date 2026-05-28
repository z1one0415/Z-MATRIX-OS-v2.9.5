#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-4 B-Matrix Workbench Verification ═══"
python3 -c "
from workbenches.b_matrix_current_snapshot.b_snapshot_schema import B_SNAPSHOT_FIELDS, B_TIERS, B_SNAPSHOT_PERMISSIONS, BSnapshotItem
assert len(B_SNAPSHOT_FIELDS)>=10
assert len(B_TIERS)>=3
assert B_SNAPSHOT_PERMISSIONS['production']=='BLOCKED'
assert B_SNAPSHOT_PERMISSIONS['historical_pit']=='BLOCKED_DATA_INSUFFICIENT'
bs=BSnapshotItem(ticker='000001',name='test',b_score=80,tier='B_CORE_STRONG')
assert bs.real_trade_allowed==False
assert bs.production_allowed==False
print(f'  ✅ {len(B_SNAPSHOT_FIELDS)} snapshot fields')
print(f'  ✅ {len(B_TIERS)} tiers')
print(f'  ✅ Historical PIT: BLOCKED')
print(f'  ✅ Production: BLOCKED')
"
echo "═══ V4.0-4 B-Matrix Workbench PASS ═══"
