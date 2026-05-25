#!/usr/bin/env bash
set -euo pipefail

echo "═══ Z-MATRIX-OS v2.9.7-dev Architecture Verification Gate ═══"
echo "Target: v2.9.7-dev / Batch F (Complete Closure)"

echo ""
echo "== Build Architecture Package Manifest =="
python3 scripts/build_architecture_package_manifest.py

echo ""
echo "== Compile =="
python3 -m compileall zmatrix tests scripts pipelines
echo "✅ compileall PASS"

echo ""
echo "== Shared Skill Registry tests =="
python3 tests/test_shared_skill_registry.py

echo ""
echo "== Pipeline Registry tests =="
python3 tests/test_pipeline_registry.py

echo ""
echo "== Gate Registry tests =="
python3 tests/test_gate_registry.py

echo ""
echo "== Workflow DAG tests =="
python3 tests/test_workflow_dag.py

echo ""
echo "== Architecture Enforcement tests =="
python3 tests/test_architecture_enforcement.py

echo ""
echo "== Cross-Pipeline Conflict Audit tests =="
python3 tests/test_cross_pipeline_conflict_audit.py

echo ""
echo "== System Controller MVP tests =="
python3 tests/test_system_controller_mvp.py

echo ""
echo "== Architecture Package tests =="
python3 tests/test_architecture_package.py

echo ""
echo "== Existing RC safety gate smoke =="
python3 tests/test_rc_verification_gate.py
python3 tests/test_rc_packaging.py

echo ""
echo "== Git diff check =="
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
 git diff --check
else
 echo "(non-git workspace, skip git diff check)"
fi

echo ""
echo "== Git clean check =="
if [ -n "$(git status --short 2>/dev/null)" ]; then
 echo "❌ working tree not clean (local repo)"
 git status --short
 exit 1
fi
echo "✅ working tree clean"

echo ""
echo "═══ Architecture verification PASS ═══"
