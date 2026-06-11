"""Configuration for Z-SkillOS Frontend Handoff Backend (readonly shell)."""

import os

# Network
HOST = os.environ.get("ZSKILLOS_BACKEND_HOST", "0.0.0.0")
PORT = int(os.environ.get("ZSKILLOS_BACKEND_PORT", "5500"))

# Mode flags — this is a readonly shell, no writes, no mutations
DEBUG = False
DISABLED_DEFAULT = True   # all POST/PUT/PATCH/DELETE blocked
READONLY_MODE = True       # GET-only; service reads from fixtures

# Version
VERSION = "v0.1.0-rc"
