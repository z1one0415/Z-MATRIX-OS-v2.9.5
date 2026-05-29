#!/usr/bin/env python3
"""RA-4: Safety Gate Deep Scan — forbidden expression detection across entire repo.

Scans .py, .sh, .md files under zmatrix/ scripts/ docs/ for unsafe tokens
that would enable production order execution or bypass safety gates.

Skips:
  - Files containing "allowlist: forbidden-token-definition"
  - Files under docs/rc1_audit/
  - .gitignore
"""

import json
import os
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent

FORBIDDEN = [
    # Boolean flags
    "real_trade_allowed=True",
    "broker_order_allowed=True",
    "runtime_enabled=True",
    "auto_buy_allowed=True",
    "auto_sell_allowed=True",
    "production_allowed=True",

    # Spaced variants
    "real_trade_allowed = True",
    "broker_order_allowed = True",
    "runtime_enabled = True",

    # Expression bypasses (assigning from variable instead of literal)
    "real_trade_allowed=mode",
    "broker_order_allowed=mode",
    "runtime_enabled=mode",

    # Dangerous API calls
    "auto_buy",
    "auto_sell",
    "broker_order",
    "send_order",
    "place_order",
    "execute_trade",
]

SCAN_ROOTS = ["zmatrix", "scripts", "docs"]
ALLOWLIST_TOKEN = "allowlist: forbidden-token-definition"
SKIP_DIR = "docs/rc1_audit"
SKIP_FILES = {".gitignore"}

EXTENSIONS = {".py", ".sh", ".md"}


def _is_skippable(file_path: Path) -> bool:
    """Return True if file should be skipped."""
    # Skip exact filenames
    if file_path.name in SKIP_FILES:
        return True
    # Skip docs/rc1_audit/
    rel = str(file_path.relative_to(WORKSPACE))
    if rel.startswith(SKIP_DIR + os.sep) or rel == SKIP_DIR:
        return True
    return False


def _has_allowlist_token(file_path: Path) -> bool:
    """Check whether file contains the allowlist bypass token."""
    try:
        content = file_path.read_text(errors="ignore")
        return ALLOWLIST_TOKEN in content
    except Exception:
        return False


def _collect_files() -> list[Path]:
    """Collect all scannable files."""
    files: list[Path] = []
    for root in SCAN_ROOTS:
        root_path = WORKSPACE / root
        if not root_path.is_dir():
            continue
        for dirpath, _, filenames in os.walk(root_path):
            for fname in filenames:
                fpath = Path(dirpath) / fname
                if fpath.suffix in EXTENSIONS:
                    files.append(fpath)
    return sorted(files)


def scan() -> dict:
    """Run the deep scan and return a result dict."""
    violations: list[dict] = []
    allowlisted: list[str] = []
    files_scanned = 0

    all_files = _collect_files()

    for fpath in all_files:
        rel = str(fpath.relative_to(WORKSPACE))

        # Step 1: skip-list check
        if _is_skippable(fpath):
            # Not counted as allowlisted or scanned; simply excluded
            continue

        # Step 2: allowlist token check
        if _has_allowlist_token(fpath):
            allowlisted.append(rel)
            continue

        # Step 3: scan content
        try:
            content = fpath.read_text(errors="ignore")
        except Exception:
            continue

        files_scanned += 1

        for token in FORBIDDEN:
            if token in content:
                # Find line numbers
                lines_with_token = []
                for lineno, line in enumerate(content.split("\n"), start=1):
                    if token in line:
                        lines_with_token.append(lineno)

                violations.append({
                    "file": rel,
                    "token": token,
                    "lines": lines_with_token,
                })

    scan_status = "PASS" if len(violations) == 0 else "FAIL"

    return {
        "scan_status": scan_status,
        "violations": violations,
        "files_scanned": files_scanned,
        "allowlisted_files": allowlisted,
    }


def main() -> int:
    result = scan()
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["scan_status"] == "PASS":
        print(f"\n✅ RA-4 Safety Gate Deep Scan PASS — {result['files_scanned']} files, 0 violations")
        return 0
    else:
        print(f"\n❌ RA-4 Safety Gate Deep Scan FAIL — {len(result['violations'])} violation(s) in {result['files_scanned']} files")
        for v in result["violations"]:
            lines_str = ",".join(str(ln) for ln in v["lines"][:5])
            if len(v["lines"]) > 5:
                lines_str += ",..."
            print(f"   {v['file']}:{lines_str}  → {v['token']}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
