#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0-2 Factor Registry Verification ═══"
python3 -c "
import json
r=json.load(open('governance/factor_registry/initial_factor_registry.json'))
fs=r['factors']; assert len(fs)>=15, f'too few factors: {len(fs)}'
for f in fs:
    assert f.get('factor_id'), f'missing id: {f}'
    assert f.get('matrix_layer'), f'{f[\"factor_id\"]} missing matrix_layer'
    assert f.get('pit_safe'), f'{f[\"factor_id\"]} missing pit_safe'
    assert f.get('trust_level'), f'{f[\"factor_id\"]} missing trust_level'
    assert f.get('production_allowed')==False, f'{f[\"factor_id\"]} production_allowed!'
# B historical pit blocked
bhist=[f for f in fs if 'historical_pit' in f['factor_id']]
assert bhist and bhist[0]['trust_level']=='BLOCKED'
assert bhist[0]['production_allowed']==False
# D factors missing
dfs=[f for f in fs if f['factor_id'].startswith('d_')]
for d in dfs:
    assert d['trust_level'] in ('MISSING','BLOCKED'), f'{d[\"factor_id\"]} should be MISSING'
    assert d['production_allowed']==False
print(f'  ✅ {len(fs)} factors registered')
print(f'  ✅ All matrix_layer + pit_safe + trust_level present')
print(f'  ✅ All production_allowed=False')
print(f'  ✅ B historical PIT: BLOCKED')
print(f'  ✅ D factors ({len(dfs)}): MISSING')
"
echo "═══ V4.0-2 Factor Registry PASS ═══"
