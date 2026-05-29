#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 Hardening-C2.1 Truth/Asset/Matrix Closeout ═══"
python3 -c "
from pathlib import Path
t=Path('docs/release/V40_CLOSEOUT_TRUTH_REPORT.md').read_text(encoding='utf-8')
m=Path('docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md').read_text(encoding='utf-8')
a=Path('docs/upgrade/V40_CONTENT_ASSET_INDEX.md').read_text(encoding='utf-8')
for text in [t,m,a]:
    assert 'INTEGRATION_SMOKE_CANDIDATE' in text; assert 'NOT_APPROVED' in text
    assert 'BLOCKED' in text
for line in m.splitlines():
    if line.startswith('| HC-'):
        assert '| ACCEPTANCE_DONE |' not in line, f'False ACCEPTANCE_DONE: {line}'
for fb in ['RC1_APPROVED','PRODUCTION_READY','BROKER_READY','RUNTIME_READY']:
    assert fb not in t+m+a, f'Forbidden: {fb}'
required={'ZC20_DATAFORGE':'DEPTH_PARTIAL','ZC30_FACTOR_FACTORY':'DEPTH_PARTIAL','ZC40_EXECUTION_QUALITY':'DEPTH_PARTIAL','ZC50_ACCOUNT_GOVERNANCE':'DEPTH_PARTIAL','ZSC_AUDIT_EXPORT':'MINIMAL_CORE_DONE','IRF_01_03_04':'INTEGRATION_SMOKE_DONE'}
for aid,s in required.items():
    for l in a.splitlines():
        if aid in l: assert s in l, f'{aid} should be {s}'; break
print('  ✅ Truth/Asset/Matrix synchronized + 0 ACCEPTANCE_DONE rows')
"
echo "═══ V4.0 Hardening-C2.1 Closeout PASS ═══"
