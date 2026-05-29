# allowlist: forbidden-token-definition
"""V4.0-C8 IRF pipelines — integration smoke stubs"""
from __future__ import annotations
from zmatrix.audit.cockpit_audit import OutputEnvelope, AuditEvent

class BaseIRF:
    def __init__(self, irf_id, irf_name):
        self.irf_id = irf_id; self.irf_name = irf_name
    def execute(self):
        envelope = OutputEnvelope(pipeline_id=self.irf_id, run_id=f"{self.irf_id}-001", status="INTEGRATION_SMOKE", human_review_required=True)
        event = AuditEvent(event_id=f"{self.irf_id}-evt-001", event_type="PIPELINE_RUN", pipeline_id=self.irf_id)
        return {"envelope":envelope.to_dict(),"audit_event":event.to_dict(),"real_trade_allowed":False,"broker_order_allowed":False,"production_allowed":False}

IRF_REGISTRY = {}
for irf_id, irf_name in [
    ("IRF-01","Single Stock Institutional Research"),("IRF-02","Monthly Full Market Selection"),
    ("IRF-03","Strategy Validation"),("IRF-04","Paper Execution"),("IRF-05","Account Review"),
    ("IRF-06","Portfolio Alpha Review"),("IRF-07","Multi-Strategy Portfolio"),("IRF-08","Factor & Proprietary Data Factory")
]: IRF_REGISTRY[irf_id] = BaseIRF(irf_id, irf_name)
