from __future__ import annotations
from zmatrix.sector_clock_foundation.sector_mapping_discovery import discover_sector_mapping
from zmatrix.sector_clock_foundation.sector_index_discovery import discover_sector_indexes
from zmatrix.sector_clock_foundation.synthetic_sector_basket import build_synthetic_sector_basket_preview
from zmatrix.sector_clock_foundation.stock_sector_joiner import join_stock_sector_mapping
from zmatrix.sector_clock_foundation.matrix_clock_metadata import build_matrix_clock_metadata
from zmatrix.sector_clock_foundation.data_decay_penalty import calculate_data_decay_penalty
from zmatrix.sector_clock_foundation.policy import validate_sector_clock_foundation_report
from zmatrix.sector_clock_foundation.schema import DEFAULT_SECTOR_CLOCK_SAFETY

def build_sector_clock_foundation_report(*, replay_rows: list[dict], data_root=".") -> dict:
    sm = discover_sector_mapping(data_root=data_root)
    si = discover_sector_indexes(data_root=data_root)
    syn = build_synthetic_sector_basket_preview(sector_mapping=sm.get("sector_mapping",{}), max_sectors=50) if si.get("sector_index_status")=="DATA_INSUFFICIENT" and sm.get("sector_mapping_status") in ("READY","PARTIAL") else {}
    joined = join_stock_sector_mapping(rows=replay_rows, sector_mapping=sm.get("sector_mapping",{}))
    bm = build_matrix_clock_metadata(matrix_type="B", matrix_name="B_MATRIX", as_of_date=None)
    rm = build_matrix_clock_metadata(matrix_type="R", matrix_name="R_MATRIX", as_of_date=None)
    dm = build_matrix_clock_metadata(matrix_type="D", matrix_name="D_MATRIX", as_of_date=None)
    decay = {"B":calculate_data_decay_penalty(matrix_type="B",age_days=bm.get("age_days"),ttl_days=bm.get("ttl_days")),"R":calculate_data_decay_penalty(matrix_type="R",age_days=rm.get("age_days"),ttl_days=rm.get("ttl_days")),"D":calculate_data_decay_penalty(matrix_type="D",age_days=dm.get("age_days"),ttl_days=dm.get("ttl_days"))}
    report = {"report_version":"V359_SECTOR_CLOCK_FOUNDATION_REPORT_V10","mode":"FOUNDATION_ONLY","sector_mapping_discovery":sm,"sector_index_discovery":si,"synthetic_sector_basket_preview":syn,"stock_sector_join":{"total_rows":joined.get("total_rows"),"sector_join_ready_count":joined.get("sector_join_ready_count"),"sector_join_coverage":joined.get("sector_join_coverage"),"sector_join_status":joined.get("sector_join_status")},"matrix_clock_metadata":{"B":bm,"R":rm,"D":dm},"data_decay_penalty_preview":decay,"production_strategy_modified":False,"real_trade_allowed":False,"broker_order_allowed":False,"auto_buy_allowed":False,"auto_sell_allowed":False,"runtime_enabled":False,"production_yaml_write_allowed":False,"production_parameter_write_allowed":False,"production_weight_adjustment_allowed":False,"synthetic_sector_index_production_allowed":False,"safety":dict(DEFAULT_SECTOR_CLOCK_SAFETY)}
    report["policy_violations"] = validate_sector_clock_foundation_report(report)
    ck = report["matrix_clock_metadata"]; ck_ready = all(ck.get(k,{}).get("metadata_ready") for k in ("B","R","D"))
    sj = report["stock_sector_join"]["sector_join_status"]
    report["foundation_status"] = "FOUNDATION_READY" if sj=="READY" and ck_ready else "FOUNDATION_SECTOR_READY_CLOCK_INSUFFICIENT" if sj in ("READY","PARTIAL") else "FOUNDATION_SECTOR_DATA_INSUFFICIENT"
    report["recommended_next_step"] = {"FOUNDATION_READY":"v3.5.10 Regime × Sector Joint Attribution","FOUNDATION_SECTOR_READY_CLOCK_INSUFFICIENT":"v3.5.10 Matrix Clock Metadata Enrichment","FOUNDATION_SECTOR_DATA_INSUFFICIENT":"v3.5.10 Sector Mapping Data Ingestion"}.get(report["foundation_status"])
    return report
