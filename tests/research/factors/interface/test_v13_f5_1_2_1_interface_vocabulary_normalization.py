"""V13.F5.1.2.1 — Interface vocabulary normalization tests."""
import json, glob
from pathlib import Path

FACTORS = ["F21","F22","F24","F26","F27","F30","F31","F34"]
CANONICAL_MODES = {"REGISTRY_READ","EVIDENCE_READ","VALIDATION_SUMMARY","GUARDRAIL_SUMMARY","CANDIDATE_MONITOR","RESEARCH_CONTEXT","SCORING_CONTEXT_DRY_PLAN","COMPOSITION_GRAPH_DRY_PLAN"}
LEGACY_MODES = {"RESEARCH_EVIDENCE_READ","VALIDATION_SUMMARY_READ","GUARDRAIL_SUMMARY_READ","MONITORING_READ"}
REQUIRED_BLOCKED_MODES = {"ALPHA_SIGNAL","PORTFOLIO_WEIGHT","ORDER_SIGNAL","PAPER_TRADING","BROKER_RUNTIME","REAL_TRADE","PRODUCTION"}
REQUIRED_BLOCKED_OUTPUTS = {"buy_signal","sell_signal","position_weight","expected_return_claim","alpha_claim"}
REQUIRED_BLOCKED_CONSUMERS = {"Z8_EXECUTION_RUNTIME","V3_TRADE_SANDBOX","BROKER","REAL_TRADE"}

def test_all_contracts_use_canonical_modes():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        modes = set(ac.get("allowed_application_modes", []))
        assert modes.issubset(CANONICAL_MODES), f"{fid}: non-canonical modes found: {modes - CANONICAL_MODES}"

def test_no_legacy_modes_in_contracts():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        modes = set(ac.get("allowed_application_modes", []))
        assert modes.isdisjoint(LEGACY_MODES), f"{fid}: legacy modes found: {modes & LEGACY_MODES}"

def test_legacy_aliases_documented():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        aliases = ac.get("legacy_mode_aliases", {})
        for legacy, canonical in [("RESEARCH_EVIDENCE_READ","EVIDENCE_READ"),("VALIDATION_SUMMARY_READ","VALIDATION_SUMMARY"),("GUARDRAIL_SUMMARY_READ","GUARDRAIL_SUMMARY"),("MONITORING_READ","CANDIDATE_MONITOR")]:
            assert aliases.get(legacy) == canonical, f"{fid}: missing or wrong alias for {legacy}"

def test_all_blocked_modes_present():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        modes = set(ac.get("blocked_application_modes", []))
        assert REQUIRED_BLOCKED_MODES.issubset(modes), f"{fid}: missing blocked modes: {REQUIRED_BLOCKED_MODES - modes}"

def test_all_blocked_outputs_present():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        outputs = set(ac.get("blocked_outputs", []))
        assert REQUIRED_BLOCKED_OUTPUTS.issubset(outputs), f"{fid}: missing blocked outputs: {REQUIRED_BLOCKED_OUTPUTS - outputs}"

def test_all_blocked_consumers_present():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        consumers = set(ac.get("blocked_downstream_consumers", []))
        assert REQUIRED_BLOCKED_CONSUMERS.issubset(consumers), f"{fid}: missing blocked consumers: {REQUIRED_BLOCKED_CONSUMERS - consumers}"

def test_alpha_false():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        assert ac.get("alpha_claim_allowed") is False

def test_prod_blocked():
    for fid in FACTORS:
        ac = json.loads((Path("research/factor_library/factors") / fid / "application_contract.json").read_text())
        assert ac.get("production") == "BLOCKED"
        assert ac.get("broker_runtime") == "BLOCKED"
        assert ac.get("real_trade") == "BLOCKED"

def test_schema_constrains_allowed_modes():
    """Verify the schema JSON has the enum constraint for allowed_application_modes."""
    schema = json.loads(open("research/factor_library/interface/v1/schemas/factor_application_contract.schema.json").read())
    items = schema["properties"]["allowed_application_modes"]["items"]
    assert "enum" in items
    schema_enum = set(items["enum"])
    assert schema_enum == CANONICAL_MODES, f"Schema enum mismatch: extra={schema_enum-CANONICAL_MODES} missing={CANONICAL_MODES-schema_enum}"

def test_invocation_request_enum_matches():
    """Verify invocation_request schema enum matches canonical readonly intents."""
    schema = json.loads(open("research/factor_library/interface/v1/schemas/factor_invocation_request.schema.json").read())
    schema_enum = set(schema["properties"]["invocation_intent"]["enum"])
    assert schema_enum == CANONICAL_MODES | {"SCORING_CONTEXT_DRY_PLAN","COMPOSITION_GRAPH_DRY_PLAN"} or schema_enum == CANONICAL_MODES, \
        f"invocation_request enum mismatch: {schema_enum}"

def test_execution_requested_false():
    """Verify invocation_request schema has execution_requested const false."""
    schema = json.loads(open("research/factor_library/interface/v1/schemas/factor_invocation_request.schema.json").read())
    assert schema["properties"]["execution_requested"]["const"] is False
