#!/usr/bin/env python3
"""Generate v3.0-alpha tag artifacts."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

from zmatrix.alpha_tag.release_notes_builder import build_v3_alpha_rc1_release_notes

OUT = Path("release/alpha_rc")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    notes = build_v3_alpha_rc1_release_notes()
    (OUT / "v3_alpha_rc1_release_notes.md").write_text(notes, encoding="utf-8")

    (OUT / "v3_alpha_tag_command_preview_v10.md").write_text(
        """# v3.0-alpha-rc1 Tag Command Preview

DO NOT EXECUTE AUTOMATICALLY.

Manual review required.

Preview only:

git tag -a v3.0-alpha-rc1 -m "Z-MATRIX-OS v3.0-alpha RC1"
git push origin v3.0-alpha-rc1

Safety:

- git_tag_execute_allowed=False
- git_push_tags_allowed=False
- runtime_enabled=False
- real_trade_allowed=False
""",
        encoding="utf-8",
    )

    (OUT / "v3_alpha_final_release_summary_v10.md").write_text(
        """# v3.0-alpha RC1 Final Release Summary

Status: READY_FOR_TAG_REVIEW

This RC is not production-ready.
This RC is not live-trading-ready.
This RC is not runtime-enabled.

Validated chain:

v2.9.10 → v2.9.18

Final gate:

v2.9.19-dev Final Tag Gate & Release Notes
""",
        encoding="utf-8",
    )

    print("generated v3 alpha tag artifacts")

if __name__ == "__main__":
    main()
