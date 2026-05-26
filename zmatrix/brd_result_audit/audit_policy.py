"""Audit Policy — 13 blocked fields"""
from __future__ import annotations
from zmatrix.brd_result_audit.schema import AUDIT_BLOCKED_FIELDS

def validate_brd_result_audit_report(record):
    e=[]
    if not isinstance(record,dict): return ["record must be dict"]
    for f in AUDIT_BLOCKED_FIELDS:
        if record.get(f) is True: e.append(f"{f} must be False")
    s=record.get("safety",{}); s={} if s is None else s
    if not isinstance(s,dict): e.append("safety must be dict"); s={}
    for f in AUDIT_BLOCKED_FIELDS:
        if s.get(f) is True: e.append(f"safety.{f} must be False")
    return e
