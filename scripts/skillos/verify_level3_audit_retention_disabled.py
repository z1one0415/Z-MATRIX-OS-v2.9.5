#!/usr/bin/env python3
"""Verify SkillOS Level 3 audit retention can be disabled without side effects."""

import sys
import time
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from zmatrix.agent.skillos_level3_retention_config import get_default_retention_config
from zmatrix.agent.skillos_level3_retention_cleanup import run_retention_cleanup


def main() -> int:
    with TemporaryDirectory() as td:
        audit_path = Path(td)
        old_file = audit_path / "old.log"
        old_file.write_text("x")
        past = time.time() - 30 * 86400
        old_file.touch()
        old_file.chmod(0o600)

        os.utime(old_file, (past, past))

        config = get_default_retention_config(audit_path, enabled=False)
        result = run_retention_cleanup(config, apply=True)
        if not old_file.exists():
            print("FAIL: disabled retention deleted an audit file")
            return 1
        if result.deleted_count != 0:
            print("FAIL: disabled retention reported deleted files")
            return 1

    print("Z_SKILLOS_LEVEL3_AUDIT_RETENTION_DISABLED_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
