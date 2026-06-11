"""Flask application — CORS enabled, readonly shell, disabled-default mode."""

from flask import Flask
from flask_cors import CORS

from . import config
from .routes import api


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = config.DEBUG

    # CORS — allow all origins for development / readonly shell
    CORS(app)

    # Register the API blueprint
    app.register_blueprint(api)

    return app


# Module-level app instance for WSGI / test clients
app = create_app()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT)
