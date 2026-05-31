#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.4 ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v03.sh
bash scripts/verify_z_skillos_v02.sh
bash scripts/verify_z_skillos_v01.sh
for f in data/research_db/agent/ledgers/*.jsonl data/research_db/governance/*.jsonl; do
    [ ! -f "$f" ] && continue; base=$(basename "$f"); [ "$base" = "data_source_attribution_ledger.csv" ] && continue
    [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }
done
echo "✅ ledgers EMPTY"
echo "═══ Z-SkillOS v0.4 PASS ═══"
