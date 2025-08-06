from flask import Flask
from app import create_app

# Prüft, ob die Factory eine Flask-App zurückgibt (U22)


def test_app_factory_returns_flask_app():
    app = create_app()
    assert isinstance(app, Flask)

# Stellt sicher, dass ein zufälliger Secret Key gesetzt wurde (U23)


def test_app_has_secret_key():
    app = create_app()
    assert app.secret_key is not None
    assert isinstance(app.secret_key, bytes)
    assert len(app.secret_key) == 24

# Prüft, ob der Haupt-Blueprint ('main') korrekt registriert wurde (U24)


def test_main_blueprint_registered():
    app = create_app()
    assert "main" in app.blueprints  # "main" ist der Name im Blueprint
