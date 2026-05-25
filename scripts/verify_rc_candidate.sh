#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v2.9.6 RC Verification Gate ═══"
echo "RC target: v2.9.6-RC1"

echo ""
echo "== Safety boundary scan =="

python3 -c "
import ast, sys, os
from pathlib import Path

_FORBIDDEN = {'BUY', 'SELL', 'ADD', 'CLEAR', 'MARKET_ORDER', 'BROKER_ORDER', 'AUTO_TRADE', 'REAL_TRADE'}

def scan_file(path):
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except (SyntaxError, Exception):
        return []
    hits = []
    for node in ast.walk(tree):
        # 只检查 dict literal 中的 str key/value
        if isinstance(node, ast.Dict):
            for val in node.values:
                if isinstance(val, ast.Constant) and isinstance(val.value, str) and val.value in _FORBIDDEN:
                    # 检查这个 dict 是否在 action 相关位置(entry_intent/exit_intent/paper_action/action_cap)
                    for k in node.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                          and k.value in ('entry_intent', 'exit_intent', 'paper_action', 'action_cap', 'decision_outcome'):
                            hits.append((path, val.lineno, val.value))
                            break
    return hits

root = Path('$PWD')
scanned = 0
violations = []
for p in sorted((root / 'pipelines').rglob('*.py')) + sorted((root / 'zmatrix').rglob('*.py')):
    # 跳过Z-G16A纸面验证仓(paper adapter/BUY/SELL合法)
    if 'Z-G16A_Alpha' in str(p) or '__pycache__' in str(p):
        continue
    scanned += 1
    hits = scan_file(p)
    if hits:
        violations.extend(hits)

if violations:
    for path, lineno, token in violations:
        rel = os.path.relpath(str(path), str(root))
        print(f'  ❌ {rel}:{lineno} — {token}')
    print('❌ executable real trade token in action fields')
    sys.exit(1)
else:
    print(f'  ✅ scanned {scanned} .py files, 0 violations')
"

echo ""
echo "== RC contract files check =="

required_files=(
 "docs/release/RC_MANIFEST_v2.9.6.md"
 "docs/contracts/CONTRACT_INDEX_v2.9.6.md"
 "docs/release/RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md"
 "docs/contracts/Z9_CALIBRATION_POLICY_V10.md"
 "docs/contracts/examples/z9_calibration_policy_preview_v10_example.json"
)

for f in "${required_files[@]}"; do
 if [ ! -f "$f" ]; then
   echo "❌ missing required file: $f"
   exit 1
 fi
done
echo "✅ required RC files present"

echo ""
echo "== Compile all =="
python3 -m compileall pipelines tests zmatrix hermes scripts
echo "✅ compileall PASS"

echo ""
echo "== Core contract tests =="
python3 tests/test_core_contracts.py

echo ""
echo "== Pipeline smoke test =="
python3 tests/test_pipeline_smoke.py

echo ""
echo "== 18-pipeline manifest smoke =="
python3 tests/test_pipeline_manifest_smoke.py

echo ""
echo "== Type A horizontal tests =="
python3 tests/test_zg09_type_a_horizontal.py

echo ""
echo "== Z-G09/Z-G10 scorer contract tests =="
python3 tests/test_zg09_zg10_contracts.py

echo ""
echo "== B-Matrix v2.1.1 tests =="
python3 tests/test_b_matrix_v211.py

echo ""
echo "== Z-G13 B-Matrix integration tests =="
python3 tests/test_zg13_bmatrix_integration.py

echo ""
echo "== OHLCV data contract tests =="
python3 tests/test_data_contract_ohlcv.py

echo ""
echo "== Z-G03 intraday contract tests =="
python3 tests/test_zg03_intraday_contract.py

echo ""
echo "== Pytest =="
if command -v pytest >/dev/null 2>&1; then
    pytest tests/test_core_contracts.py tests/test_pipeline_smoke.py \
        tests/test_pipeline_manifest_smoke.py tests/test_zg09_zg10_contracts.py \
        tests/test_zg09_type_a_horizontal.py tests/test_b_matrix_v211.py \
        tests/test_zg13_bmatrix_integration.py tests/test_data_contract_ohlcv.py \
        tests/test_zg03_intraday_contract.py tests/test_capability_mask_contract.py tests/test_zg10_payload_ohlcv.py tests/test_intraday_tail_precision_flags.py tests/test_zg13_financial_coverage.py tests/test_universe_provider.py tests/test_global_pipelines_universe_contract.py tests/test_zg07_contracts.py tests/test_zg14_matrix_reliability.py tests/test_chain_taxonomy_provider.py tests/test_bmatrix_input_builder.py tests/test_l25_macro_contract.py tests/test_z9_calibration_contract.py tests/test_zg11_account_truth.py tests/test_zg18_core.py tests/test_zg01_covers_zg07_data_channels.py tests/test_zg14_uses_rmatrix_service.py tests/test_zg18_g09_constraint_consistency.py tests/test_rmatrix_service_v20_four_king.py tests/test_rmatrix_service_degraded_contract.py tests/test_zg09_uses_rmatrix_service_only.py tests/test_g09_g14_rmatrix_consistency.py tests/test_rmatrix_contract_schema.py tests/test_g18_final_decision_envelope_v11.py tests/test_g18_upstream_evidence_aggregation.py tests/test_g18_conflict_resolver.py tests/test_g18_paper_execution_record.py tests/test_z9_calibration_sample_contract.py tests/test_z9_ingestion_queue_contract.py tests/test_z9_outcome_backfill_contract.py tests/test_z9_calibration_policy_contract.py tests/test_rc_verification_gate.py -q
