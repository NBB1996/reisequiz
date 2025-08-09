import pytest
from flask import Flask
from app import create_app

# Prüft, ob die Factory eine Flask-App zurückgibt (U25)


def test_app_factory_returns_flask_app():
    app = create_app()
    assert isinstance(app, Flask)

# Stellt sicher, dass ein zufälliger Secret Key gesetzt wurde (U26)


def test_app_has_secret_key():
    app = create_app()
    assert app.secret_key is not None
    assert isinstance(app.secret_key, bytes)
    assert len(app.secret_key) == 24

# Prüft, ob der Haupt-Blueprint ('main') korrekt registriert wurde (U27)


def test_main_blueprint_registered():
    app = create_app()
    assert "main" in app.blueprints  # "main" ist der Name im Blueprint

# Fixture für den Flask-Testclient (U28)
# Wird genutzt, um Anfragen an die Anwendung zu stellen, ohne dass ein echter Server gestartet werden muss.   


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True  # Aktiviert den Testmodus (z. B. bessere Fehlerausgabe)
    with app.test_client() as client:
        yield client

# Testet, ob die sicherheitsrelevanten HTTP-Header korrekt gesetzt werden


def test_security_headers(client):
    response = client.get('/')
    headers = response.headers

    assert "Content-Security-Policy" in headers, "CSP-Header fehlt"
    assert "X-Content-Type-Options" in headers, "X-Content-Type-Options Header fehlt"
    assert "X-Frame-Options" in headers, "X-Frame-Options Header fehlt"
    assert "default-src" in headers["Content-Security-Policy"], "CSP scheint unvollständig zu sein"
    assert headers["X-Content-Type-Options"] == "nosniff", "X-Content-Type-Options sollte 'nosniff' sein"
    assert headers["X-Frame-Options"] == "DENY", "X-Frame-Options sollte 'DENY' sein"