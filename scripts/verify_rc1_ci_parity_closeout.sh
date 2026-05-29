#!/usr/bin/env bash
set -euo pipefail

echo "═══ RC1 CI Parity Closeout Verification ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

python3 - <<'PY'
from pathlib import Path

closeout = Path("docs/rc1_audit/RC1_CI_PARITY_CLOSEOUT.md").read_text(encoding="utf-8")
audit = Path("docs/rc1_audit/RC1_READINESS_AUDIT_REPORT.md").read_text(encoding="utf-8")
score = Path("docs/rc1_audit/RC1_READINESS_SCORECARD.md").read_text(encoding="utf-8")

for f in ["docs/rc1_audit/RC1_CI_PARITY_CLOSEOUT.md", "docs/rc1_audit/RC1_READINESS_AUDIT_REPORT.md", "docs/rc1_audit/RC1_READINESS_SCORECARD.md", ".github/workflows/v40-rc1-audit.yml"]:
    assert Path(f).exists(), f"missing: {f}"

required = ["CI parity status:", "Workflow: v40-rc1-audit.yml", "Run ID:", "Run URL:", "Head SHA:", "Conclusion:", "Production: BLOCKED", "Broker/runtime: BLOCKED", "Real trade: BLOCKED"]
for item in required:
    if "RC1 tag" in item:
        assert "RC1 tag created" in closeout and "FALSE" in closeout, "Missing RC1 tag"
    else:
        assert item in closeout, f"Missing: {item}"

assert "GitHub Actions CI" in audit
assert "CI Cloud Run" in score

forbidden = ["RC1 tag created: TRUE", "Production: READY", "Broker/runtime: READY", "RC1 status: APPROVED"]
for fb in forbidden:
    for doc in [closeout, audit, score]:
        assert fb not in doc, f"Forbidden: {fb}"

print("✅ RC1 CI parity closeout docs PASS")
PY

echo "═══ RC1 CI Parity Closeout PASS ═══"
