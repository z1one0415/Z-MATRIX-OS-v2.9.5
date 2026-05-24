#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v2.9.6-BatchA ═══"

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
        tests/test_zg03_intraday_contract.py tests/test_capability_mask_contract.py tests/test_zg10_payload_ohlcv.py tests/test_intraday_tail_precision_flags.py tests/test_zg13_financial_coverage.py tests/test_universe_provider.py tests/test_global_pipelines_universe_contract.py tests/test_zg07_contracts.py tests/test_zg14_matrix_reliability.py tests/test_chain_taxonomy_provider.py tests/test_bmatrix_input_builder.py tests/test_l25_macro_contract.py tests/test_z9_calibration_contract.py tests/test_zg11_account_truth.py tests/test_zg18_core.py tests/test_zg01_covers_zg07_data_channels.py tests/test_zg14_uses_rmatrix_service.py tests/test_zg18_g09_constraint_consistency.py tests/test_rmatrix_service_v20_four_king.py tests/test_rmatrix_service_degraded_contract.py tests/test_zg09_uses_rmatrix_service_only.py tests/test_g09_g14_rmatrix_consistency.py tests/test_rmatrix_contract_schema.py tests/test_g18_final_decision_envelope_v11.py -q
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
