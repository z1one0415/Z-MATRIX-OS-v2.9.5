"""V4.0-C7 Cockpit + Audit — output envelope and audit export (Hardening-C3 enhanced)"""
from __future__ import annotations
from dataclasses import dataclass, field
import json
import zipfile
from pathlib import Path
from datetime import datetime, timezone


@dataclass
class OutputEnvelope:
    pipeline_id: str = ""
    run_id: str = ""
    status: str = "DEGRADED"
    domain_states: dict = field(default_factory=dict)
    data_health: str = "UNKNOWN"
    risk_flags: list = field(default_factory=list)
    human_review_required: bool = True
    real_trade_allowed: bool = False
    broker_order_allowed: bool = False
    audit_event_id: str = ""

    def to_dict(self):
        return {
            "pipeline_id": self.pipeline_id,
            "run_id": self.run_id,
            "status": self.status,
            "domain_states": self.domain_states,
            "data_health": self.data_health,
            "risk_flags": self.risk_flags,
            "human_review_required": self.human_review_required,
            "real_trade_allowed": self.real_trade_allowed,
            "broker_order_allowed": self.broker_order_allowed,
            "audit_event_id": self.audit_event_id,
        }


@dataclass
class AuditEvent:
    event_id: str
    event_type: str
    timestamp: str = ""
    pipeline_id: str = ""
    input_hash: str = ""
    output_hash: str = ""
    safety_gate_passed: bool = True
    real_trade_allowed: bool = False
    broker_order_allowed: bool = False

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "pipeline_id": self.pipeline_id,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "safety_gate_passed": self.safety_gate_passed,
            "real_trade_allowed": self.real_trade_allowed,
            "broker_order_allowed": self.broker_order_allowed,
        }


SAFETY_DECLARATION_TXT = """\
============================================================
Z-MATRIX-OS V4.0 HARDENING-C3 — SAFETY DECLARATION
============================================================
This AUDIT ZIP contains PAPER-ONLY research artifacts.
No real trading recommendation is contained herein.

real_trade_allowed:       False
broker_order_allowed:     False
production_allowed:       False
human_review_required:    True

ALL POSITIONS ARE SIMULATED. NO BROKER ORDERS SHALL BE PLACED
BASED ON THE CONTENTS OF THIS ARCHIVE.
============================================================
Generated: {timestamp}
============================================================
"""


class AuditExportPack:
    @staticmethod
    def generate(envelope, events):
        """Legacy: return a dict with manifest (no file I/O)."""
        manifest = {
            "manifest_version": "V40_AUDIT_V1",
            "envelope": envelope.to_dict(),
            "events": [e.to_dict() for e in events],
            "real_trade_allowed": False,
        }
        return {
            "manifest": manifest,
            "format": "ZIP_READY",
            "size_estimate": len(json.dumps(manifest)),
        }

    @staticmethod
    def export_to_zip(envelope, events, output_path):
        """Hardening-C3: create a real .zip audit archive.

        Parameters
        ----------
        envelope : OutputEnvelope
        events : list[AuditEvent]
        output_path : str | Path
            Destination .zip file path.

        Returns
        -------
        dict
            {"path": str, "size_bytes": int, "file_count": int, "real_trade_allowed": False}
        """
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        now_iso = datetime.now(timezone.utc).isoformat()

        with zipfile.ZipFile(str(out), "w", compression=zipfile.ZIP_DEFLATED) as zf:
            # manifest.json
            manifest = {
                "manifest_version": "V40_AUDIT_V1",
                "generated_at": now_iso,
                "pipeline_id": envelope.pipeline_id,
                "run_id": envelope.run_id,
                "event_count": len(events),
                "real_trade_allowed": False,
                "broker_order_allowed": False,
            }
            zf.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))

            # envelope.json
            zf.writestr(
                "envelope.json",
                json.dumps(envelope.to_dict(), indent=2, ensure_ascii=False),
            )

            # events/*.json
            for i, event in enumerate(events):
                event_dict = event.to_dict()
                # Ensure real_trade_allowed is False in every event
                event_dict["real_trade_allowed"] = False
                event_dict["broker_order_allowed"] = False
                event_name = f"events/event_{i:04d}.json"
                zf.writestr(
                    event_name,
                    json.dumps(event_dict, indent=2, ensure_ascii=False),
                )

            # safety_declaration.txt
            zf.writestr(
                "safety_declaration.txt",
                SAFETY_DECLARATION_TXT.format(timestamp=now_iso),
            )

        file_count = 2 + len(events) + 1  # manifest + envelope + events + safety
        size_bytes = out.stat().st_size

        return {
            "path": str(out.resolve()),
            "size_bytes": size_bytes,
            "file_count": file_count,
            "real_trade_allowed": False,
        }


class ForbiddenOutputScan:
    """Allowlist: forbidden token definitions."""

    FORBIDDEN = [
        "real_trade_allowed=True",
        "broker_order_allowed=True",
        "BUY",
        "SELL",
        "AUTO_EXECUTE",
    ]

    @staticmethod
    def scan(text):
        hits = [f for f in ForbiddenOutputScan.FORBIDDEN if f in (text or "")]
        return {"passed": len(hits) == 0, "hits": hits}
