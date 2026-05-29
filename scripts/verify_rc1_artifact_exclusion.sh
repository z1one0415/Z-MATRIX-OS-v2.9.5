#!/usr/bin/env bash
set -euo pipefail

echo "═══ RC1 Runtime Artifact Exclusion Audit ═══"
cd "$(cd "$(dirname "$0")/.." && pwd)"

mkdir -p runtime_reports/rc1_artifact_test

# Generate a test audit ZIP to verify it works
PYTHONPATH=. python3 - <<'PY'
from pathlib import Path
from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent

out_dir = Path("runtime_reports/rc1_artifact_test")
env = OutputEnvelope(pipeline_id="RC1_AUDIT", run_id="rc1_artifact_test")
evt = AuditEvent("e1", "PIPELINE_RUN")
result = AuditExportPack.export_to_zip(env, [evt], str(out_dir / "test_audit.zip"))
assert Path(result["path"]).exists()
print(f"ZIP created: {result['path']}")
print(f"Files in ZIP: {result['file_count']}")
PY

# Verify runtime_reports not tracked by git
echo ""
echo "Checking git tracking..."
if git status --short | grep -qE 'runtime_reports|\.zip'; then
  echo "❌ runtime artifact visible to git"
  exit 1
fi

echo "✅ runtime artifact exclusion PASS"
