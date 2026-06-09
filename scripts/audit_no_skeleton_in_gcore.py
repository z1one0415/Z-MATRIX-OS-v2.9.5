#!/usr/bin/env python3
"""V13.GCORE.3 — Skeleton Guard: no pass/TODO/placeholder in G-Core production paths.

Checks:
- zmatrix/prediction/human_risk_engine.py
- zmatrix/prediction/human_risk_schema.py
- zmatrix/daily_memory/memory_card_modules.py
- zmatrix/research/industry_chain_analyzer.py
- pipelines/Z-G05_日记忆卡/gate_pipeline.py
- pipelines/Z-G15_产业链深研/gate_pipeline.py
- pipelines/Z-G17_人类风控/gate_pipeline.py

FORBIDDEN patterns in production code (outside comments/docstrings):
- bare `pass` on its own line (function body = just pass)
- TODO
- NotImplemented
- placeholder
- stub (except import fallback lambdas)
- 待实现
- 占位

ALLOWED in:
- docs/
- tests/fixtures/
- comments explaining WHY something is deferred (not bare pass)
"""
import re, sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent

PRODUCTION_PATHS = [
    "zmatrix/prediction/human_risk_engine.py",
    "zmatrix/prediction/human_risk_schema.py",
    "zmatrix/daily_memory/memory_card_modules.py",
    "zmatrix/research/industry_chain_analyzer.py",
    "pipelines/Z-G05_日记忆卡/gate_pipeline.py",
    "pipelines/Z-G15_产业链深研/gate_pipeline.py",
    "pipelines/Z-G17_人类风控/gate_pipeline.py",
]

FORBIDDEN = [
    (r"^\s*pass\s*$", "bare pass"),
    (r"\bTODO\b", "TODO"),
    (r"\bNotImplemented\b", "NotImplemented"),
    (r"\bplaceholder\b", "placeholder"),
    (r"\b待实现\b", "待实现"),
    (r"\b占位\b", "占位"),
]

# stub is allowed only in import fallback lambdas
STUB_PATTERN = re.compile(r"\bstub\b", re.IGNORECASE)
STUB_ALLOWED = re.compile(r"lambda|ImportError|except|fallback|\"stub\".*status", re.IGNORECASE)


def check_file(path: Path) -> list[str]:
    violations = []
    if not path.exists():
        violations.append(f"FILE_MISSING: {path}")
        return violations
    lines = path.read_text().splitlines()
    in_docstring = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Track docstrings
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                in_docstring = not in_docstring
            continue
        if in_docstring:
            continue
        # Skip comments
        if stripped.startswith("#"):
            continue
        # Check forbidden
        for pattern, name in FORBIDDEN:
            if re.search(pattern, line):
                violations.append(f"{path}:{i} [{name}] {stripped[:80]}")
        # Check stub (special handling)
        if STUB_PATTERN.search(line) and not STUB_ALLOWED.search(line):
            violations.append(f"{path}:{i} [stub_in_production] {stripped[:80]}")
    return violations


def main():
    print("☯️ V13.GCORE.3 — Skeleton Guard Audit")
    print("=" * 60)
    all_violations = []
    for rel_path in PRODUCTION_PATHS:
        full = WORKSPACE / rel_path
        violations = check_file(full)
        status = "✅" if not violations else f"❌ {len(violations)} violations"
        print(f"  {status} {rel_path}")
        all_violations.extend(violations)

    print(f"\n{'=' * 60}")
    if all_violations:
        print(f"❌ FAIL: {len(all_violations)} skeleton violations found:")
        for v in all_violations:
            print(f"  → {v}")
        sys.exit(1)
    else:
        print("✅ PASS: No skeleton code in G-Core production paths.")
        sys.exit(0)


if __name__ == "__main__":
    main()
