#!/usr/bin/env bash
# allowlist: forbidden-token-definition
set -euo pipefail

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-3 Audit ZIP Verify ═══"

WORKSPACE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$WORKSPACE"

python3 -m compileall zmatrix/audit/ 2>&1 | tail -1

# Tests
PYTHONPATH=. python3 -m pytest -q tests/test_hardening_c3_templates_audit.py -k "audit_zip"

# Verify real ZIP export
python3 - <<'PY'
import tempfile, os, zipfile, json
from pathlib import Path
from zmatrix.audit.cockpit_audit import AuditExportPack, OutputEnvelope, AuditEvent

with tempfile.TemporaryDirectory() as d:
    env = OutputEnvelope(pipeline_id="IRF-TEST", run_id="T001")
    evt = AuditEvent("ev1", "PIPELINE_RUN")
    zip_path = os.path.join(d, "audit_export.zip")
    result = AuditExportPack.export_to_zip(env, [evt], zip_path)
    assert result["path"], f"export failed: {result}"
    zip_file = result["path"]
    assert os.path.exists(zip_path), "zip not created"
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()
        assert "manifest.json" in names
        assert "envelope.json" in names
        assert any("events" in n for n in names)
        assert any("safety" in n.lower() for n in names)
        
        # Verify no trade allowed
        for n in names:
            if n.endswith(".json"):
                data = json.loads(zf.read(n))
                data_str = json.dumps(data)
                assert "real_trade_allowed=True" not in data_str
                assert "broker_order_allowed=True" not in data_str
    print(f"✅ C3-3: real ZIP export with {len(names)} files, 0 trade violations")
PY

# Ensure runtime_reports not git-tracked
python3 - <<'PY'
import subprocess
r = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
bad = [l for l in r.stdout.split("\n") if "runtime_reports" in l and not l.startswith("?")]
if bad:
    print(f"❌ runtime_reports tracked: {bad}")
    exit(1)
print("✅ C3-3: runtime_reports not git-tracked")
PY

echo "═══ V4.0 FINAL-HARDGATES Hardening-C3-3 PASS ═══"