else
    echo "pytest not installed, skip"
fi

echo ""
echo "== capability mask contract tests =="
python3 tests/test_capability_mask_contract.py

echo ""
echo "== Z-G10 OHLCV payload tests =="
python3 tests/test_zg10_payload_ohlcv.py

echo ""
echo "== Precision flags tests =="
python3 tests/test_intraday_tail_precision_flags.py

echo ""
echo "== Z-G13 financial coverage tests =="
python3 tests/test_zg13_financial_coverage.py

echo ""
echo "== UniverseProvider tests =="
python3 tests/test_universe_provider.py

echo ""
echo "== Global pipelines universe contract tests =="
python3 tests/test_global_pipelines_universe_contract.py

echo ""
echo "== Z-G07 contracts tests =="
python3 tests/test_zg07_contracts.py

echo ""
echo "== Z-G14 matrix reliability tests =="
python3 tests/test_zg14_matrix_reliability.py

echo ""
echo "== Chain taxonomy provider tests =="
python3 tests/test_chain_taxonomy_provider.py

echo ""
echo "== BMatrix input builder tests =="
python3 tests/test_bmatrix_input_builder.py

echo ""
echo "== L2.5 macro contract tests =="
python3 tests/test_l25_macro_contract.py

echo ""
echo "== Z9 calibration contract tests =="
python3 tests/test_z9_calibration_contract.py

echo ""
echo "== Z-G11 account truth tests =="
python3 tests/test_zg11_account_truth.py

echo ""
echo "== Z-G18 Tianji engine tests =="
python3 tests/test_zg18_core.py

echo ""
echo "== Z-G09 sell decision tests =="
python3 tests/test_zg09_sell_decision.py

echo ""
echo "== Z-G07 data channel tests =="
python3 tests/test_zg01_covers_zg07_data_channels.py

echo ""
echo "== Z-G14 R-Matrix service tests =="
python3 tests/test_zg14_uses_rmatrix_service.py

echo ""
echo "== Z-G18 constraint consistency tests =="
python3 tests/test_zg18_g09_constraint_consistency.py

echo ""
echo "== R-Matrix v2.0 four-king tests =="
python3 tests/test_rmatrix_service_v20_four_king.py

echo ""
echo "== R-Matrix degraded contract tests =="
python3 tests/test_rmatrix_service_degraded_contract.py

echo ""
echo "== Z-G09 r_matrix_service-only tests =="
python3 tests/test_zg09_uses_rmatrix_service_only.py

echo ""
echo "== G09/G14 R-Matrix consistency tests =="
python3 tests/test_g09_g14_rmatrix_consistency.py

echo ""
echo "== R-Matrix contract schema tests =="
python3 tests/test_rmatrix_contract_schema.py

echo ""
echo "== G18 Final Decision Envelope v1.1 tests =="
python3 tests/test_g18_final_decision_envelope_v11.py

echo ""
echo "== G18 upstream evidence aggregation tests =="
python3 tests/test_g18_upstream_evidence_aggregation.py

echo ""
echo "== G18 conflict resolver tests =="
python3 tests/test_g18_conflict_resolver.py

echo ""
echo "== G18 paper execution record tests =="
python3 tests/test_g18_paper_execution_record.py

echo ""
echo "== Z9 calibration sample contract tests =="
python3 tests/test_z9_calibration_sample_contract.py

echo ""
echo "== Z9 ingestion queue contract tests =="
python3 tests/test_z9_ingestion_queue_contract.py

echo ""
echo "== Z9 outcome backfill contract tests =="
python3 tests/test_z9_outcome_backfill_contract.py

echo ""
echo "== Z9 calibration policy contract tests =="
python3 tests/test_z9_calibration_policy_contract.py

echo ""
echo "== RC verification gate tests =="
python3 tests/test_rc_verification_gate.py
echo ""
echo "== Git diff check =="
git diff --check
echo "✅ no whitespace errors"

echo ""
echo "== Git clean check =="
if [ -n "$(git status --short)" ]; then
    echo "❌ working tree not clean"
    git status --short
    exit 1
fi
echo "✅ working tree clean"

echo ""
echo "═══ RC verification PASS ═══"
