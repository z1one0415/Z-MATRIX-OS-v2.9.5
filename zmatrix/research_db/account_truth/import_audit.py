"""ResearchDB Account Truth — import audit logger."""
from __future__ import annotations


def audit_import(source_file: str, rows_imported: int, rows_skipped: int,
                 errors: list[dict] | None = None) -> dict:
    """Log an import audit event."""
    return {
        "source_file": source_file,
        "rows_imported": rows_imported,
        "rows_skipped": rows_skipped,
        "errors": errors or [],
        "status": "PASS" if rows_skipped == 0 else "PARTIAL",
        "production_allowed": False,
    }
