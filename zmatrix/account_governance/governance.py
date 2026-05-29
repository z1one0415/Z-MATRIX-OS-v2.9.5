# allowlist: forbidden-token-definition
"""V4.0-C6 AccountGovernance — paper-only research layer"""
from __future__ import annotations

class CapitalCurve:
    def __init__(self): self.daily = []
    def add(self, date, pnl, capital): self.daily.append({"date":date,"pnl":pnl,"capital":capital})
    def compute(self):
        if not self.daily: return {"max_drawdown":0,"sharpe_proxy":0,"start_capital":0,"end_capital":0}
        caps=[d['capital'] for d in self.daily]; pnls=[d['pnl'] for d in self.daily]
        peak=caps[0]; mdd=0
        for c in caps: peak=max(peak,c); mdd=min(mdd,(c-peak)/peak*100) if peak else 0
        import statistics; avg_pnl = statistics.mean(pnls) if pnls else 0; std_pnl = statistics.stdev(pnls) if len(pnls)>1 else 1
        return {"max_drawdown":mdd,"sharpe_proxy":avg_pnl/std_pnl*16 if std_pnl else 0,"start_capital":caps[0],"end_capital":caps[-1],"production_allowed":False,"real_trade_allowed":False}

class ActionPermissionGate:
    ALLOWED = ["RESEARCH_ONLY","PAPER_ONLY","HUMAN_REVIEW_REQUIRED","ACTION_BLOCKED","DATA_INSUFFICIENT"]
    FORBIDDEN = ["REAL_TRADE_ALLOWED","BROKER_ORDER_ALLOWED","AUTO_BUY","AUTO_SELL"]
    @staticmethod
    def check(context): return {"action":"PAPER_ONLY","real_trade_allowed":False,"broker_order_allowed":False,"human_review_required":True}
