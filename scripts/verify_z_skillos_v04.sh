#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.4.1 Full Verify ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v03.sh
bash scripts/verify_z_skillos_v02.sh
bash scripts/verify_z_skillos_v01.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh

echo "═══ v0.4 Registry Safety Scan ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
skills=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
wl3=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v03.json').read_text())
wl4=json.loads(Path('data/research_db/agent/registry/skill_selection_whitelist_v04.json').read_text())
sm={s['skill_id']:s for s in skills}
for sid in wl3['selected_skills']+wl4['selected_skills']: assert sid in sm, f'missing:{sid}'
ids=[s['skill_id'] for s in skills]; assert len(ids)==len(set(ids)),'duplicate'
for s in skills:
 assert s.get('production_allowed') is False, s['skill_id']
 assert s.get('external_api_used') is not True, s['skill_id']
 assert s.get('trade_allowed') is not True, s['skill_id']
 assert s.get('verdict_allowed') is not True, s['skill_id']
 if s.get('write_layers'):
  assert s.get('requires_human_review') is True, s['skill_id']
  assert s.get('proposal_required') is True, s['skill_id']
print(f'registry safety PASS: {len(skills)} skills')
"

echo "═══ Ledger Empty Check (agent + governance) ═══"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f")
    [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "✅ All ledgers EMPTY"
echo "═══ Z-SkillOS v0.4.1 PASS ═══"
