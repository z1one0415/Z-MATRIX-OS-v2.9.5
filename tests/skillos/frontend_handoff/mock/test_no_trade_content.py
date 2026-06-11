"""
test_no_trade_content.py

Scan ALL fixture files for prohibited content:
- buy / sell / order / position (trading actions)
- alpha / alpha_claim (alpha claims)
- PNL / pnl / trade_result (PnL)
- broker / broker_action (broker content)

Any match in any fixture file = test FAILURE.
"""

import json
import os
import re
import pytest

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
FIXTURE_DIR = os.path.join(_PROJECT_ROOT, "skillos", "frontend_handoff", "fixtures")


def _get_all_fixture_files():
    return sorted([f for f in os.listdir(FIXTURE_DIR) if f.endswith(".json")])


def _read_fixture_text(name):
    path = os.path.join(FIXTURE_DIR, name)
    with open(path, "r") as f:
        return f.read()


# --- Prohibited patterns ---

# Pattern categories mapped to their regex patterns (case-insensitive)
PROHIBITED_PATTERNS = {
    # Trading actions: buy/sell/order/position
    "buy/sell": [
        r'\bBUY\b', r'\bbuy\b',
        r'\bSELL\b', r'\bsell\b',
        r'\bORDER\b', r'\border\b',
        r'\bPOSITION\b', r'\bposition\b',
    ],
    # Alpha claims
    "alpha": [
        r'\bALPHA_CLAIM\b', r'\balpha_claim\b',
        r'\bALPHA\b.*\bCLAIM\b', r'\balpha\b.*\bclaim\b',
    ],
    # Trade result
    "trade_result": [
        r'\bTRADE_RESULT\b', r'\btrade_result\b',
        r'\bTRADE\b.*\bRESULT\b', r'\btrade\b.*\bresult\b',
    ],
    # PnL
    "pnl": [
        r'\bPNL\b', r'\bpnl\b',
        r'\bREAL_PNL\b', r'\breal_pnl\b',
        r'\bP&L\b',
    ],
    # Broker actions
    "broker": [
        r'\bBROKER_ACTION\b', r'\bbroker_action\b',
        r'\bBROKER\b', r'\bbroker\b',
    ],
}


def _find_violations(text, fixture_name):
    """Find all prohibited pattern matches in text. Returns list of (category, pattern, match_context)."""
    violations = []
    for category, patterns in PROHIBITED_PATTERNS.items():
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end].replace('\n', ' ').strip()
                violations.append({
                    "category": category,
                    "pattern": pattern,
                    "match": match.group(),
                    "context": context,
                    "fixture": fixture_name,
                })
    return violations


class TestNoTradeContent:
    """Collect all violations across all fixtures and report them."""

    def test_no_prohibited_content_in_any_fixture(self):
        all_violations = []
        for fname in _get_all_fixture_files():
            text = _read_fixture_text(fname)
            violations = _find_violations(text, fname)
            all_violations.extend(violations)

        if all_violations:
            msg_parts = [f"\nFound {len(all_violations)} prohibited content violation(s):"]
            for v in all_violations:
                msg_parts.append(
                    f"  [{v['category']}] {v['fixture']}: "
                    f"matched '{v['match']}' (pattern: {v['pattern']}) "
                    f"near: ...{v['context']}..."
                )
            pytest.fail("\n".join(msg_parts))

    def test_fixtures_are_valid_json(self):
        """Ensure all fixtures are valid JSON before scanning."""
        for fname in _get_all_fixture_files():
            path = os.path.join(FIXTURE_DIR, fname)
            with open(path, "r") as f:
                json.load(f)


class TestNoTradeContentPerFixture:
    """Individual fixture-level tests for granular reporting."""

    @pytest.mark.parametrize("fname", _get_all_fixture_files())
    def test_fixture_has_no_prohibited_content(self, fname):
        text = _read_fixture_text(fname)
        violations = _find_violations(text, fname)
        assert len(violations) == 0, (
            f"{fname} has {len(violations)} violation(s): "
            f"{[v['match'] for v in violations]}"
        )


class TestKeywordsInValues:
    """Check that even JSON values don't contain sensitive keywords in their meaning."""

    @pytest.mark.parametrize("fname", _get_all_fixture_files())
    def test_no_broker_words_in_values(self, fname):
        """Ensure no broker/trade words in unexpected places."""
        text = _read_fixture_text(fname)
        # These are very aggressive checks — but that's the point
        aggressive_terms = [
            "brokerage", "broker", "execution_venue",
            "commission", "slippage_cost",
        ]
        text_lower = text.lower()
        for term in aggressive_terms:
            assert term not in text_lower, f"{fname} contains '{term}'"
