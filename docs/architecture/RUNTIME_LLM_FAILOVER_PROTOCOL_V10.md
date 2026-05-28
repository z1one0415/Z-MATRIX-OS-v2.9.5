# RUNTIME LLM PROVIDER FAILOVER PROTOCOL V10

## Problem
System depends on LLM API calls. API downtime, rate limiting, network failure,
or content filter blocks can cause the IRF pipeline to hallucinate or crash.

## Core Rules
1. LLM/API failure: NO new factual judgment may be generated
2. Stale cached facts: may be read but MUST be marked stale
3. Stale facts: may only produce DATA_INSUFFICIENT or DEGRADED output
4. IRF pipeline: MUST degrade gracefully, never crash
5. Audit trail: failover_trace + cache_trace + stale_data_trace REQUIRED

## Components
- LLMProviderFailoverPolicy: routing + retry + circuit breaker
- OfflineDegradedMode: system operating mode when LLM unavailable
- CachedFactExtractionStore: repository of last audited extractions
- CriticalPipelineFallback: minimum viable pipeline without LLM
- StaleDataPolicy: TTL and freshness rules for cached facts
- DegradedCloseoutReport: final report documenting degradation

## Circuit Breaker States
- CLOSED: LLM available, normal operation
- OPEN: LLM failed N times in window, stop calling
- HALF_OPEN: testing recovery after cooldown
