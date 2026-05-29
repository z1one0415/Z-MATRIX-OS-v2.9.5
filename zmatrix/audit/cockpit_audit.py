"""V4.0-C7 Cockpit + Audit — output envelope and audit export"""
from __future__ import annotations
from dataclasses import dataclass, field
import json

@dataclass
class OutputEnvelope:
    pipeline_id: str = ""; run_id: str = ""; status: str = "DEGRADED"
    domain_states: dict = field(default_factory=dict); data_health: str = "UNKNOWN"
    risk_flags: list = field(default_factory=list); human_review_required: bool = True
    real_trade_allowed: bool = False; broker_order_allowed: bool = False
    audit_event_id: str = ""
    def to_dict(self): return {"pipeline_id":self.pipeline_id,"run_id":self.run_id,"status":self.status,"risk_flags":self.risk_flags,"human_review_required":self.human_review_required,"real_trade_allowed":self.real_trade_allowed,"broker_order_allowed":self.broker_order_allowed}

@dataclass
class AuditEvent:
    event_id: str; event_type: str; timestamp: str = ""; pipeline_id: str = ""
    input_hash: str = ""; output_hash: str = ""; safety_gate_passed: bool = True
    real_trade_allowed: bool = False; broker_order_allowed: bool = False
    def to_dict(self): return {"event_id":self.event_id,"event_type":self.event_type,"safety_gate_passed":self.safety_gate_passed,"real_trade_allowed":self.real_trade_allowed}

class AuditExportPack:
    @staticmethod
    def generate(envelope, events):
        manifest = {"manifest_version":"V40_AUDIT_V1","envelope":envelope.to_dict(),"events":[e.to_dict() for e in events],"real_trade_allowed":False}
        return {"manifest":manifest,"format":"ZIP_READY","size_estimate":len(json.dumps(manifest))}

class ForbiddenOutputScan:
    # allowlist: forbidden-token-definition
    FORBIDDEN = ["real_trade_allowed=True","broker_order_allowed=True","BUY","SELL","AUTO_EXECUTE"]
    @staticmethod
    def scan(text): hits = [f for f in ForbiddenOutputScan.FORBIDDEN if f in (text or "")]; return {"passed":len(hits)==0,"hits":hits}
