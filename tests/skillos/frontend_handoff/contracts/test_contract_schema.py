"""
A1 Contract Schema Validation Tests
====================================
Verify all JSON schemas parse, all routes unique, all endpoints unique,
all forbidden_actions non-empty, all mutation actions default disabled,
no buy/sell/order/position fields.

Run: python3 -m pytest tests/skillos/frontend_handoff/contracts/ -q
"""

import json
import os
import pytest
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
CONTRACTS_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent / "skillos" / "frontend_handoff" / "contracts"

CONTRACT_FILES = [
    "api_schema.json",
    "page_data_contract.json",
    "dashboard_contract.json",
    "error_abort_degraded_contract.json",
    "component_state_contract.json",
    "navigation_contract.json",
]

FORBIDDEN_FIELDS = [
    "buy", "sell", "order", "position",
    "broker_action", "runtime_enable", "production_enable",
    "paper_trading_start", "alpha_claim",
]

# ── Helpers ────────────────────────────────────────────────────────────
def load_contract(name: str) -> dict:
    """Load and parse a JSON contract file."""
    path = CONTRACTS_DIR / name
    assert path.exists(), f"Contract file not found: {path}"
    with open(path, "r") as f:
        return json.load(f)

def deep_search_fields(obj, path="", forbidden=None, skip_keys=None):
    """Recursively search for forbidden field names in any object."""
    if forbidden is None:
        forbidden = FORBIDDEN_FIELDS
    if skip_keys is None:
        skip_keys = {"global_forbidden_fields"}
    violations = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in forbidden and key not in skip_keys:
                violations.append(f"{path}.{key}" if path else key)
            violations.extend(deep_search_fields(value, f"{path}.{key}" if path else key, forbidden, skip_keys))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            violations.extend(deep_search_fields(item, f"{path}[{i}]", forbidden, skip_keys))
    return violations

def _deep_remove_key(obj, key_to_remove):
    """Recursively remove a key from all dicts in the object tree."""
    if isinstance(obj, dict):
        return {k: _deep_remove_key(v, key_to_remove) for k, v in obj.items() if k != key_to_remove}
    elif isinstance(obj, list):
        return [_deep_remove_key(item, key_to_remove) for item in obj]
    return obj

# ── Fixtures ───────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def contracts():
    """Load all contracts once per module."""
    return {name: load_contract(name) for name in CONTRACT_FILES}


# ── Test: All files exist and parse ────────────────────────────────────
class TestContractParsing:
    """Verify all JSON schemas parse successfully."""

    @pytest.mark.parametrize("name", CONTRACT_FILES)
    def test_file_exists(self, name):
        """Contract file must exist."""
        path = CONTRACTS_DIR / name
        assert path.exists(), f"Missing: {name}"

    @pytest.mark.parametrize("name", CONTRACT_FILES)
    def test_valid_json(self, name):
        """Contract must parse as valid JSON."""
        contract = load_contract(name)
        assert isinstance(contract, dict), f"{name} is not a JSON object"
        assert "$schema" in contract or "$id" in contract, f"{name} missing $schema or $id"

    @pytest.mark.parametrize("name", CONTRACT_FILES)
    def test_has_seal(self, name):
        """All contracts must carry A1_CONTRACT_FREEZE seal."""
        contract = load_contract(name)
        seal = contract.get("seal", "")
        assert seal == "A1_CONTRACT_FREEZE", f"{name} seal: expected A1_CONTRACT_FREEZE, got {seal}"


# ── Test: No forbidden fields ──────────────────────────────────────────
class TestForbiddenFields:
    """Verify no buy/sell/order/position/broker_action/etc. in any contract."""

    @pytest.mark.parametrize("name", CONTRACT_FILES)
    def test_no_forbidden_fields(self, name):
        """Contract must not contain any forbidden field names."""
        contract = load_contract(name)
        violations = deep_search_fields(contract)
        assert not violations, f"{name} contains forbidden fields: {violations}"

    @pytest.mark.parametrize("name", CONTRACT_FILES)
    def test_no_forbidden_values_in_strings(self, name):
        """Contract must not use forbidden terms as JSON object keys."""
        contract = load_contract(name)
        clean_contract = _deep_remove_key(contract, "global_forbidden_fields")
        raw = json.dumps(clean_contract).lower()
        import re
        for field in ["broker_action", "runtime_enable", "production_enable", "paper_trading_start", "alpha_claim"]:
            # Check that field does not appear as a JSON object key ("field": pattern)
            pattern = f'"{field}"\\s*:'
            match = re.search(pattern, raw)
            assert not match, f"{name} contains forbidden key: '{field}' (as JSON key)"


