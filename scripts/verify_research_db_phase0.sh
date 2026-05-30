#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 0 Verification ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/research_db/ tests/research_db/ 2>&1 | tail -1

echo "[1] Docs..."
for f in RESEARCH_DB_CONSTITUTION.md DATA_TRUST_LEVEL_POLICY.md PIT_SAFETY_POLICY.md OUTCOME_HORIZON_POLICY.md DATA_SOURCE_CAPABILITY_POLICY.md RESEARCH_DB_PROMOTION_POLICY.md NO_PRODUCTION_BOUNDARY.md RESEARCH_DB_DIRECTORY_STANDARD.md; do
  test -f "docs/research_db/$f" || { echo "❌ missing doc: $f"; exit 1; }
done
echo "  ✅ 8 docs"

echo "[2] Manifest..."
python3 -c "
import json; m=json.load(open('docs/research_db/PHASE0_MACHINE_MANIFEST.json'))
assert m['production_allowed']==False; assert m['next_phase_allowed_by_machine']==False
assert m['human_approval_required']==True
print('  ✅ manifest valid')
"

echo "[3] Data directories..."
python3 -c "
from zmatrix.research_db.directory_registry import validate_directory_structure
from pathlib import Path
r=validate_directory_structure(Path('data/research_db'))
assert r['status']=='PASS', f'dirs missing: {r[\"missing\"]}'
print('  ✅ 10 directories')
"

echo "[4] Code modules..."
python3 -c "
mods=['trust_level','pit_policy','outcome_horizon_policy','data_source_capability','promotion_policy','no_production_boundary','directory_registry','research_db_status']
for m in mods: __import__(f'zmatrix.research_db.{m}')
print('  ✅ 8 modules')
"

echo "[5] Pytest..."
PYTHONPATH=. python3 -m pytest -q tests/research_db/ 2>&1 | tail -3

echo "[6] Safety scan..."
python3 - <<'PY'
from pathlib import Path
for p in Path("zmatrix/research_db").rglob("*.py"):
    c = p.read_text(encoding="utf-8", errors="ignore")
    for f in ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        if f in c and "allowlist:" not in c:
            raise SystemExit(f"❌ FORBIDDEN {f} in {p}")
print("  ✅ 0 forbidden flags")
PY

echo "[7] Acceptance matrix..."
test -f docs/research_db/PHASE0_ACCEPTANCE_MATRIX.md && echo "  ✅"

echo "[8] Closeout..."
test -f docs/research_db/PHASE0_CLOSEOUT_REPORT.md && echo "  ✅"

echo ""
echo "═══ ResearchDB Phase 0 PASS ═══"
