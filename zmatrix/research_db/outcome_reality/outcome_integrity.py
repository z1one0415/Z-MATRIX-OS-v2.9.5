"""IntegrityChecker — coverage, consistency, duplicates, hash verification."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class IntegrityStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAILED = "FAILED"

    @classmethod
    def worst(cls, statuses: list[IntegrityStatus]) -> IntegrityStatus:
        if cls.FAILED in statuses:
            return cls.FAILED
        if cls.WARNING in statuses:
            return cls.WARNING
        return cls.PASS


@dataclass
class IntegrityResult:
    coverage_status: IntegrityStatus = IntegrityStatus.PASS
    consistency_status: IntegrityStatus = IntegrityStatus.PASS
    duplicates_status: IntegrityStatus = IntegrityStatus.PASS
    hash_status: IntegrityStatus = IntegrityStatus.PASS
    coverage_detail: str = ""
    consistency_detail: str = ""
    duplicates_detail: str = ""
    hash_detail: str = ""
    overall_status: IntegrityStatus = IntegrityStatus.PASS
    issues: list[str] = field(default_factory=list)
    production_allowed: bool = field(default=False, repr=False)

    def __post_init__(self):
        self.production_allowed = False
        all_statuses = [
            self.coverage_status,
            self.consistency_status,
            self.duplicates_status,
            self.hash_status,
        ]
        self.overall_status = IntegrityStatus.worst(all_statuses)

    def has_issues(self) -> bool:
        return self.overall_status in (IntegrityStatus.WARNING, IntegrityStatus.FAILED)


class IntegrityChecker:
    @staticmethod
    def check_coverage(snapshot) -> IntegrityResult:
        from .outcome_snapshot import OutcomeSnapshot
        result = IntegrityResult()
        years_covered = len(snapshot.event_coverage) if snapshot.event_coverage else 0
        if snapshot.total_events == 0:
            result.coverage_status = IntegrityStatus.FAILED
            result.coverage_detail = "Zero events in snapshot"
            result.issues.append(result.coverage_detail)
        elif years_covered < 5:
            result.coverage_status = IntegrityStatus.WARNING
            result.coverage_detail = f"Only {years_covered} years covered (expected >=5)"
            result.issues.append(result.coverage_detail)
        else:
            result.coverage_status = IntegrityStatus.PASS
            result.coverage_detail = f"{years_covered} years covered, {snapshot.total_events} events"
        all_statuses = [
            result.coverage_status, result.consistency_status,
            result.duplicates_status, result.hash_status,
        ]
        result.overall_status = IntegrityStatus.worst(all_statuses)
        return result

    @staticmethod
    def check_consistency(events: list) -> IntegrityResult:
        from .outcome_universe import OutcomeEvent
        result = IntegrityResult()
        issues = []
        ids_seen = set()
        for e in events:
            if not e.event_id:
                issues.append(f"Event missing event_id: {e.name}")
                continue
            if not e.start_date or not e.end_date:
                issues.append(f"Event {e.event_id} missing date range")
                continue
            if e.start_date > e.end_date:
                issues.append(f"Event {e.event_id}: start_date {e.start_date} > end_date {e.end_date}")
            if e.year < 2005 or e.year > 2026:
                issues.append(f"Event {e.event_id}: year {e.year} outside 2005-2026 range")
        if issues:
            result.consistency_status = IntegrityStatus.FAILED
            result.consistency_detail = f"{len(issues)} consistency issues"
            result.issues.extend(issues)
        else:
            result.consistency_detail = "All events consistent"
        all_statuses = [
            result.coverage_status, result.consistency_status,
            result.duplicates_status, result.hash_status,
        ]
        result.overall_status = IntegrityStatus.worst(all_statuses)
        return result

    @staticmethod
    def check_duplicates(events: list) -> IntegrityResult:
        from .outcome_universe import OutcomeEvent
        result = IntegrityResult()
        seen_ids: dict[str, int] = {}
        seen_names: dict[str, int] = {}
        issues = []
        for e in events:
            seen_ids[e.event_id] = seen_ids.get(e.event_id, 0) + 1
            seen_names[e.name.lower()] = seen_names.get(e.name.lower(), 0) + 1
        dupe_ids = {k: v for k, v in seen_ids.items() if v > 1}
        dupe_names = {k: v for k, v in seen_names.items() if v > 1}
        if dupe_ids:
            issues.append(f"Duplicate event_ids: {list(dupe_ids.keys())}")
        if dupe_names:
            issues.append(f"Duplicate event names: {list(dupe_names.keys())}")
        if issues:
            result.duplicates_status = IntegrityStatus.FAILED
            result.duplicates_detail = f"{len(issues)} duplicate issues"
            result.issues.extend(issues)
        else:
            result.duplicates_detail = "No duplicates found"
        all_statuses = [
            result.coverage_status, result.consistency_status,
            result.duplicates_status, result.hash_status,
        ]
        result.overall_status = IntegrityStatus.worst(all_statuses)
        return result

    @staticmethod
    def verify_hash(snapshot, expected_hash: str | None = None) -> IntegrityResult:
        import hashlib, json
        result = IntegrityResult()
        try:
            data = snapshot.to_dict()
            raw = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
            computed = hashlib.sha256(raw).hexdigest()
            if expected_hash is None:
                result.hash_detail = f"Computed hash: {computed[:16]}... (no expected hash)"
                result.hash_status = IntegrityStatus.PASS
            elif computed == expected_hash:
                result.hash_detail = "Hash matches expected"
            else:
                result.hash_status = IntegrityStatus.FAILED
                result.hash_detail = f"Hash mismatch: computed {computed[:16]}... != expected {expected_hash[:16]}..."
                result.issues.append(result.hash_detail)
        except Exception as e:
            result.hash_status = IntegrityStatus.FAILED
            result.hash_detail = f"Hash computation failed: {e}"
            result.issues.append(result.hash_detail)
        all_statuses = [
            result.coverage_status, result.consistency_status,
            result.duplicates_status, result.hash_status,
        ]
        result.overall_status = IntegrityStatus.worst(all_statuses)
        return result

    @staticmethod
    def full_check(snapshot, events: list, expected_hash: str | None = None) -> IntegrityResult:
        coverage = IntegrityChecker.check_coverage(snapshot)
        consistency = IntegrityChecker.check_consistency(events)
        duplicates = IntegrityChecker.check_duplicates(events)
        hash_result = IntegrityChecker.verify_hash(snapshot, expected_hash)
        all_issues = (
            coverage.issues + consistency.issues + duplicates.issues + hash_result.issues
        )
        overall = IntegrityStatus.worst([
            coverage.overall_status, consistency.overall_status,
            duplicates.overall_status, hash_result.overall_status,
        ])
        return IntegrityResult(
            coverage_status=coverage.coverage_status,
            consistency_status=consistency.consistency_status,
            duplicates_status=duplicates.duplicates_status,
            hash_status=hash_result.hash_status,
            coverage_detail=coverage.coverage_detail,
            consistency_detail=consistency.consistency_detail,
            duplicates_detail=duplicates.duplicates_detail,
            hash_detail=hash_result.hash_detail,
            overall_status=overall,
            issues=all_issues,
        )