# ── Test: API schema endpoints ─────────────────────────────────────────
class TestApiSchema:
    """Verify api_schema.json structure and constraints."""

    def test_only_get_allowed(self, contracts):
        """Only GET method is allowed."""
        schema = contracts["api_schema.json"]
        allowed = schema.get("methods_allowed", [])
        assert allowed == ["GET"], f"methods_allowed: expected ['GET'], got {allowed}"

    def test_blocked_methods_present(self, contracts):
        """POST/PUT/PATCH/DELETE must be defined as blocked."""
        schema = contracts["api_schema.json"]
        blocked = schema.get("methods_blocked", {})
        expected_blocked = {"POST", "PUT", "PATCH", "DELETE"}
        actual_blocked = set(blocked.keys())
        assert actual_blocked == expected_blocked, f"Blocked methods mismatch: {actual_blocked}"

    def test_all_blocked_return_blocked_status(self, contracts):
        """All blocked methods must return BLOCKED status."""
        schema = contracts["api_schema.json"]
        for method, response in schema.get("methods_blocked", {}).items():
            assert response.get("status") == "BLOCKED", f"{method} blocked response: expected BLOCKED"
            assert "readonly_disabled_default" in response.get("reason", ""), f"{method} reason mismatch"

    def test_all_endpoints_are_get(self, contracts):
        """Every defined endpoint must use GET method."""
        schema = contracts["api_schema.json"]
        for path, defn in schema.get("endpoints", {}).items():
            method = defn.get("method", "").upper()
            assert method == "GET", f"{path}: expected GET, got {method}"

    def test_endpoints_unique(self, contracts):
        """All endpoint paths must be unique."""
        schema = contracts["api_schema.json"]
        paths = list(schema.get("endpoints", {}).keys())
        assert len(paths) == len(set(paths)), f"Duplicate endpoints: {paths}"

    def test_error_formats_defined(self, contracts):
        """Error format definitions must exist."""
        schema = contracts["api_schema.json"]
        errors = schema.get("error_formats", {})
        expected = {"standard_error", "blocked_error", "degraded_error"}
        actual = set(errors.keys())
        assert actual >= expected, f"Missing error formats: {expected - actual}"

    def test_readonly_in_response_headers(self, contracts):
        """X-ReadOnly header must be 'true'."""
        schema = contracts["api_schema.json"]
        headers = schema.get("global_response_headers", {})
        assert headers.get("X-ReadOnly") == "true"

    def test_research_report_disabled(self, contracts):
        """Research report generation must be disabled."""
        schema = contracts["api_schema.json"]
        rr = schema["endpoints"]["/api/research-report/summary"]["response"]["properties"]
        assert rr["generation_enabled"]["const"] is False

    def test_z9_review_disabled(self, contracts):
        """Z9 review must be disabled."""
        schema = contracts["api_schema.json"]
        z9 = schema["endpoints"]["/api/z9-review/summary"]["response"]["properties"]
        assert z9["review_enabled"]["const"] is False

    def test_capabilities_enabled_count_zero(self, contracts):
        """Capability enabled_count must be const: 0."""
        schema = contracts["api_schema.json"]
        caps = schema["endpoints"]["/api/capabilities"]["response"]["properties"]
        assert caps["enabled_count"]["const"] == 0

    def test_composition_graph_disabled_default(self, contracts):
        """Composition graph must have disabled_default: true."""
        schema = contracts["api_schema.json"]
        cg = schema["endpoints"]["/api/composition-graph/summary"]["response"]["properties"]
        assert cg["disabled_default"]["const"] is True


