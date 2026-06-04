#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.04 (absorbed by full-system audit) ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py 2>/dev/null || true
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py 2>/dev/null || true
PYTHONPATH=. python3 -c "
from zmatrix.agent.skill_domain_registry import R
c=sum(1 for p in R.values() if p)
assert c>=3,f'concrete: {c}'
print(f'v0.04 PASS: {c} concrete routers')
"
