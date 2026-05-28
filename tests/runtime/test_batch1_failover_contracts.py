"""Batch 1 tests — failover + contracts"""
from zmatrix.runtime.failover import LLMProviderFailoverPolicy, CircuitBreaker, OfflineDegradedMode, StaleDataPolicy
from zmatrix.contracts.batch1_contracts import SubjectiveScoreBanValidator, FactExtractionContract, FailoverContract

def test_circuit_breaker_opens():
    cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=60)
    for _ in range(2):
        try: cb.call(lambda: (_ for _ in ()).throw(Exception("fail")))
        except Exception: pass
    assert cb.state == "OPEN"

def test_circuit_breaker_resets():
    cb = CircuitBreaker(failure_threshold=5, cooldown_seconds=60)
    result = cb.call(lambda: 42)
    assert result == 42; assert cb.state == "CLOSED"

def test_failover_primary_ok():
    fp = LLMProviderFailoverPolicy()
    result, report = fp.execute_with_failover("t1", lambda p: "ok")
    assert result == "ok"; assert report.final_status == "OK"

def test_failover_failed_closed():
    fp = LLMProviderFailoverPolicy()
    result, report = fp.execute_with_failover("t2", lambda p: (_ for _ in ()).throw(Exception("fail")))
    assert result is None; assert report.final_status == "FAILED_CLOSED"
    assert report.new_judgement_generated == False

def test_offline_degraded_mode():
    od = OfflineDegradedMode()
    od.activate("LLM API timeout")
    assert od.is_active(); assert "DATA_INSUFFICIENT" in od.allowed_actions()

def test_subjective_score_ban_blocks():
    v = SubjectiveScoreBanValidator()
    r = v.validate_llm_output({"moat_score": 0.85})
    assert r["passed"] == False; assert len(r["violations"]) > 0

def test_subjective_score_ban_allows_facts():
    v = SubjectiveScoreBanValidator()
    r = v.validate_llm_output({"revenue": 1.5e9, "event_type": "EARNINGS"})
    assert r["passed"] == True

def test_fact_extraction_contract():
    c = FactExtractionContract()
    r = c.validate({"source": "tushare", "publish_time": "2026-05-29", "evidence_level": "B", "extraction_type": "FACTUAL_NUMBER"})
    assert r["valid"] == True

def test_failover_contract_blocks_new_judgment():
    from zmatrix.runtime.failover import DegradedCloseoutReport
    rpt = DegradedCloseoutReport("p1", "test")
    rpt.new_judgement_generated = True
    fc = FailoverContract()
    result = fc.validate_degraded_report(rpt)
    assert result["valid"] == False

def test_failover_contract_passes_valid_report():
    from zmatrix.runtime.failover import DegradedCloseoutReport
    rpt = DegradedCloseoutReport("p2", "test")
    rpt.failover_trace = ["primary_failed", "failed_closed"]
    fc = FailoverContract()
    result = fc.validate_degraded_report(rpt)
    assert result["valid"] == True; assert result["llm_api_failure_no_new_judgement"] == True
