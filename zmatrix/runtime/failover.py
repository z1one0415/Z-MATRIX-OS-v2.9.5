"""V4.0-B1 Runtime Failover — LLM Provider Failover Policy + Offline Degraded Mode"""
from __future__ import annotations

class LLMProviderStatus:
    def __init__(self, provider_id, status="UNKNOWN", error_message=None):
        self.provider_id = provider_id; self.status = status; self.checked_at = None; self.error_message = error_message

class CachedFactExtractionRecord:
    def __init__(self, cache_id, source_task_id, created_at, expires_at, fact_extraction_hash, audit_event_id):
        self.cache_id = cache_id; self.source_task_id = source_task_id; self.created_at = created_at; self.expires_at = expires_at; self.is_stale = True; self.fact_extraction_hash = fact_extraction_hash; self.audit_event_id = audit_event_id; self.allowed_usage = "READ_ONLY_REFERENCE"

class DegradedCloseoutReport:
    def __init__(self, pipeline_run_id, degraded_reason):
        self.pipeline_run_id = pipeline_run_id; self.degraded_reason = degraded_reason; self.failed_provider_status = []; self.stale_cache_used = False; self.new_judgement_generated = False; self.final_status = "DEGRADED"; self.real_trade_allowed = False; self.failover_trace = []; self.cache_trace = []; self.stale_data_trace = []

class LLMProviderFailoverPolicy:
    """Failover chain: primary → secondary → cache_read → offline → failed_closed"""
    def __init__(self):
        self.primary = None; self.secondary = None; self.cache_store = None; self.circuit_breaker = CircuitBreaker()
    def execute_with_failover(self, task_id, task_fn, cache_key=None):
        trace = []
        # Primary
        try: result = task_fn(self.primary); trace.append("primary_ok"); return result, self._build_report(task_id, "OK", trace, False)
        except Exception as e: trace.append(f"primary_failed:{e}")
        # Secondary
        if self.secondary:
            try: result = task_fn(self.secondary); trace.append("secondary_ok"); return result, self._build_report(task_id, "OK", trace, False)
            except Exception as e: trace.append(f"secondary_failed:{e}")
        # Cache
        if self.cache_store and cache_key:
            cached = self.cache_store.get(cache_key)
            if cached and not cached.is_stale:
                trace.append("cache_hit_fresh")
                return cached, self._build_report(task_id, "DEGRADED", trace, True)
            elif cached:
                trace.append("cache_hit_stale")
                return None, self._build_report(task_id, "DEGRADED", trace, True)
        # Failed closed
        trace.append("failed_closed")
        report = self._build_report(task_id, "FAILED_CLOSED", trace, False)
        report.new_judgement_generated = False
        return None, report
    def _build_report(self, pid, status, trace, stale):
        r = DegradedCloseoutReport(pid, f"failover: {status}"); r.failover_trace = trace; r.stale_cache_used = stale; r.stale_data_trace = trace; r.final_status = status
        return r

class CircuitBreaker:
    def __init__(self, failure_threshold=3, cooldown_seconds=60):
        self.state = "CLOSED"; self.failure_count = 0; self.threshold = failure_threshold; self.cooldown = cooldown_seconds; self.last_failure_time = None
    def call(self, fn):
        if self.state == "OPEN": return None
        try: result = fn(); self.failure_count = 0; return result
        except Exception:
            self.failure_count += 1
            if self.failure_count >= self.threshold: self.state = "OPEN"
            raise

class OfflineDegradedMode:
    def __init__(self): self.active = False; self.reason = None
    def activate(self, reason): self.active = True; self.reason = reason
    def is_active(self): return self.active
    def allowed_actions(self): return ["READ_ONLY_REFERENCE", "DATA_INSUFFICIENT", "DEGRADED_CLOSEOUT"]

class StaleDataPolicy:
    MAX_STALE_AGE_HOURS = 24
    @staticmethod
    def check(cached_record):
        if cached_record.is_stale: return {"usable": False, "action": "BLOCK", "reason": "STALE_CACHE"}
        return {"usable": True, "action": "READ_ONLY_REFERENCE"}
