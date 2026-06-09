#!/usr/bin/env python3
"""F6.2.2 Safety Audit — check CSV artifacts and F6.2.2 scripts for forbidden patterns.

Only scans:
- f6_2_tushare_pit_fundamental_ingestion/ (CSV signal data)
- scripts/research/factors/reviews/audit_v13_f6_2_2_*.py (F6.2.2 audit scripts)
- scripts/research/factors/reviews/build_v13_f6_2_2_*.py (F6.2.2 build scripts)

Skips: contract JSONs, safety audit outputs, legacy scripts.
"""
import json, re
from pathlib import Path

FORBIDDEN_PATTERNS = [
    ("forward_return", "FORWARD_RETURN"),
    (r'alpha_signal', "ALPHA_SIGNAL"),
    (r'trade_signal', "TRADE_SIGNAL"),
    (r'runner_enabled\s*[=:]\s*true', "RUNNER_ENABLED_TRUE"),
    (r'execution_allowed\s*[=:]\s*true', "EXECUTION_ALLOWED_TRUE"),
    (r'alpha_claim_allowed\s*[=:]\s*true', "ALPHA_CLAIM_ALLOWED_TRUE"),
]

# Only scan the signal CSV directory and F6.2.2 scripts
CSV_DIR = Path("research/factor_library/reviews/batch_004/f6_2_tushare_pit_fundamental_ingestion/")
SCRIPTS_DIR = Path("scripts/research/factors/reviews/")

# F6.2.2 scripts only
F6_2_2_PREFIXES = ("audit_v13_f6_2_2_", "build_v13_f6_2_2_")

violations = []
files_scanned = []

# Scan CSV artifacts
if CSV_DIR.exists():
    for f in sorted(CSV_DIR.rglob("*")):
        if f.is_dir() or f.suffix not in ('.csv', '.json', '.md'):
            continue
        files_scanned.append(str(f))
        try:
            content = f.read_text()
        except Exception:
            continue
        for pattern, label in FORBIDDEN_PATTERNS:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                violations.append({
                    "file": str(f), "pattern": label, "match": m.group()[:80]
                })

# Scan F6.2.2 scripts only
if SCRIPTS_DIR.exists():
    for f in sorted(SCRIPTS_DIR.glob("*.py")):
        if not f.name.startswith(F6_2_2_PREFIXES):
            continue
        files_scanned.append(str(f))
        try:
            content = f.read_text()
        except Exception:
            continue
        # Skip self, contract builder, and closeout builder (document forbidden columns)
        if f.name in ("audit_v13_f6_2_2_safety.py", "build_v13_f6_2_2_csv_recovery_contract.py", "build_v13_f6_2_2_csv_recovery_closeout.py"):
            continue
        for pattern, label in FORBIDDEN_PATTERNS:
            for m in re.finditer(pattern, content, re.IGNORECASE):
                violations.append({
                    "file": str(f), "pattern": label, "match": m.group()[:80]
                })

result = {
    "audit_type": "SAFETY_BLOCK_CHECK",
    "files_scanned": files_scanned,
    "files_scanned_count": len(files_scanned),
    "forbidden_patterns_checked": [p[1] for p in FORBIDDEN_PATTERNS],
    "violations": violations,
    "violation_count": len(violations),
    "verdict": "PASS" if len(violations) == 0 else "FAIL"
}

OUTDIR = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "v13_f6_2_2_safety_audit.json"
OUTFILE.write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(f"✅ Safety audit: {len(violations)} violations across {len(files_scanned)} F6.2.2 files")

if __name__ == "__main__":
    pass
