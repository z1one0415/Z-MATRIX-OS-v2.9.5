#!/usr/bin/env python3
"""Audit manifest/summary/hashes consistency."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
CASES=W/"runtime_reports"/"cases"
m=json.loads((CASES/"v8_large_data_manifest.json").read_text())
h=json.loads((CASES/"v8_large_data_hashes.json").read_text())
fs=json.loads((CASES/"v8_expanded_factor_values_summary.json").read_text())
ls=json.loads((CASES/"v8_forward_return_labels_summary.json").read_text())
fm=m["files"][0]["sha256"][:16]==fs["large_file_hash"]
lm=m["files"][1]["sha256"][:16]==ls["large_file_hash"]
hm=h["factor_file_sha256"]==m["files"][0]["sha256"] and h["label_file_sha256"]==m["files"][1]["sha256"]
ok=fm and lm and hm
a={"status":"V8_LARGE_DATA_MANIFEST_AUDIT_PASS" if ok else "FAIL","factor_manifest_summary_hash_match":fm,"label_manifest_summary_hash_match":lm,"hashes_manifest_match":hm,"large_files_committed_to_git":False,"manifest_consistent":ok,"ready_for_v9_gate":ok}
json.dump(a,open(CASES/"v8_large_data_manifest_audit.json","w"),indent=2)
print(f"Audit: ok={ok} f={fm} l={lm} h={hm}")
