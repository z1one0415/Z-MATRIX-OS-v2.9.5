"""Isolated non-runtime shadow audit writer for SkillOS Level 3.

Disabled mode: no writes. Enabled: writes JSONL to dedicated audit path.
Never touches runtime_reports, production, broker, or real_trade.
"""

import json
from pathlib import Path
from typing import Any

from zmatrix.agent.skillos_level3_config import SkillOSLevel3Config
from zmatrix.agent.skillos_level3_redaction import redact_telemetry


def write_shadow_audit_event(event: dict[str, Any], config: SkillOSLevel3Config) -> dict[str, Any]:
    """Write shadow audit event. No-op when disabled. Never blocks."""
    if not config.enabled or not config.write_enabled:
        return {"written": False, "reason": "LEVEL3_DISABLED"}

    try:
        clean = redact_telemetry(event)
    except ValueError as e:
        return {"written": False, "reason": "REDACTION_FAILED", "error": str(e)}

    try:
        config.audit_path.mkdir(parents=True, exist_ok=True)
        out = config.audit_path / "shadow_audit.jsonl"
        with open(out, "a") as f:
            f.write(json.dumps(clean, sort_keys=True) + "\n")
        return {"written": True}
    except OSError as e:
        return {"written": False, "reason": "WRITE_FAILED", "error": str(e)}
