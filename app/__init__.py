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
