from pathlib import Path
def _r(p): return Path(p).read_text(encoding="utf-8")

def test_truth_matrix_asset_aligned():
    for t in [_r("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md"), _r("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md"), _r("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")]:
        assert "INTEGRATION_SMOKE_CANDIDATE" in t; assert "NOT_APPROVED" in t; assert "BLOCKED" in t

def test_asset_index_not_not_done():
    a = _r("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    for aid, status in {"ZC20_DATAFORGE":"DEPTH_PARTIAL","ZC30_FACTOR_FACTORY":"DEPTH_PARTIAL","ZC40_EXECUTION_QUALITY":"DEPTH_PARTIAL","ZC50_ACCOUNT_GOVERNANCE":"DEPTH_PARTIAL","ZSC_AUDIT_EXPORT":"MINIMAL_CORE_DONE","IRF_01_03_04":"INTEGRATION_SMOKE_DONE","IRF_02_05_06_07_08":"NOT_DONE"}.items():
        for l in a.splitlines():
            if aid in l: assert status in l, f"{aid}: expected {status}"; break

def test_no_false_closeout():
    combined = _r("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md")+_r("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md")+_r("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    for f in ["RC1_APPROVED","PRODUCTION_READY","BROKER_READY","RUNTIME_READY","| INTEGRATED |"]:
        assert f not in combined, f"Forbidden: {f}"
    for l in _r("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md").splitlines():
        if l.startswith("| HC-") and "| ACCEPTANCE_DONE |" in l: assert False, f"False ACCEPTANCE_DONE: {l}"
