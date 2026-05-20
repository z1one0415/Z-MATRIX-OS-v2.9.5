#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v2.9.5-RC 发布前验证 ═══"

echo ""
echo "== Compile all =="
python -m compileall pipelines tests 2>/dev/null && echo "✅ compileall PASS" || echo "❌ compileall FAIL"

echo ""
echo "== Core contract tests =="
python tests/test_core_contracts.py 2>&1 | tail -3

echo ""
echo "== Pipeline smoke test =="
python tests/test_pipeline_smoke.py 2>&1 | tail -3

echo ""
echo "== Pytest =="
if command -v pytest >/dev/null 2>&1; then
    pytest tests/test_core_contracts.py tests/test_pipeline_smoke.py -q 2>&1 | tail -5
else
    echo "pytest not installed, skip"
fi

echo ""
echo "== Git diff check =="
git diff --check 2>/dev/null && echo "✅ no whitespace errors" || true

echo ""
echo "═══ Done ═══"
