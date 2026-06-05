#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.06 absorbed historical gate ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
python3 -c "
from zmatrix.agent.skill_domain_registry import R
c={d for d,p in R.items() if p}; f={d for d,p in R.items() if not p}
assert len(c)>=3,f'too few concrete: {len(c)}'
assert 'SYSTEM' in c,'SYSTEM missing'
print(f'v0.06 PASS: concrete={len(c)}')
"
