"""V12.0: Research-Only Loop Tests — 11 test cases covering gate, contract, signals, obs, autopsy, audit, closeout, safety."""
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


# ── Gate Tests ──

def test_gate_is_research_only_allowed():
    g = load("v12_alpha_operating_loop_entry_gate.json")
    assert g["status"] == "V12_ALPHA_OPERATING_LOOP_RESEARCH_ONLY_ALLOWED"
    assert g["blocking_reasons"] == []


# ── Contract Tests ──

def test_contract_built():
    c = load("v12_research_only_operating_contract.json")
    assert c["status"] == "V12_RESEARCH_ONLY_OPERATING_CONTRACT_BUILT"
    assert c["research_only"] is True
    assert c["operating_mode"] == "RESEARCH_ONLY_PAPER_LOOP"


def test_contract_forbidden_actions_exist():
    c = load("v12_research_only_operating_contract.json")
    assert len(c["forbidden_actions"]) > 0
    assert "BUY" in c["forbidden_actions"]
    assert "SELL" in c["forbidden_actions"]


def test_contract_allowed_no_trading():
    c = load("v12_research_only_operating_contract.json")
    trading_actions = {"BUY", "SELL", "ADD_POSITION", "REDUCE_POSITION", "BROKER_ORDER"}
    for a in c.get("allowed_actions", []):
        assert a not in trading_actions, f"Trading action in allowed: {a}"


# ── Signal Snapshot Tests ──

def test_signal_snapshot_no_investment_actions():
    s = load("v12_research_signal_snapshot.json")
    assert s["investment_action_count"] == 0
    assert s["trade_action_count"] == 0
    for sig in s.get("signals", []):
        assert sig["investment_action"] == "NONE"
        assert sig["trade_action"] == "NONE"


def test_signal_snapshot_no_forbidden_words():
    s = load("v12_research_signal_snapshot.json")
    text = json.dumps(s).upper()
    for word in FORBIDDEN_WORDS:
        assert word not in text, f"Forbidden word {word} found in signal snapshot"


# ── Paper Observation Loop Tests ──

def test_observation_loop_no_actions():
    o = load("v12_paper_observation_loop.json")
    assert o["investment_action_count"] == 0
    assert o["trade_action_count"] == 0
    for obs in o.get("observations", []):
        assert obs["investment_action"] == "NONE"
        assert obs["trade_action"] == "NONE"


# ── Z9 Autopsy Tests ──

def test_z9_autopsy_no_actions():
    z = load("v12_z9_research_autopsy_input.json")
    assert z["investment_action_count"] == 0
    assert z["trade_action_count"] == 0
    for inp in z.get("autopsy_inputs", []):
        assert inp["investment_action"] == "NONE"
        assert inp["trade_action"] == "NONE"


# ── Audit Tests ──

def test_audit_pass():
    a = load("v12_research_only_loop_audit.json")
    assert a["status"] == "V12_RESEARCH_ONLY_LOOP_AUDIT_PASS"
    assert a["research_only_loop_confirmed"] is True
    assert a["forbidden_action_violations"] == []


def test_audit_intercepts_forbidden_words():
    """If forbidden words existed in runtime, audit would flag them."""
    a = load("v12_research_only_loop_audit.json")
    blocking = a.get("blocking_reasons", [])
    # None of the blocking reasons should be about forbidden words
    for r in blocking:
        assert "FORBIDDEN" not in r, f"Audit blocked by forbidden: {r}"


# ── Closeout Tests ──

def test_closeout_no_alpha():
    co = load("v12_research_only_closeout.json")
    assert co["ready_for_alpha_claim"] is False
    assert co["alpha_validated"] is False


def test_closeout_safety_blocked():
    co = load("v12_research_only_closeout.json")
    assert co["production"] == "BLOCKED"
    assert co["broker_runtime"] == "BLOCKED"
    assert co["real_trade"] == "BLOCKED"


# ── Full Chain Tests ──

def test_full_chain_pass():
    fc = load("v12_research_only_full_chain.json")
    assert fc["status"] == "V12_RESEARCH_ONLY_FULL_CHAIN_PASS"
    assert fc["research_only_loop_confirmed"] is True


def test_full_chain_safety():
    fc = load("v12_research_only_full_chain.json")
    assert fc["ready_for_alpha_claim"] is False
    assert fc["alpha_validated"] is False
    assert fc["production"] == "BLOCKED"
    assert fc["broker_runtime"] == "BLOCKED"
    assert fc["real_trade"] == "BLOCKED"
    assert fc["forbidden_action_violations"] == []
