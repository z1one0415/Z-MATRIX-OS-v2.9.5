# TAG_RECORD v2.9.6-RC1

## Tag

| 字段 | 值 |
|------|------|
| Tag name | v2.9.6-RC1 |
| Target commit | `9364df7467053350010e7afdbbbc9fbb316b6dc8` |
| Branch | master |
| Tag status | CREATED |
| Tag date | 2026-05-25 |

## Release package

```
release/v2.9.6-RC1/
├── ARTIFACT_CHECKSUMS.txt
├── CONTRACT_INDEX_v2.9.6.md
├── OPERATOR_RUNBOOK_v2.9.6-RC1.md
├── RC_KNOWN_LIMITATIONS_v2.9.6.md
├── RC_MANIFEST_v2.9.6.md
├── RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md
├── README.md
├── RELEASE_NOTES_v2.9.6-RC1.md
├── TAG_RECORD_v2.9.6-RC1.md
└── VERIFY_COMMANDS.md
```

## Required verification

```bash
python3 -m compileall pipelines tests zmatrix hermes scripts
python3 tests/test_rc_packaging.py
python3 tests/test_rc_verification_gate.py
./scripts/verify_rc_candidate.sh
git diff --check
git status --short
```

## Safety boundaries

- no real trade
- no broker order
- no real Z9 write
- no queue write
- no real market fetch
- no auto calibration

## Known limitations

`docs/release/RC_KNOWN_LIMITATIONS_v2.9.6.md`
