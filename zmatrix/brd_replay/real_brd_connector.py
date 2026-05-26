"""Real BRD Classifier Connector — connect existing B/R/D modules or report NOT_FOUND"""
from __future__ import annotations
from typing import Any

_CANDIDATES = [
    ("zmatrix.investment.stock_role_classifier","classify_stock_role"),
    ("zmatrix.investment.investment_role_workflow","build_investment_role_review"),
    ("zmatrix.investment.b_matrix","evaluate_b_matrix"),
]

class RealBRDClassifierConnector:
    connector_version = "REAL_BRD_CLASSIFIER_CONNECTOR_V10"
    def __init__(self):
        self.connector_status = "UNINITIALIZED"
        self.impl = None; self.impl_name = None
        for mod_name, fn_name in _CANDIDATES:
            try:
                mod = __import__(mod_name, fromlist=["*"])
                fn = getattr(mod, fn_name, None)
                if callable(fn):
                    self.impl = fn; self.impl_name = f"{mod_name}.{fn_name}"
                    self.connector_status = "CONNECTED"; return
            except Exception: continue
        self.connector_status = "NOT_FOUND"

    def classify(self, pit_features):
        if self.connector_status != "CONNECTED" or self.impl is None:
            return {"connector_status":self.connector_status,"role":"UNKNOWN","decision":"WATCH_ONLY",
                    "hard_gate_passed":False,"brd_score":0.0,"fallback":True,
                    "fallback_reason":"REAL_BRD_CONNECTOR_NOT_FOUND","brd_connected":False,
                    "real_trade_allowed":False,"broker_order_allowed":False}
        try:
            raw = self.impl(pit_features) if callable(self.impl) else {}
            from zmatrix.brd_replay.classifier_interface import normalize_brd_classifier_output
            n = normalize_brd_classifier_output(raw)
            n.update({"connector_status":"CONNECTED","connector_impl":self.impl_name,
                      "fallback":False,"brd_connected":True})
            return n
        except Exception as e:
            return {"connector_status":"ERROR","role":"UNKNOWN","decision":"WATCH_ONLY",
                    "hard_gate_passed":False,"brd_score":0.0,"fallback":True,
                    "fallback_reason":f"CONNECTOR_ERROR:{str(e)[:80]}","brd_connected":False,
                    "real_trade_allowed":False,"broker_order_allowed":False}

def build_real_brd_classifier_connector(): return RealBRDClassifierConnector()
