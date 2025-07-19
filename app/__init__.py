import os
from flask import Flask

def create_app():
    """
    Erzeugt und konfiguriert die Flask-Anwendung.

    Rückgabe:
        Flask-App-Instanz mit registrierten Blueprints und Konfiguration.
    """
    app = Flask(__name__)

    # Geheimschlüssel für Sessions und CSRF-Token (zufällig bei jedem Start)
    app.secret_key = os.urandom(24) 

    # Routen als Blueprint registrieren
    from .routes import main
    app.register_blueprint(main)

    return app

    @app.after_request
    def add_security_headers(response):
        # 1. Content-Security-Policy (CSP)
        #    • default-src 'self'         → nur eigene Domain
        #    • script-src 'self'          → keine externen Scripts
        #    • style-src 'self' cdn.jsdelivr.net → Styles nur von mir und jsdelivr
        #    • img-src 'self' data: upload.wikimedia.org → Bilder nur von mir, Data-URIs und Wikimedia
        #    • font-src 'self' cdn.jsdelivr.net → Fonts nur von mir und jsdelivr
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://upload.wikimedia.org; "
            "font-src 'self' https://cdn.jsdelivr.net;"
        )
        # 2. Verhindert MIME-Type-Sniffing (nosniff)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        # 3. Verhindert Einbetten in iframes (Clickjacking)
        response.headers.setdefault("X-Frame-Options", "DENY")
        return response

    return app