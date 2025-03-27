from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from .config import Config

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'SK_test'
    app.config.update(
        SESSION_COOKIE_SECURE=False,  # Allows HTTP to transfer cookies
        SESSION_COOKIE_SAMESITE='Lax', # Allow cross-domain cookies (with Secure=False)
        SESSION_COOKIE_HTTPONLY=True
    )

    mail.init_app(app)
    CORS(app,
         origins=["http://localhost:5173","http://127.0.0.1:5173","http://192.168.110.139:5173"],
         supports_credentials=True)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
