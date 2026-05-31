#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.2.1 First Domain Batch Verify ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v01.sh
bash scripts/verify_zg16_full_stub_integration.sh
bash scripts/verify_z_agent_kernel.sh
echo "═══ Ledger Empty Check (agent + governance) ═══"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue
    base=$(basename "$f"); [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "✅ All ledgers EMPTY"
echo "═══ Full Safety Scan ═══"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
forbidden={'external_api_used':True,'shadowbroker_deployed':True,'production_allowed':True,'trade_allowed':True,'verdict_allowed':True,'broker_order_allowed':True,'real_trade_allowed':True,'auto_buy_allowed':True,'auto_sell_allowed':True}
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
for x in s:
    for k,v in forbidden.items():
        assert x.get(k) is not True, f'{x[\"skill_id\"]}: {k}=true'
    if x.get('write_layers'):
        assert x.get('requires_human_review') is True, f'{x[\"skill_id\"]}: write skill no review'
        assert x.get('proposal_required') is True, f'{x[\"skill_id\"]}: write skill no proposal'
ids=[x['skill_id'] for x in s]; assert len(ids)==len(set(ids)),'duplicate id'
print(f'safety PASS: {len(s)} skills')
"
echo "═══ Z-SkillOS v0.2.1 PASS ═══"
