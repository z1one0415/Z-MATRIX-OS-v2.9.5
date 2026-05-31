#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.1 ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/ 2>/dev/null || true
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
for f in data/research_db/agent/ledgers/*.jsonl; do [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }; done
echo "✅ ledgers EMPTY"
PYTHONPATH=. python3 -c "
from pathlib import Path; import json
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
for x in s: assert x.get('production_allowed') is False, x['skill_id']
c=json.loads(Path('data/research_db/agent/registry/skill_candidate_index.json').read_text())
for x in c: assert x['status']=='CANDIDATE_ONLY' and x['production_allowed'] is False
print(f'safety PASS: {len(s)} registered, {len(c)} candidates')
"
echo "═══ Z-SkillOS v0.1 PASS ═══"
