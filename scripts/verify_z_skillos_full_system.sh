#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS Full System Closeout Verify ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
for vs in verify_z_skillos_v10 verify_z_skillos_v09 verify_z_skillos_v08 verify_z_skillos_v07 verify_z_skillos_v06 verify_z_skillos_v05 verify_z_skillos_v04 verify_z_skillos_v03 verify_z_skillos_v02 verify_z_skillos_v01 verify_zg16_full_stub_integration verify_z_agent_kernel; do
    echo "--- $vs ---"
    bash "scripts/${vs}.sh" || { echo "FAIL:$vs"; exit 1; }
done
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f")
    [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
PYTHONPATH=. python3 -c "
from zmatrix.agent.skill_domain_registry import R as routers
import json; from pathlib import Path
skills=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
concrete={d for d,p in routers.items() if p}
framework={d for d,p in routers.items() if not p}
assert len(concrete)==17
assert len(framework)==0
print(f'Skills:{len(skills)} Concrete:{len(concrete)} Framework:{len(framework)} PASS')
"
echo "═══ Z-SkillOS Full System PASS ═══"
