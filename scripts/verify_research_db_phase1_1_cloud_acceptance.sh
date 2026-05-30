#!/usr/bin/env bash
set -euo pipefail

echo "═══ ResearchDB Phase 1.1 Cloud Acceptance Verification ═══"
WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix tests scripts

bash scripts/verify_research_db_phase0.sh
bash scripts/verify_research_db_private_data_guardrail.sh
bash scripts/verify_research_db_phase1_account_truth.sh

PYTHONPATH=. python3 -m pytest -q tests/research_db/account_truth/

python3 - <<'PY'
from pathlib import Path

required = [
    "docs/research_db/PHASE1_CLOUD_ACCEPTANCE.md",
    ".github/workflows/researchdb-phase1.yml",
    "scripts/verify_research_db_private_data_guardrail.sh",
]
for p in required:
    assert Path(p).exists(), f"missing {p}"

doc = Path("docs/research_db/PHASE1_CLOUD_ACCEPTANCE.md").read_text(encoding="utf-8")
assert "Real broker data imported" in doc and "FALSE" in doc
assert "Private data tracked" in doc and "FALSE" in doc
assert "Production" in doc and "BLOCKED" in doc
assert "Broker/runtime" in doc and "BLOCKED" in doc
assert "Real trade" in doc and "BLOCKED" in doc

print("✅ ResearchDB Phase 1.1 cloud acceptance PASS")
PY

echo "═══ ResearchDB Phase 1.1 PASS ═══"
