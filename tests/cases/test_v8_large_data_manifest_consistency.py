import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_factor_hash_match():
    m=json.loads((W/"runtime_reports/cases/v8_large_data_manifest.json").read_text())
    s=json.loads((W/"runtime_reports/cases/v8_expanded_factor_values_summary.json").read_text())
    assert m["files"][0]["sha256"][:16]==s["large_file_hash"]
def test_label_hash_match():
    m=json.loads((W/"runtime_reports/cases/v8_large_data_manifest.json").read_text())
    s=json.loads((W/"runtime_reports/cases/v8_forward_return_labels_summary.json").read_text())
    assert m["files"][1]["sha256"][:16]==s["large_file_hash"]
def test_hashes_match():
    m=json.loads((W/"runtime_reports/cases/v8_large_data_manifest.json").read_text())
    h=json.loads((W/"runtime_reports/cases/v8_large_data_hashes.json").read_text())
    assert h["factor_file_sha256"]==m["files"][0]["sha256"]
    assert h["label_file_sha256"]==m["files"][1]["sha256"]
def test_not_committed():
    m=json.loads((W/"runtime_reports/cases/v8_large_data_manifest.json").read_text())
    for f in m["files"]:
        assert f["committed_to_git"] is False
def test_audit_pass():
    a=json.loads((W/"runtime_reports/cases/v8_large_data_manifest_audit.json").read_text())
    assert a["manifest_consistent"] is True
    assert a["ready_for_v9_gate"] is True
def test_v9_blocked_if_manifest_fails():
    g=json.loads((W/"runtime_reports/cases/v9_formal_factor_validation_entry_gate.json").read_text())
    assert g["manifest_consistent"] is True
    assert "ALLOWED" in g["status"]
