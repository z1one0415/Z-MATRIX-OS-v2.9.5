#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v1.1-A CI Audit Integration ═══"

echo "--- audit_golden_regression ---"
PYTHONPATH=. python3 scripts/skillos/audit_golden_regression.py

echo "--- audit_hash_aware_shadow ---"
PYTHONPATH=. python3 scripts/skillos/audit_hash_aware_shadow.py

echo "--- audit_golden_hash_lock ---"
PYTHONPATH=. python3 scripts/skillos/audit_golden_hash_lock.py

echo "--- v1.0-F golden regression tests ---"
PYTHONPATH=. python3 -m pytest -q tests/skillos/test_v1_0_f_golden_regression.py

echo "--- v1.0-E hash-aware shadow tests ---"
PYTHONPATH=. python3 -m pytest -q tests/skillos/test_v1_0_e_hash_aware_shadow.py

echo "--- v1.0-D golden hash lock tests ---"
PYTHONPATH=. python3 -m pytest -q tests/skillos/test_v1_0_d_golden_hash_lock.py

echo "--- v1.0-C hash scaffold tests ---"
PYTHONPATH=. python3 -m pytest -q tests/skillos/test_v1_0_c_hash_scaffold.py

echo "--- v1.0-B shadow audit tests ---"
PYTHONPATH=. python3 -m pytest -q tests/skillos/test_v1_0_b_shadow_audit.py

echo "--- v1.0-A contract registry tests ---"
PYTHONPATH=. python3 -m pytest -q tests/skillos/test_v1_0_a_contract_registry.py

echo "═══ Z-SkillOS v1.1-A CI Audit Integration PASS ═══"
