from flask import Flask
from .routes import payment_bp
def create_app_def():
    app = Flask(__name__)
    # Register Blueprint
    app.register_blueprint(payment_bp)
    return app