# ── Test: Page data contract ───────────────────────────────────────────
class TestPageDataContract:
    """Verify page_data_contract.json structure and constraints."""

    def test_11_pages_defined(self, contracts):
        """Exactly 11 pages must be defined."""
        pdc = contracts["page_data_contract.json"]
        pages = pdc.get("pages", [])
        assert len(pages) == 11, f"Expected 11 pages, got {len(pages)}"

    def test_all_routes_unique(self, contracts):
        """All page routes must be unique."""
        pdc = contracts["page_data_contract.json"]
        routes = [p["route"] for p in pdc["pages"]]
        assert len(routes) == len(set(routes)), f"Duplicate routes: {routes}"

    def test_all_page_ids_unique(self, contracts):
        """All page_ids must be unique."""
        pdc = contracts["page_data_contract.json"]
        ids = [p["page_id"] for p in pdc["pages"]]
        assert len(ids) == len(set(ids)), f"Duplicate page_ids: {ids}"

    def test_all_forbidden_actions_non_empty(self, contracts):
        """Every page must have at least one forbidden_action."""
        pdc = contracts["page_data_contract.json"]
        for page in pdc["pages"]:
            actions = page.get("forbidden_actions", [])
            assert len(actions) > 0, f"{page['page_id']}: forbidden_actions is empty"

    REQUIRED_STATES = ["loading", "empty", "error", "degraded", "blocked", "success"]

    @pytest.mark.parametrize("page_id,states", [
        (p["page_id"], list(p.get("states", {}).keys()))
        for p in json.loads((CONTRACTS_DIR / "page_data_contract.json").read_text()).get("pages", [])
    ])
    def test_all_states_present(self, page_id, states):
        """Every page must have all 6 required states."""
        missing = set(self.REQUIRED_STATES) - set(states)
        assert not missing, f"{page_id}: missing states: {missing}"

    def test_global_forbidden_fields(self, contracts):
        """Global forbidden fields list must be present and non-empty."""
        pdc = contracts["page_data_contract.json"]
        gff = pdc.get("global_forbidden_fields", [])
        assert len(gff) > 0, "global_forbidden_fields is empty"
        assert "buy" in gff
        assert "sell" in gff
        assert "order" in gff
        assert "position" in gff

    def test_all_mutation_actions_have_ui_blocked(self, contracts):
        """Pages' forbidden_actions should map to blocked UI states."""
        pdc = contracts["page_data_contract.json"]
        for page in pdc["pages"]:
            assert "blocked" in page.get("states", {}), f"{page['page_id']}: missing blocked state"
            blocked = page["states"]["blocked"]
            assert blocked.get("ui") == "blocked_overlay", f"{page['page_id']}: blocked state UI mismatch"

    def test_settings_page_safety_flags(self, contracts):
        """Settings page fixture must show all safety flags as false."""
        pdc = contracts["page_data_contract.json"]
        settings_page = next(p for p in pdc["pages"] if p["page_id"] == "settings")
        flags = settings_page["fixture_payload"]["safety_flags"]
        assert flags["runtime_enabled"] is False
        assert flags["production_enabled"] is False
        assert flags["paper_trading_allowed"] is False
        assert flags["broker_action_allowed"] is False
        assert flags["mutation_allowed"] is False


# ── Test: Dashboard contract ───────────────────────────────────────────
class TestDashboardContract:
    """Verify dashboard_contract.json structure."""

    def test_4_summary_cards(self, contracts):
        """Dashboard must have 4 summary cards."""
        dc = contracts["dashboard_contract.json"]
        cards = dc.get("summary_cards", {}).get("cards", [])
        assert len(cards) == 4, f"Expected 4 cards, got {len(cards)}"

    def test_8_component_statuses(self, contracts):
        """Dashboard must track 8 Z-SkillOS components."""
        dc = contracts["dashboard_contract.json"]
        ds = dc["dashboard_summary"]
        components = ds["properties"]["component_status"]["properties"]
        expected = {
            "factor_library", "composition_graph", "research_report",
            "z9_review", "evidence_chain", "run_state",
            "gate_state", "audit_trail"
        }
        actual = set(components.keys())
        assert actual == expected, f"Component mismatch: {actual}"

    def test_5_gate_statuses(self, contracts):
        """5 gate status indicators must be defined."""
        dc = contracts["dashboard_contract.json"]
        indicators = dc.get("gate_status_indicators", {}).get("indicators", {})
        assert len(indicators) == 5, f"Expected 5 indicators, got {len(indicators)}"

    def test_readonly_const_true(self, contracts):
        """Dashboard summary must have readonly: true const."""
        dc = contracts["dashboard_contract.json"]
        readonly = dc["dashboard_summary"]["properties"]["readonly"]
        assert readonly.get("const") is True


