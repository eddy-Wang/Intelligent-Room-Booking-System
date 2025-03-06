from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from .config import Config

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    CORS(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
