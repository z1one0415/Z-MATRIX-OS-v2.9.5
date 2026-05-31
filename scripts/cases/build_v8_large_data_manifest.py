#!/usr/bin/env python3
"""Build/refresh V8 large data manifest from actual files."""
import json, hashlib, os
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
CASES=W/"runtime_reports"/"cases"; LARGE=CASES/"v8_large_data"

ff=LARGE/"v8_expanded_factor_values.json"; lf=LARGE/"v8_forward_return_labels.json"
fd=ff.read_text() if ff.exists() else "{}"; ld=lf.read_text() if lf.exists() else "{}"
fh=hashlib.sha256(fd.encode()).hexdigest(); lh=hashlib.sha256(ld.encode()).hexdigest()
fj=json.loads(fd) if ff.exists() else {}; lj=json.loads(ld) if lf.exists() else {}
nr=len(fj.get("records",[])); nv=sum(len(r.get("factor_values",{})) for r in fj.get("records",[]))
lc=len(lj.get("labels",[]))

m={"status":"V8_LARGE_DATA_MANIFEST_BUILT","large_data_dir":"v8_large_data/",
   "files":[{"logical_name":"v8_expanded_factor_values","path":"v8_large_data/v8_expanded_factor_values.json",
   "size_mb":round(os.path.getsize(ff)/1024/1024,1) if ff.exists() else 0,"sha256":fh,
   "row_count":nr,"factor_value_count":nv,"committed_to_git":False},
   {"logical_name":"v8_forward_return_labels","path":"v8_large_data/v8_forward_return_labels.json",
   "size_mb":round(os.path.getsize(lf)/1024/1024,1) if lf.exists() else 0,"sha256":lh,
   "label_count":lc,"committed_to_git":False}],
   "ready_for_audit":True,"ready_for_alpha_claim":False}
json.dump(m,open(CASES/"v8_large_data_manifest.json","w"),indent=2)
json.dump({"factor_file_sha256":fh,"label_file_sha256":lh},open(CASES/"v8_large_data_hashes.json","w"),indent=2)
# Also sync summaries
json.dump({"status":"SUMMARY_ONLY","factor_records":nr,"factor_values":nv,"large_file_hash":fh[:16],"large_file_size_mb":round(os.path.getsize(ff)/1024/1024,1) if ff.exists() else 0,"committed_to_git":False},open(CASES/"v8_expanded_factor_values_summary.json","w"),indent=2)
json.dump({"status":"SUMMARY_ONLY","label_records":lc,"large_file_hash":lh[:16],"large_file_size_mb":round(os.path.getsize(lf)/1024/1024,1) if lf.exists() else 0,"committed_to_git":False},open(CASES/"v8_forward_return_labels_summary.json","w"),indent=2)
print(f"Manifest: factor_hash={fh[:16]} label_hash={lh[:16]}")