# ── Test: Error/Abort/Degraded contract ────────────────────────────────
class TestErrorAbortDegradedContract:
    """Verify error_abort_degraded_contract.json structure."""

    def test_error_categories_present(self, contracts):
        """Error categories must include client, server, and safety errors."""
        eadc = contracts["error_abort_degraded_contract.json"]
        cats = eadc["error_codes"]["categories"]
        assert "client_error" in cats
        assert "server_error" in cats
        assert "safety_error" in cats

    def test_all_error_codes_have_ui_treatment(self, contracts):
        """Every error code must specify ui_treatment."""
        eadc = contracts["error_abort_degraded_contract.json"]
        for cat_name, category in eadc["error_codes"]["categories"].items():
            for code_name, code_def in category.get("codes", {}).items():
                assert "ui_treatment" in code_def, f"{code_name}: missing ui_treatment"

    def test_7_abort_reasons(self, contracts):
        """7 abort reasons must be defined."""
        eadc = contracts["error_abort_degraded_contract.json"]
        reasons = eadc["abort_reasons"]["reasons"]
        assert len(reasons) == 7, f"Expected 7 abort reasons, got {len(reasons)}"

    def test_5_degraded_states(self, contracts):
        """5 degraded states must be defined."""
        eadc = contracts["error_abort_degraded_contract.json"]
        states = eadc["degraded_states"]["states"]
        assert len(states) == 5, f"Expected 5 degraded states, got {len(states)}"

    def test_blocked_actions_list_non_empty(self, contracts):
        """Blocked actions list must be substantial (30+ entries)."""
        eadc = contracts["error_abort_degraded_contract.json"]
        blocked = eadc["blocked_actions"]["permanently_blocked"]
        assert len(blocked) >= 30, f"Expected >=30 blocked actions, got {len(blocked)}"

    def test_all_abort_reasons_have_ui_treatment(self, contracts):
        """Every abort reason must have ui_treatment."""
        eadc = contracts["error_abort_degraded_contract.json"]
        for code, reason in eadc["abort_reasons"]["reasons"].items():
            assert "ui_treatment" in reason, f"{code}: missing ui_treatment"

    def test_all_degraded_states_have_ui_treatment(self, contracts):
        """Every degraded state must have ui_treatment."""
        eadc = contracts["error_abort_degraded_contract.json"]
        for code, state in eadc["degraded_states"]["states"].items():
            assert "ui_treatment" in state, f"{code}: missing ui_treatment"


# ── Test: Component state contract ─────────────────────────────────────
class TestComponentStateContract:
    """Verify component_state_contract.json structure."""

    REQUIRED_COMPONENTS = ["loading_spinner", "empty_state", "error_card", "degraded_badge", "blocked_overlay", "success_indicator"]

    def test_all_6_components_present(self, contracts):
        """All 6 UI components must be defined."""
        csc = contracts["component_state_contract.json"]
        components = csc.get("components", {})
        for rc in self.REQUIRED_COMPONENTS:
            assert rc in components, f"Missing component: {rc}"

    def test_state_machine_transitions(self, contracts):
        """State machine must define transitions for all 6 states."""
        csc = contracts["component_state_contract.json"]
        sm = csc.get("state_machine", {})
        assert sm.get("initial_state") == "loading"
        expected_states = {"loading", "empty", "error", "degraded", "blocked", "success"}
        assert set(sm.get("states", [])) == expected_states
        transitions = sm.get("transitions", [])
        assert len(transitions) >= 8, f"Expected >=8 transitions, got {len(transitions)}"

    def test_blocked_overlay_not_dismissible(self, contracts):
        """Blocked overlay must not be dismissible."""
        csc = contracts["component_state_contract.json"]
        bo = csc["components"]["blocked_overlay"]
        assert bo["behavior"]["dismissible"] is False
        assert bo["behavior"]["show_dismiss_button"] is False
        assert bo["behavior"]["block_page_interaction"] is True

    def test_loading_spinner_transitions_to_error(self, contracts):
        """Loading spinner must transition to error card on timeout."""
        csc = contracts["component_state_contract.json"]
        ls = csc["components"]["loading_spinner"]
        assert ls["behavior"]["on_timeout"] == "transition_to_error_card"

    def test_error_card_has_retry_button(self, contracts):
        """Error card must have retry enabled."""
        csc = contracts["component_state_contract.json"]
        ec = csc["components"]["error_card"]
        assert ec["behavior"]["retry"]["enabled"] is True


