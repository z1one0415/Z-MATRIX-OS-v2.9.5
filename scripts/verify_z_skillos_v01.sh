#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.1.2 ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
echo "--- Full Chain Verify ---"
for vs in verify_zg16_full_stub_integration verify_z_agent_kernel; do
    if [ -f "scripts/${vs}.sh" ]; then bash "scripts/${vs}.sh" || { echo "FAIL:$vs"; exit 1; }; fi
done
echo "═══ Ledger Empty Check ═══"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue
    base=$(basename "$f"); [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "✅ All ledgers EMPTY"
PYTHONPATH=. python3 -c "
from pathlib import Path; import json
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
for x in s: assert x.get('production_allowed') is False, x['skill_id']
c=json.loads(Path('data/research_db/agent/registry/skill_candidate_index.json').read_text())
for x in c: assert x['status']=='CANDIDATE_ONLY' and x['production_allowed'] is False
print(f'safety PASS: {len(s)} registered, {len(c)} candidates')
"
echo "═══ Z-SkillOS v0.1.2 PASS ═══"
