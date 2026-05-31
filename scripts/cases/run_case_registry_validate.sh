#!/usr/bin/env bash
set -euo pipefail; cd "$(cd "$(dirname "$0")/../.." && pwd)"
echo "═══ Case Registry Validation ═══"
python3 -c "
import csv, json
cases=list(csv.DictReader(open('data/research_db/cases/case_registry_v1.csv')))
print(f'Total: {len(cases)}')
assert len(cases)>=100
for c in cases:
    assert c['allowed_in_real_trade']=='FALSE', f'{c["case_id"]}: real_trade!'
core=[c for c in cases if c['case_layer']=='CORE']; exp=[c for c in cases if c['case_layer']=='EXPANSION']; fail=[c for c in cases if c['case_layer']=='FAILURE']
print(f'CORE:{len(core)} EXP:{len(exp)} FAIL:{len(fail)} real_trade:0')
print('✅ PASS')
"
echo "═══ Case Registry Validation PASS ═══"
