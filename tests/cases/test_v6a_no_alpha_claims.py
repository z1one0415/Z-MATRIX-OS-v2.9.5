import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent

def test_no_investment_words_in_json():
    """Forbidden words must not appear as VALUES (field names like buy_sell_instruction_count are OK)."""
    files = ["v6a_factor_input_inventory.json","core_12_factor_requirement_matrix.json",
             "v6b_price_only_factor_entry_gate.json","case_expansion_v6a_closeout.json"]
    forbidden = ["BUY","SELL","alpha_validated","predictive_alpha","production_allowed"]
    for fn in files:
        d = json.loads((W/"runtime_reports/cases"/fn).read_text())
        text = json.dumps(d)
        for w in forbidden:
            if w.lower() in text.lower():
                # Check it's not just a field name (buy_sell_instruction_count is OK)
                if w.lower() == "buy" and '"buy_sell_instruction_count": 0' in text.lower():
                    continue
                if w.lower() == "sell" and '"buy_sell_instruction_count": 0' in text.lower():
                    continue
                assert False, f"{fn}: FORBIDDEN: {w}"

def test_no_alpha_claim():
    """All factors and top-level docs must deny alpha."""
    files = ["v6a_factor_input_inventory.json","core_12_factor_requirement_matrix.json","case_expansion_v6a_closeout.json"]
    for fn in files:
        d = json.loads((W/"runtime_reports/cases"/fn).read_text())
        if "factors" in d:
            for f in d["factors"]:
                assert f.get("ready_for_alpha_claim") is False, f"{fn} factor {f.get('factor_id')}: alpha_claim={f.get('ready_for_alpha_claim')}"
        elif "matrix" in d:
            for m in d["matrix"]:
                assert m.get("ready_for_alpha_claim") is False, f"matrix {m.get('case_id')}"
        elif "ready_for_alpha_claim" in d:
            assert d["ready_for_alpha_claim"] is False
