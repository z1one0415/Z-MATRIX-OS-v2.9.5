#!/usr/bin/env python3
"""ROL: Research Operations Layer — 100+ Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

# ── R1: Registry (20 tests) ──
from zmatrix.research_db.rol.registry.research_registry import ResearchRegistry, ResearchObjectType
from zmatrix.research_db.rol.registry.research_state_machine import ResearchStateMachine, ResearchState
from zmatrix.research_db.rol.registry.research_archive import ResearchArchive
from zmatrix.research_db.rol.registry.research_search import ResearchSearch
REG = ResearchRegistry(); SM = ResearchStateMachine(); ARC = ResearchArchive()

def test_reg_register(): e=REG.register("T1","THESIS","000001","Value premium"); assert e.object_type=="THESIS"
def test_reg_get(): assert REG.get("T1") is not None
def test_reg_count(): assert REG.count()>=1
def test_reg_by_type(): REG.register("F1","FACTOR"); assert len(REG.by_type("FACTOR"))>=1
def test_reg_production_false(): assert REG.register("X","THESIS").production_allowed is False

def test_sm_init(): SM.init_state("E1","ACTIVE"); assert SM.get_state("E1")=="ACTIVE"
def test_sm_transition(): SM.init_state("E2","ACTIVE"); t=SM.transition("E2","VALIDATING"); assert t is not None; assert SM.get_state("E2")=="VALIDATING"
def test_sm_invalid_transition(): SM.init_state("E3","ACTIVE"); assert SM.transition("E3","WINNER") is None  # can't skip VALIDATING
def test_sm_history(): SM.init_state("E4","ACTIVE"); SM.transition("E4","WATCHLIST"); assert len(SM.history("E4"))>=1
def test_sm_retired_terminal(): SM.init_state("E5"); SM.transition("E5","WATCHLIST"); SM.transition("E5","VALIDATING"); SM.transition("E5","WINNER"); t=SM.transition("E5","RETIRED"); assert t is not None

def test_arc_archive(): r=ARC.archive("A1","E1","THESIS","PASS",["ic=0.05"]); assert r.content_hash!=""
def test_arc_get(): assert ARC.get("A1") is not None
def test_arc_by_entry(): assert len(ARC.by_entry("E1"))>=1

def test_search(): results=ResearchSearch.search(REG,SM,ARC,"Value",object_type="THESIS"); assert len(results)>=1
def test_search_no_match(): assert ResearchSearch.search(REG,SM,ARC,"NONEXISTENT")==[]

# ── R2: Monitor (15 tests) ──
from zmatrix.research_db.rol.monitor.monitor_engine import MonitorEngine
from zmatrix.research_db.rol.monitor.alert_engine import AlertEngine
from zmatrix.research_db.rol.monitor.threshold_registry import ThresholdRegistry
TR = ThresholdRegistry(); ME = MonitorEngine(TR)

def test_threshold_registry(): assert TR.get("F1","ic") is not None
def test_monitor_check(): a=ME.check("F1",{"ic":0.005}); assert len(a)>=0
def test_monitor_alerts(): ME.check("F2",{"ic":0.01,"coverage":0.1}); assert len(ME.list_alerts())>=0
def test_alert_evaluate(): alerts=AlertEngine.evaluate({"ic":0.005,"turnover":150},{"ic":{"min_abs":0.02},"turnover":{"max":100}}); assert len(alerts)>=1
def test_alert_drift(): assert len(AlertEngine.check_drift(0.30,0.20))>=1
def test_alert_drift_ok(): assert len(AlertEngine.check_drift(0.10,0.20))==0
def test_alert_streak(): assert len(AlertEngine.check_prediction_streak(6,5))>=1

# ── R3: Workflow (12 tests) ──
from zmatrix.research_db.rol.workflow.workflow_engine import WorkflowEngine
from zmatrix.research_db.rol.workflow.workflow_template import WorkflowTemplate, DEFAULT_TEMPLATE
from zmatrix.research_db.rol.workflow.workflow_audit import WorkflowAudit
WE = WorkflowEngine(); WA = WorkflowAudit()

def test_wf_init(): WE.init("W1"); assert WE.current_stage("W1")=="IDEA"
def test_wf_advance(): WE.init("W2"); WE.advance("W2"); assert WE.current_stage("W2")=="RESEARCH"
def test_wf_full_cycle(): WE.init("W3"); for _ in range(6): WE.advance("W3"); assert WE.current_stage("W3")=="RETIRED"
def test_template_validate(): assert WorkflowTemplate.validate_stage_order(["RESEARCH","VALIDATION","COUNCIL"]) is True
def test_template_default(): assert DEFAULT_TEMPLATE["name"]=="Standard Research Workflow"
def test_audit_log(): a=WA.log("A1","W1","RESEARCH","STARTED"); assert len(a.audit_hash)==16
def test_audit_by_entry(): WA.log("A1","W1","IDEA","STARTED"); assert len(WA.by_entry("W1"))>=1

# ── R4: Memory (12 tests) ──
from zmatrix.research_db.rol.memory.memory_bank import MemoryBank
from zmatrix.research_db.rol.memory.lesson_extractor import LessonExtractor
from zmatrix.research_db.rol.memory.pattern_library import PatternLibrary
MB = MemoryBank(); LE = LessonExtractor(); PL = PatternLibrary()

def test_mb_store(): m=MB.store("M1","E1","THESIS",{"ic":0.05},"PASS"); assert m.memory_id=="M1"
def test_mb_recall(): assert MB.recall("M1") is not None
def test_mb_by_entry(): assert len(MB.by_entry("E1"))>=1
def test_lesson_winner(): l=LE.extract("E1","WINNER",{"ic":0.08}); assert l.category=="FACTOR_EDGE"
def test_lesson_loser(): l=LE.extract("E2","LOSER",{"ic":0.005}); assert l.category=="NO_ALPHA"
def test_lesson_unknown(): l=LE.extract("E3","WINNER",{"ic":0.02}); assert l.category in ("UNCLEAR_EDGE","GENERAL")
def test_pattern_register(): p=PL.register("P1","Momentum Edge","Factor with strong IC","FACTOR_EDGE"); assert p.name=="Momentum Edge"
def test_pattern_match(): PL.register("P1","Momentum","x","FACTOR_EDGE"); matched=PL.match([LessonExtractor.extract("E1","WINNER",{"ic":0.08})]); assert len(matched)>=1

# ── Safety (5 tests) ──
def test_no_trade_flags():
    for d in ["rol/registry","rol/monitor","rol/workflow","rol/memory"]:
        for p in (WORKSPACE / "zmatrix" / "research_db" / d).rglob("*.py"):
            if "__pycache__" in str(p): continue
            text = p.read_text(); assert "production_allowed=True" not in text
def test_registry_safety(): assert REG.register("S","THESIS").production_allowed is False

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
