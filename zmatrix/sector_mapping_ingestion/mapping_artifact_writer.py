from __future__ import annotations
import csv
from pathlib import Path
from zmatrix.sector_mapping_ingestion.schema import DEFAULT_SECTOR_MAPPING_SAFETY

def write_sector_mapping_artifact(*, sector_mapping: dict, output_path="data/metadata/sector_mapping_v3510.csv", max_bytes=5_000_000) -> dict:
    p = Path(output_path); p.parent.mkdir(parents=True,exist_ok=True)
    rows = list((sector_mapping or {}).values()); fields = ["ticker","name","sector","industry","sector_code","theme","market","list_date","source_file"]
    with open(p,"w",encoding="utf-8-sig",newline="") as f:
        w = csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for r in rows: w.writerow({k:r.get(k) for k in fields})
    sz = p.stat().st_size; git_ok = sz <= max_bytes
    return {"writer_version":"V3510_MAPPING_ARTIFACT_WRITER_V10","output_path":str(p),"row_count":len(rows),"size_bytes":sz,"git_track_allowed":git_ok,"oversize_warning":not git_ok,"real_trade_allowed":False,"broker_order_allowed":False,"safety":dict(DEFAULT_SECTOR_MAPPING_SAFETY)}
