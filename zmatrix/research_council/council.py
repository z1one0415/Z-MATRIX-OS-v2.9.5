"""V4.0-B2 Research Council — 12-Seat Virtual Research Council + Report Templates"""
from __future__ import annotations

RESEARCH_COUNCIL_SEATS = {
    "SEAT_01_MACRO_STRATEGIST": {"domain": "ZC10", "role": "宏观策略", "parser_scorer_policy": "PARSER_ONLY", "outputs": ["macro_regime", "liquidity_assessment", "risk_appetite"]},
    "SEAT_02_INDUSTRY_ANALYST": {"domain": "ZC10", "role": "行业分析师", "parser_scorer_policy": "PARSER_THEN_SCORER", "outputs": ["industry_phase", "sector_relative_strength", "chain_position"]},
    "SEAT_03_FINANCIAL_QUALITY": {"domain": "ZC10", "role": "财务质量", "parser_scorer_policy": "DETERMINISTIC_SCORER_ONLY", "outputs": ["b_score", "financial_health", "valuation_assessment"]},
    "SEAT_04_CATALYST_TRACKER": {"domain": "ZC35", "role": "催化追踪", "parser_scorer_policy": "PARSER_ONLY", "outputs": ["catalyst_status", "lifecycle_state", "residual_power"]},
    "SEAT_05_TECHNICAL_ANALYST": {"domain": "ZC30", "role": "技术分析", "parser_scorer_policy": "DETERMINISTIC_SCORER_ONLY", "outputs": ["r_score", "cycle_phase", "momentum_signal"]},
    "SEAT_06_EVENT_SPECIALIST": {"domain": "ZC35", "role": "事件专家", "parser_scorer_policy": "PARSER_ONLY", "outputs": ["event_evidence_level", "sell_on_news_risk", "event_impact_window"]},
    "SEAT_07_RISK_OFFICER": {"domain": "ZC50", "role": "风控官", "parser_scorer_policy": "DETERMINISTIC_SCORER_ONLY", "outputs": ["risk_flags", "position_limit_check", "beta_exposure"]},
    "SEAT_08_DEFENSIVE_ALLOCATOR": {"domain": "ZC45", "role": "防御配置", "parser_scorer_policy": "NO_LLM", "outputs": ["defensive_preview", "hedge_suitability", "tail_hedge_sim"]},
    "SEAT_09_EXECUTION_QUALITY": {"domain": "ZC40", "role": "执行质量", "parser_scorer_policy": "NO_LLM", "outputs": ["fillability_status", "board_structure", "chase_risk"]},
    "SEAT_10_FACTOR_ENGINEER": {"domain": "ZC30", "role": "因子工程", "parser_scorer_policy": "NO_LLM", "outputs": ["factor_scores", "ic_analysis", "decile_report"]},
    "SEAT_11_AUDITOR": {"domain": "ZSC", "role": "审计官", "parser_scorer_policy": "NO_LLM", "outputs": ["audit_trail", "evidence_chain", "compliance_check"]},
    "SEAT_12_COCKPIT_COMMANDER": {"domain": "ZSC", "role": "驾驶舱", "parser_scorer_policy": "NO_LLM", "outputs": ["system_status", "hard_gate_panel", "degraded_mode"]},
}

REPORT_TEMPLATES = {
    "TEMPLATE_01_MACRO_BRIEFING": {"category": "宏观简报", "seats": ["SEAT_01"], "blocks": ["macro_regime", "liquidity", "risk_appetite"]},
    "TEMPLATE_02_INDUSTRY_DEEP_DIVE": {"category": "行业深研", "seats": ["SEAT_02"], "blocks": ["industry_phase", "sector_strength", "chain_map"]},
    "TEMPLATE_03_STOCK_QUALITY": {"category": "个股质量", "seats": ["SEAT_03"], "blocks": ["b_score", "financial_health", "valuation"]},
    "TEMPLATE_04_CATALYST_TRACKER": {"category": "催化追踪", "seats": ["SEAT_04","SEAT_06"], "blocks": ["catalyst_status", "event_evidence", "residual_power"]},
    "TEMPLATE_05_TECHNICAL_CYCLE": {"category": "技术周期", "seats": ["SEAT_05"], "blocks": ["r_score", "cycle_phase", "momentum"]},
    "TEMPLATE_06_RISK_DASHBOARD": {"category": "风险仪表盘", "seats": ["SEAT_07"], "blocks": ["risk_flags", "position_limits", "beta"]},
    "TEMPLATE_07_DEFENSIVE_ALLOCATION": {"category": "防御配置", "seats": ["SEAT_08"], "blocks": ["defensive_preview", "hedge_suitability", "tail_hedge"]},
    "TEMPLATE_08_EXECUTION_REPORT": {"category": "执行报告", "seats": ["SEAT_09"], "blocks": ["fillability", "board_structure", "chase_risk"]},
    "TEMPLATE_09_FACTOR_ANALYSIS": {"category": "因子分析", "seats": ["SEAT_10"], "blocks": ["factor_scores", "ic_report"]},
    "TEMPLATE_10_AUDIT_TRAIL": {"category": "审计追踪", "seats": ["SEAT_11"], "blocks": ["audit_trail", "evidence_chain"]},
    "TEMPLATE_11_SYSTEM_STATUS": {"category": "系统状态", "seats": ["SEAT_12"], "blocks": ["system_status", "hard_gates", "degraded"]},
    "TEMPLATE_12_FULL_COUNCIL": {"category": "全理事会", "seats": ["SEAT_01","SEAT_02","SEAT_03","SEAT_04","SEAT_05","SEAT_06","SEAT_07","SEAT_08","SEAT_09","SEAT_10","SEAT_11","SEAT_12"], "blocks": ["all_domains"]},
}

HARD_GATE_REPORT_BLOCKS = {
    "BLOCK_ZC40_LIMIT_BOARD": {"gate": "ZC40", "field": "fillability_status", "rule": "NOT_FILLABLE → BLOCK new entry", "panel": "LimitBoardFillabilityPanel"},
    "BLOCK_ZC45_PROXY_HEDGE": {"gate": "ZC45", "field": "hedge_proxy_suitability", "rule": "ProxyHedgeStressTest must PASS before allocation preview", "panel": "ProxyHedgeStressPanel"},
    "BLOCK_RUNTIME_FAILOVER": {"gate": "RUNTIME", "field": "degraded_mode_active", "rule": "LLM failure → NO new judgment, stale cache only", "panel": "LLMFailoverPanel"},
    "BLOCK_LLM_SUBJECTIVE_SCORE": {"gate": "ZC00", "field": "subjective_score_allowed", "rule": "Categorically FORBIDDEN", "panel": "ParserScorerSplitPanel"},
}
