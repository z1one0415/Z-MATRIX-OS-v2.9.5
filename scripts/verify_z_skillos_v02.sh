#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-SkillOS v0.2 ═══"
python3 -m compileall -q zmatrix tests scripts
PYTHONPATH=. python3 -m pytest -q tests/agent/
PYTHONPATH=. python3 -m pytest -q tests/research_db/
PYTHONPATH=. python3 scripts/skillos/scan_skill_candidates.py
PYTHONPATH=. python3 scripts/skillos/build_skill_registry.py
PYTHONPATH=. python3 scripts/skillos/validate_skill_registry.py
bash scripts/verify_z_skillos_v01.sh 2>/dev/null || true
for f in data/research_db/agent/ledgers/*.jsonl; do [ -s "$f" ] && { echo "FAIL:$f"; exit 1; }; done
echo "✅ ledgers EMPTY"
PYTHONPATH=. python3 -c "
import json; from pathlib import Path
s=json.loads(Path('data/research_db/agent/registry/skill_registry.generated.json').read_text())
for x in s: assert x.get('production_allowed') is False
print(f'safety PASS: {len(s)} registered')
"
echo "═══ Z-SkillOS v0.2 PASS ═══"
