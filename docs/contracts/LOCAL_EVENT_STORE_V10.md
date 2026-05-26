# Local EventStore v1.0

## Storage

SQLite database at data/event_store/event_store.sqlite.

## Append Rules

1. append-only
2. Same event_id + same payload → idempotent (returns stored=True, idempotent=True)
3. Same event_id + different payload → conflict (returns stored=False, conflict=True, does NOT overwrite)
4. Must validate_event before write
5. No real Z9 write
6. No Hermes memory write

## Export/Import

JSONL format for local export/import.
No network. No Z9 write. No Hermes memory write.
