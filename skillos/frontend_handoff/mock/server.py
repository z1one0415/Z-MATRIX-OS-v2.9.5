"""
server.py — Flask mock server for A5 SkillOS Frontend Handoff RC.

Serves all fixture files at A1 API endpoints.
Constrained: PORT=8080, DEBUG=False, DISABLED_DEFAULT=True
"""

from flask import Flask
from mock_config import PORT, DEBUG
from routes import register_routes


def create_app():
    """Create and configure the Flask mock server application."""
    app = Flask(__name__)
    register_routes(app)
    return app


def main():
    app = create_app()
    print(f"[A5 Mock Server] Starting on port {PORT}")
    print(f"[A5 Mock Server] DEBUG={DEBUG}")
    print(f"[A5 Mock Server] DISABLED_DEFAULT=True (per SkillOS policy)")
    print(f"[A5 Mock Server] Endpoints: /api/v1/health, /api/v1/dashboard/summary, ...")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)


if __name__ == "__main__":
    main()
