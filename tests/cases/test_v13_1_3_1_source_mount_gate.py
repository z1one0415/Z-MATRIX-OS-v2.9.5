"""V13.1.3.1 Tests"""
import json;from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent;C=W/"runtime_reports"/"cases"
def load(n):p=C/n;assert p.exists();return json.loads(p.read_text())
def test_inventory_no_gitkeep_accepted():
    for f in load("v13_1_3_1_mounted_file_inventory.json")["files"]:
        if f.get("is_placeholder"):assert f["accepted_for_validation"]is False
def test_inventory_accept_zero():assert load("v13_1_3_1_mounted_file_inventory.json")["accepted_for_validation_count"]==0
def test_schema_nosource_5():assert load("v13_1_3_1_strict_source_schema_validation.json")["no_source_group_count"]==5
def test_coverage_nosource_5():assert load("v13_1_3_1_strict_coverage_validation.json")["no_source_group_count"]==5
def test_asof_nosource_5():assert load("v13_1_3_1_strict_asof_validation.json")["no_source_group_count"]==5
def test_decision_mv_0():assert load("v13_1_3_1_mount_decision.json")["mount_validated_group_count"]==0
def test_readiness_blocked_8():assert load("v13_1_3_1_candidate_mount_readiness.json")["candidate_mount_blocked_count"]==8
def test_audit_pass():assert"PASS"in load("v13_1_3_1_source_mount_audit.json")["status"]
def test_closeout_mount_missing():assert"MOUNT_MISSING"in load("v13_1_3_1_source_mount_closeout.json")["recommended_next_action"]
def test_v13_2_blocked():assert load("v13_1_3_1_source_mount_audit.json")["ready_for_v13_2_bucket_construction_next_stage"]is False
def test_fc():fc=load("v13_1_3_1_source_mount_full_chain.json");assert fc["ready_for_v13_1_4_feature_materialization_next_stage"]is False
