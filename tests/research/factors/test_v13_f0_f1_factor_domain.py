"""V13.F0_F1 — factor domain aggregate test."""
import json;from pathlib import Path
C1=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"audit"
C2=Path(__file__).resolve().parent.parent.parent/"configs"/"research"/"factors"
C3=Path(__file__).resolve().parent.parent.parent/"runtime_reports"/"research"/"factors"
def L1(n):return json.loads((C1/n).read_text())if (C1/n).exists()else{}
def L2(n):return json.loads((C2/n).read_text())if (C2/n).exists()else{}
def L3(n):return json.loads((C3/n).read_text())if (C3/n).exists()else{}
s0=L1("v13_f0_f1_main_research_code_reality_audit.json")
sc=L2("factor_entity_schema_v1.json")
pl=L2("factor_lifecycle_policy_v1.json")
rg=L2("factor_domain_registry_v1.json")
sd=L3("current_factor_seed_registry.json")
co=L3("v13_f0_f1_factor_domain_seed_closeout.json")
def test_audit():assert s0;assert s0.get("main_research_system_is_primary")is True
def test_skillos_protocol():assert s0.get("skillos_is_protocol_layer")is True
def test_schema():assert sc;assert"trade_signal"in sc.get("forbidden_fields",[])
def test_lifecycle():assert pl;"ALPHA_VALIDATED"in pl.get("forbidden_states",[])
def test_registry_20():assert len(rg.get("factors",[]))==20
def test_seeds_2():assert sd.get("current_seed_factor_count")==2
def test_f01():assert sd["seeds"][0]["factor_id"]=="F01"
def test_f01_state():assert sd["seeds"][0]["current_lifecycle_state"]=="ORANGE_MONITORING"
def test_f01_waiting():assert"2026-05-29"in sd["seeds"][0]["current_runtime_state"].get("waiting_for","")
def test_f02():assert sd["seeds"][1]["factor_id"]=="F02"
def test_f02_state():assert sd["seeds"][1]["current_lifecycle_state"]=="RESEARCH_CANDIDATE_FROZEN"
def test_f02_collision():assert sd["seeds"][1].get("formula_identity_state",{}).get("proxy_collision_detected")is True
def test_alias_blocked():assert"DOWNSIDE_VOL_TILT"in rg.get("blocked_aliases",[])
def test_alias2_blocked():assert"DRAWDOWN_RECOVERY_QUALITY"in rg.get("blocked_aliases",[])
def test_materialized_0():assert co.get("materialized_factor_count_this_round")==0
def test_multi_composite_false():assert co.get("multi_factor_composite_built")is False
def test_skillos_unchanged():assert co.get("skillos_protocol_modified")is False
def test_frontend_unchanged():assert co.get("frontend_modified")is False
def test_no_v13_6():assert co.get("v13_6_allowed")is False
def test_no_paper():assert co.get("paper_trading_allowed")is False
def test_alpha():assert co.get("alpha_claim_allowed")is False
def test_prod():assert co.get("production")=="BLOCKED"
