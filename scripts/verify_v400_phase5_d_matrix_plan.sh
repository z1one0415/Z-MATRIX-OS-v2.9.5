#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-5 D-Matrix Data Source Plan Verification ═══"
python3 -c "
from plans.d_matrix_data_source_plan.d_source_plan import D_FIELD_CAPABILITIES, D_PROXY_POLICY, D_ACCESS_PRIORITY
assert len(D_FIELD_CAPABILITIES)>=8
for f,cap in D_FIELD_CAPABILITIES.items():
    assert cap.get('availability'), f'{f} missing availability'
    assert cap.get('usable_for_production')==False, f'{f} marked production!'
assert D_PROXY_POLICY['usable_for_production']==False
assert D_PROXY_POLICY['not_original_data']==True
assert len(D_ACCESS_PRIORITY['P0_NOW'])>=2
print(f'  ✅ {len(D_FIELD_CAPABILITIES)} D-Matrix fields mapped')
print(f'  ✅ All production=BLOCKED')
print(f'  ✅ Proxy policy: research only')
print(f'  ✅ P0 priority fields: {len(D_ACCESS_PRIORITY[\"P0_NOW\"])}')
"
echo "═══ V4.0-5 D-Matrix Plan PASS ═══"
