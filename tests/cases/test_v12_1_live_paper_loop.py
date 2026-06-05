"""V12.1: Live Paper Loop Tests — 14 test cases covering contract, registry, schedule, status, delta, audit, closeout, safety."""
import json
from pathlib import Path

W = Path(__file__).resolve().parent.parent.parent
C = W / "runtime_reports" / "cases"

FORBIDDEN_WORDS = [
    "BUY", "SELL", "LONG", "SHORT", "WEIGHT", "POSITION",
    "TARGET_PRICE", "TAKE_PROFIT", "STOP_LOSS", "ORDER",
]


def load(name: str) -> dict:
    p = C / name
    assert p.exists(), f"Missing runtime: {name}"
    return json.loads(p.read_text())


# ── Contract Tests ──

def test_contract_based_on_v12_closeout_confirmed():
    c = load("v12_1_live_paper_contract.json")
    assert c["status"] == "V12_1_LIVE_PAPER_CONTRACT_BUILT"
    assert "CONFIRMED" in c["source_v12_closeout"]


def test_contract_has_correct_counts():
    c = load("v12_1_live_paper_contract.json")
    assert c["source_signal_count"] == 12
    assert c["pending_observation_count"] == 8
    assert c["rejected_observation_count"] == 4
    assert c["activation_policy"] == "PENDING_ONLY"
    assert c["rejected_policy"] == "KEEP_REJECTED"


# ── Registry Tests ──

def test_registry_only_activates_pending():
    r = load("v12_1_live_paper_run_registry.json")
    assert r["active_live_paper_run_count"] == 8
    assert r["rejected_preserved_count"] == 4
    # Verify: all active runs have LIVE_PAPER_PENDING
    active = [run for run in r["runs"] if run["run_status"] == "LIVE_PAPER_PENDING"]
    assert len(active) == 8


def test_registry_does_not_activate_rejected():
    r = load("v12_1_live_paper_run_registry.json")
    rejected = [run for run in r["runs"] if run["run_status"] == "PRESERVED_REJECTED"]
    assert len(rejected) == 4
    # Verify no TRACKING_REJECTED observation is activated
    for run in rejected:
        assert run["run_status"] != "LIVE_PAPER_PENDING"
    assert r["active_live_paper_run_count"] == r["source_observation_count"] - r["rejected_preserved_count"]


def test_registry_action_counts_zero():
    r = load("v12_1_live_paper_run_registry.json")
    assert r["investment_action_count"] == 0
    assert r["trade_action_count"] == 0


# ── Due Schedule Tests ──

def test_due_schedule_initial_waiting():
    s = load("v12_1_live_paper_due_schedule.json")
    assert s["waiting_for_future_label_count"] == s["scheduled_run_count"]
    assert s["ready_for_completion"] is False
    assert "LIVE_PAPER_FUTURE_LABELS_NOT_AVAILABLE" in s["blocking_reasons"]


def test_due_schedule_only_active_runs():
    s = load("v12_1_live_paper_due_schedule.json")
    r = load("v12_1_live_paper_run_registry.json")
    # Schedule count must equal active count from registry
    assert s["scheduled_run_count"] == r["active_live_paper_run_count"]


def test_due_schedule_no_trading():
    s = load("v12_1_live_paper_due_schedule.json")
    for item in s.get("schedule_items", []):
        assert item["investment_action"] == "NONE"
        assert item["trade_action"] == "NONE"


# ── Status Updater Tests ──

def test_status_updater_no_old_labels():
    """V12.1 status updater must not use V11.6.1 OOS labels as future labels."""
    su = load("v12_1_live_paper_status_update.json")
    # Status updater reads v8_forward_return_labels, not V11.6.1
    assert su["status"] == "V12_1_LIVE_PAPER_STATUS_UPDATE_BUILT"
    # All completed runs must have forward_labels_available > 0
    for run in su.get("updated_runs", []):
        if run.get("run_status") == "COMPLETED":
            assert run.get("forward_labels_available", 0) > 0, \
                f"COMPLETED run {run['live_paper_run_id']} has no forward labels"


def test_status_updater_not_all_completed_without_labels():
    su = load("v12_1_live_paper_status_update.json")
    if su.get("all_live_paper_runs_completed", False):
        # If all completed, every run must have labels
        for run in su.get("updated_runs", []):
            if run.get("run_status") == "COMPLETED":
                assert run.get("forward_labels_available", 0) > 0
    # Fail-closed: if waiting runs exist, not all completed
    if su.get("waiting_run_count", 0) > 0:
        assert su.get("all_live_paper_runs_completed") is False


# ── Delta Report Tests ──

def test_delta_report_no_trading_advice():
    d = load("v12_1_live_paper_delta_report.json")
    assert d["research_only"] is True
    assert d["paper_only"] is True
    assert d["investment_action_count"] == 0
    assert d["trade_action_count"] == 0
    text = json.dumps(d).upper()
    for word in FORBIDDEN_WORDS:
        assert word not in text, f"Forbidden word {word} in delta report"


# ── Audit Tests ──

def test_audit_pass():
    a = load("v12_1_live_paper_loop_audit.json")
    assert a["status"] == "V12_1_LIVE_PAPER_LOOP_AUDIT_PASS"
    assert a["live_paper_loop_confirmed"] is True


def test_audit_no_rejected_reactivation():
    a = load("v12_1_live_paper_loop_audit.json")
    assert a["rejected_reactivation_violations"] == []


def test_audit_no_forbidden_actions():
    a = load("v12_1_live_paper_loop_audit.json")
    assert a["forbidden_action_violations"] == []
    assert a["blocking_reasons"] == []


# ── Closeout Tests ──

def test_closeout_safety_blocked():
    co = load("v12_1_live_paper_closeout.json")
    assert co["ready_for_alpha_claim"] is False
    assert co["alpha_validated"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


def test_closeout_rejected_not_reactivated():
    co = load("v12_1_live_paper_closeout.json")
    assert co["rejected_not_reactivated"] is True
    assert co["rejected_preserved_count"] == 4


# ── Full Chain Tests ──

def test_full_chain_pass():
    fc = load("v12_1_live_paper_full_chain.json")
    assert fc["status"] == "V12_1_LIVE_PAPER_FULL_CHAIN_PASS"
    assert fc["v12_research_only_base_confirmed"] is True
    assert fc["live_paper_loop_confirmed"] is True


def test_full_chain_safety():
    fc = load("v12_1_live_paper_full_chain.json")
    assert fc["ready_for_alpha_claim"] is False
    assert fc["alpha_validated"] is False
    assert fc["production"] == "BLOCKED"
    assert fc["broker_runtime"] == "BLOCKED"
    assert fc["real_trade"] == "BLOCKED"
    assert fc["forbidden_action_violations"] == []
    assert fc["rejected_reactivation_violations"] == []
