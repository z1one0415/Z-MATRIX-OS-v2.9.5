#!/usr/bin/env bash
set -euo pipefail
echo "═══ V4.0 ALL PHASES VERIFICATION ═══"
py_compile() { python3 -m py_compile "$1" 2>/dev/null && echo "  ✅ $1" || { echo "  ❌ $1 compile failed"; exit 1; }; }
py_compile governance/data_source_capability_map/data_governance.py
py_compile governance/experiment_ledger/experiment_ledger.py
py_compile workbenches/b_matrix_current_snapshot/b_snapshot_schema.py
py_compile plans/d_matrix_data_source_plan/d_source_plan.py
bash scripts/verify_v400_phase0_platform_hardgate.sh
bash scripts/verify_v400_phase1_data_governance.sh
bash scripts/verify_v400_phase2_factor_registry.sh
bash scripts/verify_v400_phase3_experiment_os.sh
bash scripts/verify_v400_phase4_b_matrix_workbench.sh
bash scripts/verify_v400_phase5_d_matrix_plan.sh
echo "═══ V4.0 ALL 6 PHASES PASS ═══"
