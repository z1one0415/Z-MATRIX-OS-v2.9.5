#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS Full System vFS.11 Verify ═══"

echo "═══ Script Presence Gate ═══"
for vs in verify_z_skillos_v10 verify_z_skillos_v09 verify_z_skillos_v08 verify_z_skillos_v07 verify_z_skillos_v06 verify_z_skillos_v05 verify_z_skillos_v04 verify_z_skillos_v03 verify_z_skillos_v02 verify_z_skillos_v01 verify_zg16_full_stub_integration verify_z_agent_kernel; do
    [ -f "scripts/${vs}.sh" ] || { echo "FAIL: missing scripts/${vs}.sh"; exit 1; }
done
echo "All scripts present"

python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py

echo "═══ Full Verify Chain ═══"
for vs in verify_z_skillos_v10 verify_z_skillos_v09 verify_z_skillos_v08 verify_z_skillos_v07; do
    echo "--- $vs local gates ---"
    Z_SKILLOS_FLAT_VERIFY=1 bash "scripts/${vs}.sh"
done

echo "═══ Historical / Integration Verify Chain ═══"
for vs in verify_z_skillos_v06 verify_z_skillos_v05 verify_z_skillos_v04 verify_z_skillos_v03 verify_z_skillos_v02 verify_z_skillos_v01 verify_zg16_full_stub_integration verify_z_agent_kernel; do
    echo "--- $vs ---"
    bash "scripts/${vs}.sh"
done

echo "═══ Registry Domain Audit ═══"
python3 << 'PYEOF'
import json; from pathlib import Path
from zmatrix.agent.skill_domain_registry import R as routers
s=json.loads(Path("data/research_db/agent/registry/skill_registry.generated.json").read_text())
exp={"SYSTEM","ZG16","CASEFORGE","REPORT","COCKPIT","RESEARCHDB","DATAFORGE","AUTOCASE","MEMORY","GOVERNANCE","FACTOR","COUNCIL","ZC35","BMATRIX","DMATRIX","PORTFOLIO","WORKFLOW"}
crt={d for d,p in routers.items() if p}; fwk={d for d,p in routers.items() if not p}
assert crt==exp and fwk==set() and len(s)>=104
ids=[x["skill_id"] for x in s]; assert len(ids)==len(set(ids))
ro={"R0_READ":0,"R1_ANNOTATE":1,"R2_DRAFT":2}
for x in s:
    rvl=x.get("risk_level","R0_READ"); assert ro.get(rvl,99)<=2,f"{x['skill_id']}:{rvl}"
    if x.get("write_layers"): assert x.get("requires_human_review") and x.get("proposal_required"),x["skill_id"]
print(f"PASS: {len(s)} skills {len(crt)} concrete")
PYEOF

echo "═══ Doc Section Gate ═══"
python3 << 'PYEOF'
from pathlib import Path
r={"docs/skillos/Z_SKILLOS_FULL_SYSTEM_CLOSEOUT.md":18,"docs/skillos/Z_SKILLOS_FULL_SYSTEM_INTEGRATION_AUDIT.md":18,"docs/skillos/Z_SKILLOS_MERGE_READINESS_FINAL.md":7}
for p,m in r.items():
    c=sum(1 for l in Path(p).read_text().splitlines() if l.startswith("## "))
    assert c>=m,f"{p}:{c}<{m}"
print(f"doc gate PASS")
PYEOF

echo "═══ Ledger Empty ═══"
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f")
    [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done

echo "═══ Workspace Clean Gate ═══"
dirty="$(git status --short --untracked-files=all)"
if [ -n "$dirty" ]; then
    echo "$dirty"
    echo "FAIL: verify left workspace dirty"
    exit 1
fi

echo "═══ Z-SkillOS Full System vFS.11 PASS ═══"
