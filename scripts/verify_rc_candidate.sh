#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v2.9.5-RC 发布前验证 ═══"

echo ""
echo "== Compile all =="
python3 -m compileall pipelines tests
echo "✅ compileall PASS"

echo ""
echo "== Core contract tests =="
python3 tests/test_core_contracts.py

echo ""
echo "== Pipeline smoke test =="
python3 tests/test_pipeline_smoke.py

echo ""
echo "== Pytest =="
if command -v pytest >/dev/null 2>&1; then
    pytest tests/test_core_contracts.py tests/test_pipeline_smoke.py -q
else
    echo "pytest not installed, skip"
fi

echo ""
echo "== Git diff check =="
git diff --check
echo "✅ no whitespace errors"

echo ""
echo "═══ RC verification PASS ═══"
