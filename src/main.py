# -*- coding: utf-8 -*-
"""
App entrypoint (Flask) - Session 4 split structure
Creates the Flask app and registers blueprints.
"""
from flask import Flask
from src.api.routes import api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
