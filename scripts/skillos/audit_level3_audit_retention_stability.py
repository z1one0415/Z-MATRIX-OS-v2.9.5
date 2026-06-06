#!/usr/bin/env python3
"""Audit Level 3 audit retention stability. 50 repeated runs. Tmp only."""

import os, sys, json, time
from pathlib import Path
from tempfile import TemporaryDirectory

RETENTION_STABILITY_RUNS = 50

from zmatrix.agent.skillos_level3_retention_config import get_default_retention_config, FORBIDDEN_CLEANUP_PATHS
from zmatrix.agent.skillos_level3_retention_cleanup import run_retention_cleanup


def populate(audit, count=5):
    for i in range(count):
        f = audit / f"log_{i}.txt"
        f.write_text("x" * 100)
        past = time.time() - (15 + i) * 86400
        os.utime(f, (past, past))


def main():
    errors = []

    with TemporaryDirectory() as td:
        # 1. Dry-run repeated: check file existence, not deleted_count
        for i in range(RETENTION_STABILITY_RUNS):
            a = Path(td) / f"dry_{i}"; a.mkdir(); populate(a, 5)
            c = get_default_retention_config(a)
            r = run_retention_cleanup(c, apply=False)
            remaining = list(a.iterdir())
            if len(remaining) != 5:
                errors.append(f"dry-run run {i}: {len(remaining)} files remain")

        # 2. Apply repeated
        for i in range(RETENTION_STABILITY_RUNS):
            a = Path(td) / f"ap_{i}"; a.mkdir(); populate(a, 5)
            c = get_default_retention_config(a)
            run_retention_cleanup(c, apply=True)

        # 3. Fresh file retention check
        a = Path(td) / "fresh_check"; a.mkdir(); populate(a, 5)
        f = a / "fresh.txt"; f.write_text("x")
        c = get_default_retention_config(a)
        for i in range(RETENTION_STABILITY_RUNS):
            run_retention_cleanup(c, apply=True)
        if not f.exists():
            errors.append("fresh file deleted within retention_days")

        # 4. Summary deterministic
        a = Path(td) / "det"; a.mkdir(); populate(a, 5)
        c = get_default_retention_config(a)
        r1 = run_retention_cleanup(c, apply=False)
        r2 = run_retention_cleanup(c, apply=False)
        if r1.deleted_paths != r2.deleted_paths:
            errors.append("summary not deterministic")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print("Z_SKILLOS_LEVEL3_AUDIT_RETENTION_STABILITY_FAIL_CI")
        return 1

    print("Z_SKILLOS_LEVEL3_AUDIT_RETENTION_STABILITY_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
