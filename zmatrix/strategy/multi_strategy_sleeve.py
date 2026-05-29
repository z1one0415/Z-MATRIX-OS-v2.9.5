# allowlist: forbidden-token-definition
"""V4.0 MultiStrategySleeve — standalone module"""
from __future__ import annotations
class MultiStrategySleeve:
    def __init__(self):
        self.sleeves = {"ROLE_CORE":{"weight_cap":0.30,"beta_budget":0.80},"ROLE_ROT":{"weight_cap":0.25,"beta_budget":1.0},"ROLE_HUNT":{"weight_cap":0.15,"beta_budget":1.2,"paper_only":True},"DEFENSIVE":{"weight_cap":0.30,"beta_budget":0.50},"CASH":{"weight_cap":1.0,"beta_budget":0.0}}
    def allocate(self, candidates):
        alloc={}; remaining=1.0
        for sleeve, cfg in self.sleeves.items(): w=min(cfg['weight_cap'],remaining); alloc[sleeve]=w; remaining-=w
        return {"allocations":alloc,"total_beta_check":sum(alloc.get(s,0)*self.sleeves[s]['beta_budget'] for s in alloc),"production_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False,"paper_only":True,"human_review_required":True}
