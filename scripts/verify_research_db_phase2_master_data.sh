#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 2 Master Data Verification ═══"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

echo ""
echo "[0] Compile"
python3 -m compileall zmatrix/research_db/master_data/ tests/research_db/master_data/

echo ""
echo "[1] Phase 1.1 Cloud Acceptance Baseline"
bash scripts/verify_research_db_phase1_1_cloud_acceptance.sh

echo ""
echo "[2] Master Data Unit Tests"
PYTHONPATH=. python3 -m pytest -q tests/research_db/master_data/

echo ""
echo "[3] Phase 2 Required Modules"
python3 - <<'PY'
from pathlib import Path
required = [ "master_schema.py","security_master.py","ticker_identity_resolver.py","alias_resolver.py",
 "exchange_board_classifier.py","industry_taxonomy.py","sector_mapper.py","chain_taxonomy.py",
 "chain_node_mapper.py","mapping_snapshot.py","mapping_integrity_checker.py","coverage_report.py",
 "master_data_report.py","import_audit.py" ]
base = Path("zmatrix/research_db/master_data")
for name in required:
    assert (base / name).exists(), f"missing module: {name}"
print("  ✅ 14 required modules exist")
PY

echo ""
echo "[4] Phase 2 Safety Scan"
python3 - <<'PY'
from pathlib import Path; import subprocess
for p in Path("zmatrix/research_db/master_data").rglob("*.py"):
    text = p.read_text(encoding="utf-8", errors="ignore")
    for forbidden in [ "real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True",
     "auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True" ]:
        if forbidden in text and "allowlist:" not in text:
            raise SystemExit(f"FORBIDDEN {forbidden} in {p}")
r = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
tracked = []
for line in r.stdout.splitlines():
    lower = line.lower()
    if "data/research_db/master_data/raw/" in lower and not lower.endswith(".gitkeep"): tracked.append(line)
    if "data/research_db/master_data/staging/" in lower and not lower.endswith(".gitkeep"): tracked.append(line)
    if "data/research_db/master_data/vendor/" in lower and not lower.endswith(".gitkeep"): tracked.append(line)
    if lower.endswith((".xlsx",".xls",".vendor.csv",".raw.csv")): tracked.append(line)
assert not tracked, f"private/vendor master data tracked: {tracked}"
print("  ✅ safety scan PASS")
PY

echo ""
echo "[5] Phase 2 Documents"
test -f docs/research_db/PHASE2_SCOPE_LOCK.md && echo "  ✅ scope lock"
test -f docs/research_db/PHASE2_ACCEPTANCE_MATRIX.md && echo "  ✅ acceptance matrix"
test -f docs/research_db/PHASE2_CLOSEOUT_REPORT.md && echo "  ✅ closeout"

echo ""
echo "═══ ResearchDB Phase 2 Master Data PASS ═══"
