#!/usr/bin/env python3
"""F6.2.2 No Hardcoded Ground Truth Audit — scan all audit scripts."""
import re, json
from pathlib import Path

HARDCODED_PATTERNS = [
    (r'FUNDAMENTAL_TICKERS\s*=\s*\[', "FUNDAMENTAL_TICKERS"),
    (r'F13_SCORES\s*=\s*\[', "F13_SCORES"),
    (r'F6_2_TICKERS\s*=\s*\[', "F6_2_TICKERS"),
]

# We allow PRICE_LABEL_TICKERS (known constant) and ETF_TICKERS (known classification constant)
ALLOWED_HARDCODED = {"PRICE_LABEL_TICKERS", "ETF_TICKERS"}

SCRIPT_DIR = Path("scripts/research/factors/reviews")

violations = []
allowed_found = []

for script in sorted(SCRIPT_DIR.glob("*.py")):
    content = script.read_text()
    for pattern, label in HARDCODED_PATTERNS:
        if re.search(pattern, content):
            if label in ALLOWED_HARDCODED:
                allowed_found.append({"script": script.name, "label": label, "status": "ALLOWED"})
            else:
                violations.append({"script": script.name, "pattern": label, "status": "VIOLATION"})

result = {
    "audit_type": "NO_HARDCODED_GROUND_TRUTH",
    "scripts_scanned": [s.name for s in sorted(SCRIPT_DIR.glob("*.py"))],
    "violations": violations,
    "allowed_patterns_found": allowed_found,
    "verdict": "PASS" if len(violations) == 0 else "FAIL"
}

OUTDIR = Path("research/factor_library/reviews/batch_004/f6_2_2_csv_recovery_and_file_reaudit")
OUTDIR.mkdir(parents=True, exist_ok=True)
OUTFILE = OUTDIR / "v13_f6_2_2_no_hardcoded_ground_truth_audit.json"
OUTFILE.write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(f"✅ No hardcoded ground truth: {len(violations)} violations, {len(allowed_found)} allowed")

if __name__ == "__main__":
    pass
