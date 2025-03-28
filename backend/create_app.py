from flask import Flask
from routes import payment_bp
def create_app():
    app = Flask(__name__)
    # Register Blueprint
    app.register_blueprint(payment_bp)
    return app