# ── Test: Navigation contract ──────────────────────────────────────────
class TestNavigationContract:
    """Verify navigation_contract.json structure."""

    def test_5_sidebar_sections(self, contracts):
        """5 sidebar sections must be defined."""
        nc = contracts["navigation_contract.json"]
        sections = nc["sidebar"]["sections"]
        assert len(sections) == 5, f"Expected 5 sections, got {len(sections)}"

    def test_11_nav_items(self, contracts):
        """11 navigation items (one per page) must be defined."""
        nc = contracts["navigation_contract.json"]
        items = []
        for section in nc["sidebar"]["sections"]:
            items.extend(section.get("items", []))
        assert len(items) == 11, f"Expected 11 nav items, got {len(items)}"

    def test_all_nav_routes_match_pages(self, contracts):
        """Navigation routes must match page_data_contract routes."""
        nc = contracts["navigation_contract.json"]
        pdc = contracts["page_data_contract.json"]

        nav_routes = set()
        for section in nc["sidebar"]["sections"]:
            for item in section.get("items", []):
                nav_routes.add(item["route"])

        page_routes = set(p["route"] for p in pdc.get("pages", []))
        assert nav_routes == page_routes, f"Route mismatch: nav={nav_routes}, pages={page_routes}"

    def test_breadcrumb_rules_present(self, contracts):
        """Breadcrumb rules must be defined."""
        nc = contracts["navigation_contract.json"]
        assert "breadcrumb_rules" in nc
        assert len(nc["breadcrumb_rules"]["examples"]) == 11

    def test_all_items_always_visible(self, contracts):
        """All nav items must be always_visible (permission gates interaction not visibility)."""
        nc = contracts["navigation_contract.json"]
        for section in nc["sidebar"]["sections"]:
            for item in section.get("items", []):
                assert item.get("always_visible") is True, f"{item['id']}: always_visible should be true"

    def test_footer_shows_readonly(self, contracts):
        """Sidebar footer must show read-only indicator."""
        nc = contracts["navigation_contract.json"]
        footer = nc["sidebar"]["footer"]
        assert footer["readonly_indicator"]["show"] is True
        assert "lock" in footer["readonly_indicator"].get("icon", "")
        assert footer["readonly_indicator"]["label"] == "Read-Only Mode"
        assert footer["contract_seal"]["label"] == "A1_CONTRACT_FREEZE"


# ── Test: Cross-contract integrity ─────────────────────────────────────
class TestCrossContractIntegrity:
    """Verify consistency across all contracts."""

    def test_page_ids_consistent(self, contracts):
        """page_data_contract and navigation_contract must reference same page_ids."""
        pdc = contracts["page_data_contract.json"]
        nc = contracts["navigation_contract.json"]

        pdc_ids = set(p["page_id"] for p in pdc["pages"])
        nav_ids = set()
        for section in nc["sidebar"]["sections"]:
            for item in section.get("items", []):
                nav_ids.add(item["page_id"])

        assert pdc_ids == nav_ids, f"Page ID mismatch: pdc={pdc_ids}, nav={nav_ids}"

    def test_api_endpoints_referenced_by_pages(self, contracts):
        """All API endpoints referenced by pages must exist in api_schema."""
        schema = contracts["api_schema.json"]
        pdc = contracts["page_data_contract.json"]

        schema_endpoints = set(schema["endpoints"].keys())
        for page in pdc["pages"]:
            for ep in page.get("api_endpoints", []):
                assert ep in schema_endpoints, f"{page['page_id']} references unknown endpoint: {ep}"

    def test_component_status_keys_consistent(self, contracts):
        """Dashboard component_status keys must match api_schema health components."""
        dc = contracts["dashboard_contract.json"]
        schema = contracts["api_schema.json"]

        dash_comps = set(dc["dashboard_summary"]["properties"]["component_status"]["properties"].keys())
        api_health_comps = set(schema["endpoints"]["/api/health"]["response"]["properties"]["components"]["properties"].keys())

        assert dash_comps == api_health_comps, f"Component mismatch: dashboard={dash_comps}, api={api_health_comps}"

    def test_all_contracts_have_matching_seals(self, contracts):
        """All contracts must carry the same A1_CONTRACT_FREEZE seal."""
        for name, contract in contracts.items():
            assert contract.get("seal") == "A1_CONTRACT_FREEZE", f"{name}: seal mismatch"
            assert contract.get("version") == "v0.1.0-rc", f"{name}: version mismatch"

    def test_no_forbidden_fields_in_constants(self, contracts):
        """Deep-check: no forbidden field names appear as JSON object keys."""
        import re
        for name, contract in contracts.items():
            clean_contract = _deep_remove_key(contract, "global_forbidden_fields")
            raw = json.dumps(clean_contract)
            for field in ["broker_action", "runtime_enable", "production_enable", "paper_trading_start", "alpha_claim"]:
                pattern = f'"{field}"\\s*:'
                match = re.search(pattern, raw)
                assert not match, f"{name}: contains forbidden key: '{field}' (as JSON key)"
            # buy/sell/order/position may appear as common English words in descriptions,
            # but never as JSON keys (already checked in TestForbiddenFields)
