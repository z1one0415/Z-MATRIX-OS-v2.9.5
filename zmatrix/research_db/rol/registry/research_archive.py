"""R1: Research Archive — immutable historical archive."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib, json

@dataclass
class ArchiveRecord:
    archive_id: str; entry_id: str; object_type: str; result: str = ""; evidence: list = field(default_factory=list)
    archived_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat()); content_hash: str = ""
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed=False

class ResearchArchive:
    def __init__(self): self._records: list[ArchiveRecord] = []
    def archive(self, archive_id: str, entry_id: str, object_type: str, result: str = "", evidence: list = None) -> ArchiveRecord:
        r = ArchiveRecord(archive_id=archive_id, entry_id=entry_id, object_type=object_type, result=result, evidence=evidence or [])
        r.content_hash = hashlib.sha256(json.dumps({"aid":archive_id,"eid":entry_id,"result":result},sort_keys=True).encode()).hexdigest()[:16]
        self._records.append(r); return r
    def get(self, archive_id: str) -> ArchiveRecord | None: return next((r for r in self._records if r.archive_id==archive_id), None)
    def by_entry(self, entry_id: str) -> list[ArchiveRecord]: return [r for r in self._records if r.entry_id==entry_id]
    def count(self) -> int: return len(self._records)
