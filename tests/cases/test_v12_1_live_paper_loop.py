"""V12.1: Live Paper Loop Tests — 21 test cases including label-key validation."""
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


# ── Registry Tests ──

def test_registry_only_activates_pending():
    r = load("v12_1_live_paper_run_registry.json")
    assert r["active_live_paper_run_count"] == 8
    assert r["rejected_preserved_count"] == 4


def test_registry_does_not_activate_rejected():
    r = load("v12_1_live_paper_run_registry.json")
    rejected = [run for run in r["runs"] if run["run_status"] == "PRESERVED_REJECTED"]
    assert len(rejected) == 4


# ── Due Schedule Tests (V12.1.1 fixed) ──

def test_due_schedule_has_required_label_key():
    """Each schedule item must have required_label_key with as_of_date and horizon."""
    s = load("v12_1_live_paper_due_schedule.json")
    for item in s.get("schedule_items", []):
        rlk = item.get("required_label_key", {})
        assert rlk, f"Missing required_label_key in {item.get('live_paper_run_id')}"
        assert rlk.get("as_of_date", ""), f"Missing as_of_date in required_label_key"
        assert rlk.get("horizon", ""), f"Missing horizon in required_label_key"


def test_due_schedule_does_not_reuse_source_date():
    """required_label_key.as_of_date must NOT equal source_start_as_of_date (20240905)."""
    s = load("v12_1_live_paper_due_schedule.json")
    for item in s.get("schedule_items", []):
        rlk = item.get("required_label_key", {})
        ssa = item.get("source_start_as_of_date", "")
        if rlk.get("as_of_date") and ssa:
            assert rlk["as_of_date"] != ssa, (
                f"Label key reuses source date {ssa} for {item.get('live_paper_run_id')}"
            )


def test_due_schedule_only_active_runs():
    s = load("v12_1_live_paper_due_schedule.json")
    r = load("v12_1_live_paper_run_registry.json")
    assert s["scheduled_run_count"] == r["active_live_paper_run_count"]


def test_due_schedule_no_trading():
    s = load("v12_1_live_paper_due_schedule.json")
    for item in s.get("schedule_items", []):
        assert item["investment_action"] == "NONE"
        assert item["trade_action"] == "NONE"


# ── Status Updater Tests (V12.1.1 fixed) ──

def test_status_updater_no_fixed_base_date():
    """Status updater source must NOT contain hardcoded base_date = '20240905'."""
    src = (W / "scripts/cases/update_v12_1_live_paper_status.py").read_text()
    assert 'base_date = "20240905"' not in src, "Status updater still uses fixed base_date"


def test_completed_runs_have_validated_label_key():
    """Every COMPLETED run must have label_key_validated=true and label_source set."""
    su = load("v12_1_live_paper_status_update.json")
    for run in su.get("updated_runs", []):
        if run.get("run_status") == "COMPLETED":
            assert run.get("label_key_validated") is True, (
                f"COMPLETED run {run.get('live_paper_run_id')} missing label_key_validated"
            )
            assert run.get("label_source") == "v8_forward_return_labels.json", (
                f"COMPLETED run {run.get('live_paper_run_id')} missing correct label_source"
            )
            # required_label_key must not use 20240905
            rlk = run.get("required_label_key", {})
            assert rlk.get("as_of_date") != "20240905", (
                f"COMPLETED run uses source date as label key"
            )


def test_status_updater_reused_date_tracked():
    """reused_source_date_count must be 0."""
    su = load("v12_1_live_paper_status_update.json")
    assert su.get("reused_source_date_count", -1) == 0, (
        f"Status updater reports {su.get('reused_source_date_count')} reused source dates"
    )


def test_status_updater_not_all_completed_without_labels():
    """Fail-closed: if waiting runs exist, all_completed must be false."""
    su = load("v12_1_live_paper_status_update.json")
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


# ── Audit Tests (V12.1.1 hardened) ──

def test_audit_pass_with_label_keys():
    a = load("v12_1_live_paper_loop_audit.json")
    assert a["status"] == "V12_1_LIVE_PAPER_LOOP_AUDIT_PASS", (
        f"Audit blocked: {a.get('blocking_reasons', [])}"
    )
    assert a["live_paper_loop_confirmed"] is True


def test_audit_no_rejected_reactivation():
    a = load("v12_1_live_paper_loop_audit.json")
    assert a["rejected_reactivation_violations"] == []


def test_audit_no_forbidden_actions():
    a = load("v12_1_live_paper_loop_audit.json")
    assert a["forbidden_action_violations"] == []
    assert a["blocking_reasons"] == []


def test_audit_blocks_reused_source_date():
    """Audit must not contain LIVE_PAPER_LABEL_KEY_REUSES_SOURCE_DATE violations."""
    a = load("v12_1_live_paper_loop_audit.json")
    reasons = " ".join(a.get("blocking_reasons", []))
    assert "LABEL_KEY_REUSES" not in reasons, f"Audit has reused label key violations"
    assert "USES_SOURCE_DATE_AS_LABEL_KEY" not in reasons


# ── Closeout Tests ──

def test_closeout_safety_blocked():
    co = load("v12_1_live_paper_closeout.json")
    assert co["ready_for_alpha_claim"] is False
    assert co["alpha_validated"] is False
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


def test_closeout_label_key_clean():
    """label_key_reused_source_date_count must be 0, label_key_clean=true."""
    co = load("v12_1_live_paper_closeout.json")
    assert co.get("label_key_reused_source_date_count", -1) == 0
    assert co.get("label_key_clean") is True


def test_closeout_next_action_consistent():
    """If completion is WAITING_FOR_LABELS, next must be WAIT_FOR_LIVE_PAPER_DUE_LABELS."""
    co = load("v12_1_live_paper_closeout.json")
    completion = co.get("live_paper_completion_status", "")
    next_action = co.get("next_required_action", "")
    if completion == "WAITING_FOR_LABELS":
        assert next_action == "WAIT_FOR_LIVE_PAPER_DUE_LABELS", (
            f"Expected WAIT_FOR_LIVE_PAPER_DUE_LABELS, got {next_action}"
        )
    elif completion == "COMPLETED":
        assert next_action == "V12_2_RESEARCH_ONLY_Z9_FEEDBACK_LOOP", (
            f"Expected V12_2, got {next_action}"
        )


# ── Full Chain Tests ──

def test_full_chain_pass():
    fc = load("v12_1_live_paper_full_chain.json")
    assert fc["status"] == "V12_1_LIVE_PAPER_FULL_CHAIN_PASS"
    assert fc["v12_research_only_base_confirmed"] is True


def test_full_chain_safety():
    fc = load("v12_1_live_paper_full_chain.json")
    assert fc["ready_for_alpha_claim"] is False
    assert fc["alpha_validated"] is False
    assert fc["production"] == "BLOCKED"
    assert fc["broker_runtime"] == "BLOCKED"
    assert fc["real_trade"] == "BLOCKED"
    assert fc["forbidden_action_violations"] == []
    assert fc["rejected_reactivation_violations"] == []
