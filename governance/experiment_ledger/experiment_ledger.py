"""V4.0-3 Research Experiment OS — experiment ledger + workflow registry"""
from __future__ import annotations

EXPERIMENT_TYPES = ["REPLAY","FACTOR_TEST","REPAIR_TEST","PAPER_REPLAY","B_MATRIX_RESEARCH","D_MATRIX_RESEARCH","DATA_AUDIT","REPORT_GENERATION"]
EXPERIMENT_STATUSES = ["DRAFT","RUNNING","COMPLETED","FAILED","BLOCKED","ARCHIVED"]
EXPERIMENT_PERMISSIONS = {"RESEARCH_READY":["REPLAY","PAPER_REPLAY","DATA_AUDIT","REPORT_GENERATION","B_MATRIX_RESEARCH"],"SHADOW_ONLY":["DATA_AUDIT","REPORT_GENERATION","B_MATRIX_RESEARCH"],"BLOCKED":[]}

class ExperimentLedgerItem:
    def __init__(self, experiment_id, experiment_name, experiment_type, git_commit, phase=None, factor_ids=None, data_sources=None):
        self.experiment_id = experiment_id; self.experiment_name = experiment_name; self.experiment_type = experiment_type; self.created_at = None; self.created_by = "openclaw"; self.git_commit = git_commit; self.phase = phase; self.factor_ids = factor_ids or []; self.data_sources = data_sources or []; self.promotion_allowed = False; self.production_allowed = False; self.real_trade_allowed = False; self.broker_order_allowed = False; self.runtime_enabled = False; self.approval_required = True

INITIAL_EXPERIMENTS = [{"experiment_id":"EXP-V3520-001","experiment_name":"v3.5.20 RC closeout audit","experiment_type":"REPORT_GENERATION","git_commit":"f7a67c6","phase":"v3.5.20"},{"experiment_id":"EXP-PATCH-F-001","experiment_name":"B-Matrix debt ratio unit fix + 81 candidates","experiment_type":"B_MATRIX_RESEARCH","git_commit":"cf568bd","phase":"PATCH-F","factor_ids":["b_roe","b_gross_margin","b_pe_ttm","b_debt_ratio"]},{"experiment_id":"EXP-PATCH-H-001","experiment_name":"B-Matrix Current Snapshot 81 candidates profiled","experiment_type":"B_MATRIX_RESEARCH","git_commit":"dc4b980","phase":"PATCH-H","factor_ids":["b_roe","b_gross_margin","b_pe_ttm","b_debt_ratio","b_ocf_proxy","b_industry_roe_pct"]}]

RESEARCH_WORKFLOWS = {"full_replay":{"name":"Full Replay Workflow","steps":["load_data","pit_check","factor_compute","score","paper_action","outcome","metrics","report"],"allowed_experiment_types":["REPLAY","PAPER_REPLAY"]},"b_snapshot":{"name":"B-Matrix Current Snapshot","steps":["load_financial","load_price","pit_check","score_b","tier","report"],"allowed_experiment_types":["B_MATRIX_RESEARCH"]},"data_audit":{"name":"Data Audit","steps":["scan_sources","check_pit","check_ttl","check_coverage","report"],"allowed_experiment_types":["DATA_AUDIT"]}}
