"""Z-SkillOS Frontend Handoff — Version Registry Module.

Provides canonical version and base commit for the release.
Imported by tests and runtime to verify alignment.
"""

VERSION = "v0.1.0-rc"
BASE_COMMIT = "1f20dc1b"
RELEASE_DATE = "2026-06-12"
RELEASE_BRANCH = "integration/z-skillos-frontend-handoff-rc"

__all__ = ["VERSION", "BASE_COMMIT", "RELEASE_DATE", "RELEASE_BRANCH"]
