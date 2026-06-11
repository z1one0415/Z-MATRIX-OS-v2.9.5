"""
test_mock_payload_contract_alignment.py

Verify all fixture files match their expected contract schemas.
Tests structural validity of every JSON fixture.
"""

import json
import os
import pytest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
FIXTURE_DIR = os.path.join(_PROJECT_ROOT, "skillos", "frontend_handoff", "fixtures")


def _load_fixture(name):
    path = os.path.join(FIXTURE_DIR, name)
    with open(path, "r") as f:
        return json.load(f)


def _get_all_fixture_files():
    return sorted([f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")])


# --- Contract alignment tests ---

class TestDashboardSummaryContract:
    def test_top_level_key(self):
        data = _load_fixture("dashboard_summary.json")
        assert "dashboard_summary" in data

    def test_required_fields(self):
        d = _load_fixture("dashboard_summary.json")["dashboard_summary"]
        for key in ["system", "timestamp_utc", "last_run_utc", "status", "counts", "indicator_lights"]:
            assert key in d, f"Missing required field: {key}"

    def test_status_overall(self):
        d = _load_fixture("dashboard_summary.json")["dashboard_summary"]
        assert d["status"]["overall"] in ["NOMINAL", "DEGRADED", "ERROR", "OFFLINE"]

    def test_counts_values(self):
        d = _load_fixture("dashboard_summary.json")["dashboard_summary"]
        assert isinstance(d["counts"]["skills"], int)
        assert isinstance(d["counts"]["factors"], int)
        assert d["counts"]["skills"] > 0
        assert d["counts"]["factors"] > 0


class TestCapabilityListContract:
    def test_top_level_key(self):
        data = _load_fixture("capability_list.json")
        assert "capability_list" in data

    def test_items_list(self):
        data = _load_fixture("capability_list.json")
        assert isinstance(data["capability_list"]["items"], list)
        assert len(data["capability_list"]["items"]) > 0

    def test_item_schema(self):
        items = _load_fixture("capability_list.json")["capability_list"]["items"]
        for item in items:
            for key in ["id", "name", "status", "description", "depends_on"]:
                assert key in item, f"Missing key {key} in {item.get('id', 'unknown')}"
            assert item["status"] in ["READY", "DISABLED", "BLOCKED"]

    def test_status_counts_match(self):
        data = _load_fixture("capability_list.json")
        items = data["capability_list"]["items"]
        by_status = data["capability_list"]["by_status"]
        assert by_status["READY"] == sum(1 for i in items if i["status"] == "READY")
        assert by_status["DISABLED"] == sum(1 for i in items if i["status"] == "DISABLED")
        assert by_status["BLOCKED"] == sum(1 for i in items if i["status"] == "BLOCKED")


class TestFactorLibrarySummaryContract:
    def test_top_level_key(self):
        data = _load_fixture("factor_library_summary.json")
        assert "factor_library_summary" in data

    def test_factor_count(self):
        data = _load_fixture("factor_library_summary.json")
        assert data["factor_library_summary"]["total_factors"] == 23
        assert len(data["factor_library_summary"]["factors"]) == 23

    def test_factor_schema(self):
        factors = _load_fixture("factor_library_summary.json")["factor_library_summary"]["factors"]
        for f in factors:
            for key in ["id", "name", "category", "seal", "weight", "description"]:
                assert key in f, f"Missing key {key} in {f.get('id', 'unknown')}"
            assert f["seal"] in ["SEALED", "DRAFT", "DEPRECATED"]

    def test_matrix_counts_add_up(self):
        data = _load_fixture("factor_library_summary.json")["factor_library_summary"]
        ms = data["matrix_status"]
        total = ms["b_matrix_factors"] + ms["d_matrix_factors"] + ms["r_matrix_factors"] + ms["shared_factors"]
        assert total == 23


class TestCompositionGraphSummaryContract:
    def test_top_level_key(self):
        data = _load_fixture("composition_graph_summary.json")
        assert "composition_graph_summary" in data

    def test_nodes_and_edges(self):
        data = _load_fixture("composition_graph_summary.json")["composition_graph_summary"]
        assert len(data["nodes"]) == data["total_nodes"]
        assert len(data["edges"]) == data["total_edges"]
        assert data["total_nodes"] > 0
        assert data["total_edges"] > 0

    def test_node_schema(self):
        nodes = _load_fixture("composition_graph_summary.json")["composition_graph_summary"]["nodes"]
        for node in nodes:
            for key in ["id", "type", "label", "status"]:
                assert key in node, f"Missing key {key} in {node.get('id', 'unknown')}"

    def test_edge_refs_valid(self):
        data = _load_fixture("composition_graph_summary.json")["composition_graph_summary"]
        node_ids = {n["id"] for n in data["nodes"]}
        for edge in data["edges"]:
            assert edge["from"] in node_ids, f"Edge from={edge['from']} not in nodes"
            assert edge["to"] in node_ids, f"Edge to={edge['to']} not in nodes"


class TestResearchReportSummaryContract:
    def test_top_level_key(self):
        data = _load_fixture("research_report_summary.json")
        assert "research_report_summary" in data

    def test_sections_count(self):
        data = _load_fixture("research_report_summary.json")["research_report_summary"]
        assert len(data["sections"]) == 12

    def test_section_schema(self):
        sections = _load_fixture("research_report_summary.json")["research_report_summary"]["sections"]
        for s in sections:
            for key in ["id", "title", "status", "summary"]:
                assert key in s, f"Missing key {key} in section {s.get('id', 'unknown')}"
            assert 1 <= s["id"] <= 12

    def test_evidence_chain_hashes(self):
        data = _load_fixture("research_report_summary.json")["research_report_summary"]
        ec = data["evidence_chain"]
        for key in ["factor_lib_hash", "a1_hash", "b1_hash", "z2_hash", "z9_hash"]:
            assert key in ec
            assert ec[key].startswith("sha256:")

    def test_z9_snapshot(self):
        data = _load_fixture("research_report_summary.json")["research_report_summary"]
        z9 = data["z9_snapshot"]
        for key in ["calibration_status", "regime", "confidence_interval_95"]:
            assert key in z9


class TestZ9ReviewSummaryContract:
    def test_top_level_key(self):
        data = _load_fixture("z9_review_summary.json")
        assert "z9_review_summary" in data

    def test_node_disabled(self):
        data = _load_fixture("z9_review_summary.json")["z9_review_summary"]
        assert data["node_status"] == "DISABLED_DEFAULT"
        assert data["policy_ref"] == "P0-merge-decision-Z9-review-disabled-default"

    def test_review_labels(self):
        data = _load_fixture("z9_review_summary.json")["z9_review_summary"]
        assert len(data["review_labels"]) >= 4


class TestEvidenceChainDemoContract:
    def test_top_level_key(self):
        data = _load_fixture("evidence_chain_demo.json")
        assert "evidence_chain_demo" in data

    def test_steps_count(self):
        data = _load_fixture("evidence_chain_demo.json")["evidence_chain_demo"]
        assert len(data["steps"]) == 5

    def test_step_schema(self):
        steps = _load_fixture("evidence_chain_demo.json")["evidence_chain_demo"]["steps"]
        for s in steps:
            for key in ["step", "node", "action", "input_hash", "output_hash", "timestamp_utc", "status"]:
                assert key in s, f"Missing key {key} in step {s.get('step', 'unknown')}"
            assert s["status"] == "OK"

    def test_hash_continuity(self):
        data = _load_fixture("evidence_chain_demo.json")["evidence_chain_demo"]
        assert data["chain_integrity"]["verified"] is True
        assert data["chain_integrity"]["hash_continuity"] == "UNBROKEN"


class TestRunStateDemoContract:
    def test_top_level_key(self):
        data = _load_fixture("run_state_demo.json")
        assert "run_state_demo" in data

    def test_phases_count(self):
        data = _load_fixture("run_state_demo.json")["run_state_demo"]
        assert len(data["phases"]) == 11

    def test_abort_reasons_empty(self):
        data = _load_fixture("run_state_demo.json")["run_state_demo"]
        assert data["abort_reasons"] == []

    def test_phase_schema(self):
        phases = _load_fixture("run_state_demo.json")["run_state_demo"]["phases"]
        for p in phases:
            for key in ["phase", "status", "elapsed_sec", "output"]:
                assert key in p, f"Missing key {key} in phase {p.get('phase', 'unknown')}"


class TestGateStateDemoContract:
    def test_top_level_key(self):
        data = _load_fixture("gate_state_demo.json")
        assert "gate_state_demo" in data

    def test_gates_count(self):
        data = _load_fixture("gate_state_demo.json")["gate_state_demo"]
        assert len(data["gates"]) == 7

    def test_f7_0_preconditions(self):
        gates = _load_fixture("gate_state_demo.json")["gate_state_demo"]["gates"]
        f70 = gates[0]
        assert f70["gate_id"] == "F7.0"
        assert len(f70["preconditions"]) == 7

    def test_f7_2_last(self):
        gates = _load_fixture("gate_state_demo.json")["gate_state_demo"]["gates"]
        assert gates[-1]["gate_id"] == "F7.2"

    def test_all_passed(self):
        data = _load_fixture("gate_state_demo.json")["gate_state_demo"]
        assert data["f7_gate_chain"]["gates_passed"] == 7
        assert data["f7_gate_chain"]["gates_failed"] == 0


class TestAuditTrailDemoContract:
    def test_top_level_key(self):
        data = _load_fixture("audit_trail_demo.json")
        assert "audit_trail_demo" in data

    def test_events_count(self):
        data = _load_fixture("audit_trail_demo.json")["audit_trail_demo"]
        assert len(data["events"]) == data["total_events"]

    def test_event_schema(self):
        events = _load_fixture("audit_trail_demo.json")["audit_trail_demo"]["events"]
        for e in events:
            for key in ["seq", "timestamp_utc", "actor", "action", "detail", "status"]:
                assert key in e, f"Missing key {key} in event {e.get('seq', 'unknown')}"

    def test_seq_monotonic(self):
        events = _load_fixture("audit_trail_demo.json")["audit_trail_demo"]["events"]
        seqs = [e["seq"] for e in events]
        assert seqs == sorted(seqs)
        assert seqs == list(range(1, len(seqs) + 1))


class TestErrorAbortDegradedDemoContract:
    def test_top_level_key(self):
        data = _load_fixture("error_abort_degraded_demo.json")
        assert "error_abort_degraded_demo" in data

    def test_scenarios_count(self):
        data = _load_fixture("error_abort_degraded_demo.json")["error_abort_degraded_demo"]
        assert len(data["scenarios"]) == 9

    def test_scenario_types_distributed(self):
        scenarios = _load_fixture("error_abort_degraded_demo.json")["error_abort_degraded_demo"]["scenarios"]
        types = [s["type"] for s in scenarios]
        assert types.count("ERROR") == 3
        assert types.count("ABORT") == 3
        assert types.count("DEGRADED") == 3

    def test_scenario_schema(self):
        scenarios = _load_fixture("error_abort_degraded_demo.json")["error_abort_degraded_demo"]["scenarios"]
        for s in scenarios:
            for key in ["type", "scenario_id", "title", "severity", "detail", "ui_state"]:
                assert key in s, f"Missing key {key} in {s.get('scenario_id', 'unknown')}"


# --- General fixture validity ---

class TestAllFixturesValidJson:
    def test_all_files_are_valid_json(self):
        for fname in _get_all_fixture_files():
            path = os.path.join(FIXTURE_DIR, fname)
            with open(path, "r") as f:
                json.load(f)  # Will raise JSONDecodeError if invalid


class TestAllFixturesUniqueTopLevelKey:
    def test_unique_top_level_keys(self):
        """Each fixture file should have a single top-level key that matches its purpose."""
        keys = {}
        for fname in _get_all_fixture_files():
            data = _load_fixture(fname)
            keys[fname] = list(data.keys())
        # No fixture should have empty data
        for fname, k in keys.items():
            assert len(k) >= 1, f"{fname} has no top-level keys"
