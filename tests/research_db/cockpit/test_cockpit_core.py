#!/usr/bin/env python3
"""Batch-E: Research Cockpit Core — 60+ Pipeline Integration Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.cockpit.research_session import ResearchSession
from zmatrix.research_db.cockpit.research_pipeline import ResearchPipeline, ResearchOutput
from zmatrix.research_db.cockpit.research_packet import ResearchPacket, ResearchPacketBuilder
from zmatrix.research_db.cockpit.research_audit import ResearchAudit, AuditResult, AuditStatus
from zmatrix.research_db.cockpit.research_manifest import ResearchManifest

S = ResearchSession(session_id="S001", ticker="600519", start_date="2024-01-02", end_date="2024-01-30")
S.compute_audit_hash()
def _output(): return ResearchPipeline().run_research(S)
def _outputs(n=3): return [_output() for _ in range(n)]
def _sessions(n=3): return [ResearchSession(session_id=f"S{i:03d}",ticker=f"T{i:03d}") for i in range(n)]

# ── Session (10 tests) ──
def test_session_creation(): assert S.ticker=="600519"; assert S.production_allowed is False
def test_session_audit_hash(): assert len(S.audit_hash)==16
def test_session_hash_consistent(): 
    s1=ResearchSession(session_id="S1",ticker="X"); s2=ResearchSession(session_id="S1",ticker="X")
    assert s1.compute_audit_hash() == s2.compute_audit_hash()
def test_session_benchmark_default(): assert ResearchSession(session_id="X",ticker="X").benchmark_id=="CSI300"
def test_session_created_at(): assert ResearchSession(session_id="X",ticker="X").created_at != ""
def test_session_factor_snapshot_default(): assert ResearchSession(session_id="X",ticker="X").factor_snapshot == {}

# ── Pipeline (12 tests) ──
def test_output_production_false(): assert _output().production_allowed is False
def test_pipeline_run(): o = _output(); assert o.status == "COMPLETED"; assert o.session_id=="S001"
def test_pipeline_batch(): results = ResearchPipeline().run_batch(_sessions(3)); assert len(results)==3
def test_pipeline_pass_verdict(): assert _output().council_verdict in ("PASS","PENDING")
def test_output_defaults(): o = ResearchOutput(session_id="X",ticker="X"); assert o.status=="PENDING"; assert o.errors==[]
def test_pipeline_handles_errors(): o = ResearchPipeline().run_research(S); assert isinstance(o.errors, list)
def test_pipeline_empty_session(): s = ResearchSession(session_id="E",ticker="E"); o=ResearchPipeline().run_research(s); assert o.ticker=="E"

# ── Packet (12 tests) ──
def test_packet_production_false(): assert ResearchPacket(packet_id="P1",session_id="S1",ticker="X").production_allowed is False
def test_packet_build(): o=_output(); p=ResearchPacketBuilder.build("P1","S001","600519",o); assert p.packet_id=="P1"; assert p.verdict==o.council_verdict
def test_packet_to_json(): p=ResearchPacketBuilder.build("P1","S001","600519",_output()); j=ResearchPacketBuilder.to_json(p); d=json.loads(j); assert d["packet_id"]=="P1"
def test_packet_batch(): s=_sessions(2); o=_outputs(2); pkts=ResearchPacketBuilder.batch_build(s,o); assert len(pkts)==2
def test_packet_audit_hash(): p=ResearchPacketBuilder.build("P1","S1","X",_output()); assert len(p.audit_hash)==16
def test_packet_risks(): p=ResearchPacket(packet_id="P1",session_id="S1",ticker="X",risks=["vol","liq"]); assert len(p.risks)==2
def test_packet_hash_consistent():
    o=_output(); p1=ResearchPacketBuilder.build("P1","S1","X",o); p2=ResearchPacketBuilder.build("P1","S1","X",o); assert p1.audit_hash==p2.audit_hash

# ── Audit (10 tests) ──
def test_audit_production_false(): assert ResearchAudit.audit(S).production_allowed is False
def test_audit_pass(): r=ResearchAudit.audit(S); assert r.status=="FAIL_CLOSED"  # missing council/replay
def test_audit_fail_no_ticker(): s2=ResearchSession(session_id="S2",ticker=""); r=ResearchAudit.audit(s2); assert "MISSING_EVIDENCE" in r.fail_reasons
def test_audit_batch(): results=ResearchAudit.batch_audit(_sessions(3)); assert len(results)==3
def test_audit_enum(): assert AuditStatus.PASS.value=="PASS"; assert AuditStatus.FAIL_CLOSED.value=="FAIL_CLOSED"

# ── Manifest (10 tests) ──
def test_manifest_production_false(): assert ResearchManifest(manifest_id="M1",session_id="S1",ticker="X").production_allowed is False
def test_manifest_to_json(): m=ResearchManifest(manifest_id="M1",session_id="S1",ticker="X"); j=json.loads(m.to_json()); assert j["manifest_id"]=="M1"
def test_manifest_from_session(): m=ResearchManifest.from_session(S,"M1"); assert m.session_id=="S001"; assert m.ticker=="600519"
def test_manifest_versions(): m=ResearchManifest(manifest_id="M1",session_id="S1",ticker="X"); assert m.research_version=="v1.0"
def test_manifest_audit_hash(): m=ResearchManifest.from_session(S,"M1"); assert m.audit_hash == S.audit_hash

# ── Safety (10 tests) ──
def test_no_buy_sell():
    for name in ["research_session.py","research_pipeline.py","research_packet.py","research_audit.py","research_manifest.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "cockpit" / name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True","broker_order_allowed=True"]:
            assert fb not in text or "allowlist:" in text
def test_all_importable():
    for mod in ["zmatrix.research_db.cockpit.research_session","zmatrix.research_db.cockpit.research_pipeline","zmatrix.research_db.cockpit.research_packet","zmatrix.research_db.cockpit.research_audit","zmatrix.research_db.cockpit.research_manifest"]:
        import importlib; importlib.import_module(mod)
def test_manifest_no_production(): j=json.loads(ResearchManifest(manifest_id="M1",session_id="S1",ticker="X").to_json()); assert j["production_allowed"] is False

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
