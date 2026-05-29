# allowlist: forbidden-token-definition
from __future__ import annotations
"""v3.5.20-PATCH-A Scope Lock — 不可动摇的边界"""
PATCH_A_VERSION = "V3520_PATCH_A_SCOPE_LOCK_V10"
PATCH_A_SCOPE = {
    "patch_id": "V3520-PATCH-A",
    "patch_name": "Parameter Trust Hardening",
    "base_version": "v3.5.20 Research OS RC",
    "version_ceiling": "v3.5.20",
    "v36_allowed": False,
    "v40_allowed": False,
    "strategy_logic_modified": False,
    "production_classifier_modified": False,
    "real_trade_allowed": False,
    "broker_order_allowed": False,
    "auto_buy_allowed": False,
    "auto_sell_allowed": False,
    "runtime_enabled": False,
    "scope": [
        "数据可信度加固",
        "回测标签可信度加固",
        "交易成本可信度加固",
        "参数可信度加固",
        "证据链可信度加固",
    ],
    "out_of_scope": [
        "策略逻辑修改",
        "B/R/D 评分公式优化",
        "实盘启用",
        "生产分类器替换",
        "L2/L3旧模块迁移",
        "v4.0功能提前实现",
    ],
}

PATCH_A_ACCEPTANCE_MATRIX = {
    "PA-A-001": {"patch":1,"name":"Outcome Horizon Gate","verify":"verify_patch_a_outcome_horizon.sh","test":"tests/test_patch_a_outcome_horizon.py","fail_if":"T20/T60 metrics use insufficient forward data"},
    "PA-A-002": {"patch":2,"name":"Data Contract + PIT","verify":"verify_patch_a_pit_rules.sh","test":"tests/test_patch_a_pit_rules.py","fail_if":"any future fact used in decision"},
    "PA-A-003": {"patch":3,"name":"B-Matrix Foundation","verify":"verify_patch_a_b_matrix.sh","test":"tests/test_patch_a_b_matrix.py","fail_if":"B-Matrix coverage < 70% or ROLE_CORE source != MATRIX_B_BASE"},
    "PA-A-004": {"patch":4,"name":"D-Matrix Foundation","verify":"verify_patch_a_d_matrix.sh","test":"tests/test_patch_a_d_matrix.py","fail_if":"D-Matrix signals without event+price+flow resonance"},
    "PA-A-005": {"patch":5,"name":"Trading Cost Model","verify":"verify_patch_a_trading_cost.sh","test":"tests/test_patch_a_trading_cost.py","fail_if":"net_return not computed or limit board ignored"},
    "PA-A-006": {"patch":6,"name":"Parameter Trust Map","verify":"verify_patch_a_parameter_trust.sh","test":"tests/test_patch_a_parameter_trust.py","fail_if":"T4/T5 claim without sample-out validation"},
    "PA-A-007": {"patch":7,"name":"Evidence Status Audit","verify":"verify_patch_a_evidence_status.sh","test":"tests/test_patch_a_evidence_status.py","fail_if":"file-exists treated as evidence-ready"},
}

PATCH_A_SAFETY = {"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"auto_position_close_allowed":False,"real_z9_write_allowed":False,"hermes_memory_write_allowed":False,"auto_calibration_allowed":False,"runtime_enabled":False,"classifier_production_write_allowed":False,"role_definition_production_write_allowed":False,"legacy_runtime_rewrite_allowed":False}
