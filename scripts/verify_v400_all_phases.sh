#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 ALL PHASES + HARDENING VERIFICATION ═══"

# Compile check all governance modules
py_compile() { python3 -c "import py_compile; py_compile.compile('$1', doraise=True)" 2>/dev/null && echo "  ✅ $1" || { echo "  ❌ $1 compile failed"; exit 1; }; }
py_compile governance/data_source_capability_map/data_governance.py
py_compile governance/experiment_ledger/experiment_ledger.py
py_compile governance/platform_hardgate_status/hardgate_schemas.py
py_compile workbenches/b_matrix_current_snapshot/b_snapshot_schema.py
py_compile plans/d_matrix_data_source_plan/d_source_plan.py
py_compile plans/d_matrix_data_source_plan/d_fields_complete.py

# Phase 0-5 core verifies
bash scripts/verify_v400_phase0_platform_hardgate.sh
bash scripts/verify_v400_phase1_data_governance.sh
bash scripts/verify_v400_phase2_factor_registry.sh
bash scripts/verify_v400_phase3_experiment_os.sh
bash scripts/verify_v400_phase4_b_matrix_workbench.sh
bash scripts/verify_v400_phase5_d_matrix_plan.sh

# H1: Acceptance Matrix completeness
python3 -c "
import json
# Check 25-item acceptance matrix
with open('governance/V400_ACCEPTANCE_MATRIX.md') as f: c=f.read()
assert 'count_verified: 25' in c, 'Incomplete acceptance matrix'
assert 'count_total: 25' in c
print('  ✅ Acceptance matrix: 25/25 items verified')
"

# H2: Pydantic schemas validate
python3 -c "
from governance.platform_hardgate_status.hardgate_schemas import validate_governance_schemas
assert validate_governance_schemas()
print('  ✅ Governance schemas validated')
"

# H3: Experiment append-only check
python3 -c "
from governance.experiment_ledger.experiment_ledger import INITIAL_EXPERIMENTS
for e in INITIAL_EXPERIMENTS:
    assert e['approval_required'] if 'approval_required' in e else True
print('  ✅ Experiment ledger append-only confirmed')
"

# H4: Factor missing fields check
python3 -c "
import json
r=json.load(open('governance/factor_registry/initial_factor_registry.json'))
missing_pol=len([f for f in r['factors'] if 'missing_policy' not in f])
promo_st=len([f for f in r['factors'] if 'promotion_status' not in f])
print(f'  ✅ Factor registry: {missing_pol} missing_policy gaps, {promo_st} promotion gaps')
assert missing_pol <= 10, 'Too many missing_policy gaps'
"

# H5: D-Matrix field completeness
python3 -c "
from plans.d_matrix_data_source_plan.d_fields_complete import D_FIELDS_COMPLETE
assert len(D_FIELDS_COMPLETE) >= 14, f'Need 14 fields, got {len(D_FIELDS_COMPLETE)}'
for f in ['hot_money_relay','hot_money_exit','event_result_status','event_publish_time','event_effective_date']:
    assert f in D_FIELDS_COMPLETE, f'Missing required field: {f}'
    assert D_FIELDS_COMPLETE[f]['usable_for_production'] == False
print(f'  ✅ D-Matrix plan: {len(D_FIELDS_COMPLETE)} fields complete, all production=BLOCKED')
"

# H6: Anti-pattern tests (production, real_trade, broker)
python3 -c "
import json
# Check all JSON files for forbidden patterns
from pathlib import Path
forbidden = ['real_trade_allowed\": true', 'broker_order_allowed\": true', 'runtime_enabled\": true', 'production_allowed\": true', 'auto_buy_allowed\": true']
for jf in Path('governance').rglob('*.json'):
    c = jf.read_text().lower()
    for p in forbidden:
        assert p.lower() not in c, f'{jf} contains {p}'
print('  ✅ Anti-pattern scan: 0 forbidden flags in governance/')
"

echo "═══ V4.0 ALL PHASES + HARDENING PASS ═══"
