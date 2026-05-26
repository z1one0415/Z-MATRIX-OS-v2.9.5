"""Report Writer — write validation report to runtime_reports/"""
from __future__ import annotations
import json
from pathlib import Path

def write_validation_report(*, report, output_path):
    path = Path(output_path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"write_status":"OK","output_path":str(path),"bytes":path.stat().st_size,"real_trade_allowed":False,"broker_order_allowed":False}
