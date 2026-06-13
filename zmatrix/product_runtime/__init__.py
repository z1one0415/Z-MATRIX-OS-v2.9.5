"""Product runtime helpers for the local Z-MATRIX workstation."""

from .local_backend import (
    READINESS_BLOCKED,
    READINESS_PASS,
    ProductRuntimeConfig,
    build_cockpit_manifest,
    build_research_evidence_index,
    build_runtime_product_readiness,
    build_product_status,
    serve_product_runtime,
)

build_product_readiness = build_runtime_product_readiness

__all__ = [
    "READINESS_BLOCKED",
    "READINESS_PASS",
    "ProductRuntimeConfig",
    "build_cockpit_manifest",
    "build_research_evidence_index",
    "build_product_readiness",
    "build_runtime_product_readiness",
    "build_product_status",
    "serve_product_runtime",
]
