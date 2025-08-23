from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)
    # If you need sessions/flash later, set a secret key:
    app.config.from_object("app.config.Config")
    app.register_blueprint(main_bp)
    return app
