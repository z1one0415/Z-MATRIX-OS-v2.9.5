"""Research Asset Index v1.0 — 研究结论索引边界 (v2.9.10-dev)
本阶段不导入 Obsidian 全文。只定义索引边界。
"""
from __future__ import annotations

RESEARCH_ASSET_INDEX_POLICY = {
    "external_memory_root": "~/Documents/openclaw memory/Z2信息熔炉/",
    "index_mode": "metadata_only",
    "full_text_import_allowed": False,
    "git_import_allowed": False,
    "real_trade_allowed": False,
    "default_status": "EXTERNAL_UNINDEXED",
}

RESEARCH_OUTPUT_INDEX_FIELDS = [
    "research_id","source_path","ticker","company","chain","research_type",
    "conclusion","confidence","evidence_grade","linked_matrix",
    "valid_until","decay_status","created_at",
]

def check_research_asset_index_policy() -> list[str]:
    violations = []
    if RESEARCH_ASSET_INDEX_POLICY.get("full_text_import_allowed"):
        violations.append("full_text_import_allowed should be False")
    if RESEARCH_ASSET_INDEX_POLICY.get("git_import_allowed"):
        violations.append("git_import_allowed should be False")
    if RESEARCH_ASSET_INDEX_POLICY.get("real_trade_allowed"):
        violations.append("real_trade_allowed should be False")
    return violations
