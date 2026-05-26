"""Release Notes Builder — generate v3.0-alpha-rc1 release notes"""
from __future__ import annotations

from zmatrix.alpha_tag.schemas import TARGET_TAG


def build_v3_alpha_rc1_release_notes() -> str:
    """Markdown release notes for v3.0-alpha-rc1."""
    return f"""# Z-MATRIX-OS v3.0-alpha-rc1 Release Notes

## Status

READY_FOR_TAG_REVIEW

## Scope

This is an alpha release candidate for architecture rehearsal only.

## Included Version Chain

- v2.9.10-dev Workspace Alignment & Pipeline Census
- v2.9.11-dev EventStore & Unified Event Ledger
- v2.9.12-dev Hermes Memory Kernel Preview
- v2.9.13-dev Approval-Required Reflection Loop
- v2.9.14-dev Prompt Hot-Patching Middleware Preview
- v2.9.15-dev Tail-Risk Autonomic Gates Preview
- v2.9.16-dev v3.0-alpha Integration Readiness Gate
- v2.9.17-dev v3.0-alpha Dry-Run Rehearsal
- v2.9.18-dev Alpha RC Packaging & Freeze

## What This Release Can Do

- Run verification gates
- Run dry-run rehearsal
- Generate readiness report
- Generate RC packaging artifacts
- Validate tag readiness

## What This Release Cannot Do

- No real trading
- No broker connection
- No auto buy/sell/close
- No Hermes long-term memory write
- No real Z9 write
- No auto calibration
- No prompt auto-injection
- No system_prompt write
- No runtime enablement

## Tag Command Preview

```
git tag -a {TARGET_TAG} -m "Z-MATRIX-OS v3.0-alpha RC1"
git push origin {TARGET_TAG}
```

## Important

These commands are preview only and must not be executed by automation.
"""
