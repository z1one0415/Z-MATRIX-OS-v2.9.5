from pathlib import Path
def _r(p): return Path(p).read_text(encoding="utf-8")

def test_truth_matrix_asset_aligned():
    for t in [_r("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md"), _r("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md"), _r("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")]:
        assert ("INTEGRATION_SMOKE_CANDIDATE" in t) or ("INTEGRATION_COMPLETE_CANDIDATE" in t), "missing integration status"
        assert "NOT_APPROVED" in t
        assert "BLOCKED" in t

def test_asset_index_not_not_done():
    a = _r("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    for aid, statuses in {"ZC20_DATAFORGE":["DEPTH_PARTIAL"],"ZC30_FACTOR_FACTORY":["DEPTH_PARTIAL"],"ZC40_EXECUTION_QUALITY":["DEPTH_PARTIAL"],"ZC50_ACCOUNT_GOVERNANCE":["DEPTH_PARTIAL"],"ZSC_AUDIT_EXPORT":["MINIMAL_CORE_DONE","INTEGRATION_DONE"],"IRF_01_03_04":["INTEGRATION_SMOKE_DONE"],"IRF_02_05_06_07_08":["NOT_DONE","INTEGRATION_DONE"]}.items():
        for l in a.splitlines():
            if aid in l:
                assert any(s in l for s in statuses), f"{aid}: expected one of {statuses}, got: {l[:60]}"
                break

def test_no_false_closeout():
    combined = _r("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md")+_r("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md")+_r("docs/upgrade/V40_CONTENT_ASSET_INDEX.md")
    for f in ["RC1_APPROVED","PRODUCTION_READY","BROKER_READY","RUNTIME_READY"]:
        for line in combined.splitlines():
            s = line.strip()
            if f in s:
                # Allow in explicitly forbidden (❌) contexts
                if s.startswith("❌") or s.startswith("- ❌") or s.startswith("| ❌"):
                    continue
                # Allow if line ends with ❌ (declaring forbidden)
                if s.endswith("❌") or ": ❌" in s:
                    continue
                # Allow in "not yet"/"NOT yet" contexts
                if "NOT yet" in s or "not yet" in s:
                    continue
                assert False, f"Forbidden token in non-forbidden context: {f} → {s[:60]}"
    # Check no fake ACCEPTANCE_DONE
    for l in _r("docs/upgrade/V40_HARDENING_C_ACCEPTANCE_MATRIX.md").splitlines():
        if l.startswith("| HC-") and "| ACCEPTANCE_DONE |" in l:
            assert False, f"False ACCEPTANCE_DONE: {l}"
