"""Real BRD Classifier Connector v3.4 — call classify_stock_role with proper bundle"""
from __future__ import annotations

_CANDIDATES = [
    ("zmatrix.investment.stock_role_classifier","classify_stock_role"),
    ("zmatrix.investment.investment_role_workflow","build_investment_role_review"),
]

class RealBRDClassifierConnector:
    connector_version = "REAL_BRD_CLASSIFIER_CONNECTOR_V10"
    def __init__(self):
        self.connector_status = "UNINITIALIZED"; self.impl = None; self.impl_name = None
        for mod_name, fn_name in _CANDIDATES:
            try:
                mod = __import__(mod_name, fromlist=["*"])
                fn = getattr(mod, fn_name, None)
                if callable(fn): self.impl = fn; self.impl_name = f"{mod_name}.{fn_name}"; self.connector_status = "CONNECTED"; return
            except Exception: continue
        self.connector_status = "NOT_FOUND"

    def classify(self, pit_features):
        if self.connector_status != "CONNECTED" or self.impl is None:
            return {"connector_status":self.connector_status,"role":"UNKNOWN","decision":"WATCH_ONLY",
                    "hard_gate_passed":False,"brd_score":0.0,"fallback":True,
                    "fallback_reason":"REAL_BRD_CONNECTOR_NOT_FOUND","brd_connected":False,
                    "real_trade_allowed":False,"broker_order_allowed":False}
        bundle = pit_features.get("brd_input_bundle") or pit_features.get("input_bundle")
        if not bundle or not bundle.get("input_ready"):
            return {"connector_status":self.connector_status,"connector_impl":self.impl_name,
                    "role":"UNKNOWN","decision":"WATCH_ONLY","hard_gate_passed":False,"brd_score":0.0,
                    "fallback":True,"fallback_reason":"BRD_INPUT_BUNDLE_NOT_READY","brd_connected":False,
                    "real_trade_allowed":False,"broker_order_allowed":False}
        ticker = bundle.get("ticker") or pit_features.get("ticker","")
        b_matrix = bundle.get("b_matrix",{})
        r_matrix = bundle.get("r_matrix",{})
        d_matrix = bundle.get("d_matrix",{})
        account = bundle.get("account",{})
        exposure = bundle.get("exposure",{})
        try:
            raw = self.impl(ticker, b_matrix, r_matrix, d_matrix, account=account, exposure=exposure)
            from zmatrix.brd_replay.classifier_interface import normalize_brd_classifier_output
            n = normalize_brd_classifier_output(raw)
            # Inject B-Matrix reason_codes into result for audit trail
            brc = b_matrix.get("reason_codes", [])
            if brc:
                n.setdefault("reason_codes", []).extend(brc)
            # Respect B-Matrix role_cap: downgrade if classifier gives A but B-Matrix caps lower
            b_matrix = bundle.get("b_matrix",{})
            role_cap = b_matrix.get("role_cap")
            if role_cap and role_cap != "A_LONG_CORE" and n.get("role") == "A_LONG_CORE":
                n["role"] = role_cap
                n.setdefault("reason_codes",[]).append(f"ROLE_DOWNGRADED_BY_B_MATRIX_CAP:{role_cap}")
            n.update({"connector_status":"CONNECTED","connector_impl":self.impl_name,
                      "fallback":False,"brd_connected":True})
            return n
        except Exception as e:
            return {"connector_status":"ERROR","connector_impl":self.impl_name,
                    "role":"UNKNOWN","decision":"WATCH_ONLY","hard_gate_passed":False,"brd_score":0.0,
                    "fallback":True,"fallback_reason":f"CONNECTOR_ERROR:{str(e)[:80]}","brd_connected":False,
                    "real_trade_allowed":False,"broker_order_allowed":False}

def build_real_brd_classifier_connector(): return RealBRDClassifierConnector()
