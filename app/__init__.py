"""Flask application factory for the Tickets Reseller web app."""

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "tickets-reseller-dev-key-change-me"

    from . import routes
    app.register_blueprint(routes.bp)

    return app
