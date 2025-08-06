import os
from flask import Flask
from flask_wtf import CSRFProtect

def create_app():
    """
    Erzeugt und konfiguriert die Flask-Anwendung.

    Rückgabe:
        Flask-App-Instanz mit registrierten Blueprints und Konfiguration.
    """
    app = Flask(__name__)

    # Geheimschlüssel für Sessions und CSRF-Token (zufällig bei jedem Start)
    app.secret_key = os.urandom(24) 

    # CSRF-Schutz aktivieren
    csrf = CSRFProtect(app)

    # Routen als Blueprint registrieren
    from .routes import main
    app.register_blueprint(main)

    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://upload.wikimedia.org; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    return app