import pytest
import os
from flask import session
from app.routes import main, is_allowed_link
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level
from app.models.quizfrage import Quizfrage
from app.models.reiseziel import Reiseziel, ReisezielDetails
from app.models.quiz import Quiz

from flask import Flask
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(base_dir, "test_templates")

    app = Flask(__name__, template_folder=template_path)
    app.secret_key = 'test'
    app.register_blueprint(main)
    return app


@pytest.fixture
def client(app):
    return app.test_client()

# Funktionstest für Sicherheit (U12)


def test_is_allowed_link():
    assert is_allowed_link("https://de.wikipedia.org/wiki/Berlin") is True
    assert is_allowed_link("https://www.booking.com/hotel") is True
    assert is_allowed_link("https://malicious-site.com") is False

# Test der Startseite (I01)


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Reisequiz" in response.data

# Test der Einstellungs-Seite (I02)


@patch("app.models.kategorie.Kategorie.get_all",
       return_value=[Kategorie("Stadt")])
@patch("app.models.kontinent.Kontinent.get_all",
       return_value=[Kontinent("Europa")])
@patch("app.models.level.Level.get_all",
       return_value=[Level("Test", 2, 10, "Testlevel")])
def test_settings_page(mock_level, mock_kontinent, mock_kategorie, client):
    response = client.get("/settings")
    assert response.status_code == 200
    assert b"Stadt" in response.data
    assert b"Europa" in response.data

# Test Quiz starten (I03)


@patch("app.routes.generiere_quizfrage")
@patch("app.models.level.Level.get_by_name",
       return_value=Level("Test", 2, 10, "Test"))
@patch("app.models.kontinent.Kontinent.get_by_name",
       return_value=Kontinent("Europa"))
@patch("app.models.kategorie.Kategorie.get_by_name",
       return_value=Kategorie("Stadt"))
def test_quiz_route_valid(
        mock_kategorie,
        mock_kontinent,
        mock_level,
        mock_generiere_quizfrage,
        client):
    dummy_frage = Quizfrage(
        "Hinweistext", "img_url", [
            Reiseziel(
                "Rom", Kontinent("Europa"), Kategorie("Stadt"))], Reiseziel(
            "Rom", Kontinent("Europa"), Kategorie("Stadt")))
    dummy_details = ReisezielDetails(
        "Rom", "Beschreibung", "img_url", "booking", "wiki")
    mock_generiere_quizfrage.return_value = (dummy_frage, dummy_details)

    response = client.post("/quiz", data={
        "kategorie": "Stadt",
        "kontinent": "Europa",
        "level": "Test"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Hinweistext" in response.data
    assert b"img_url" in response.data

# Test Ergebnis anzeigen (I04)


@patch("app.routes.lade_reiseziele",
       return_value=[Reiseziel("Rom", Kontinent("Europa"), Kategorie("Stadt"))])
def test_result_view(mock_lade, client, app):
    with client.session_transaction() as sess:
        sess["quiz_config"] = {
            "kategorie": "Stadt",
            "kontinent": "Europa",
            "level": "Test",
            "richtige_antwort": "Rom",
            "details": {
                "beschreibung": "Beschreibung",
                "booking_link": "https://www.booking.com/test",
                "wikipedia_link": "https://de.wikipedia.org/wiki/Rom",
                "bild_url": "img.jpg"
            }
        }
    response = client.post("/result", data={"selected_answer": "Rom"})
    assert response.status_code == 200
    assert b"Rom" in response.data
    assert b"Beschreibung" in response.data
    assert b"booking.com" in response.data

# Ungültige Quiz Einstellung testen (I05)


def test_quiz_invalid_settings_redirect(client):
    response = client.post("/quiz", data={
        "kategorie": "Ungültig",
        "kontinent": "Ungültig",
        "level": "Ungültig"
    }, follow_redirects=True)
    assert "Ungültige Einstellungen" in response.get_data(as_text=True)

# Keine aktvie Quizrunde auf der Ergebnisssteite gefunden (I06)


def test_result_no_quiz_in_session(client):
    response = client.post(
        "/result",
        data={
            "selected_answer": "Rom"},
        follow_redirects=True)
    assert b"Keine aktive Quizrunde gefunden" in response.data

# Reiseziel nicht gefunden (I07)


@patch("app.routes.lade_reiseziele", return_value=[])
def test_result_richtige_antwort_nicht_gefunden(mock_lade, client):
    with client.session_transaction() as sess:
        sess["quiz_config"] = {
            "richtige_antwort": "Unbekanntes Ziel",
            "details": {
                "beschreibung": "Test",
                "booking_link": "https://www.booking.com",
                "wikipedia_link": "https://de.wikipedia.org/wiki/Test",
                "bild_url": "img.jpg"
            }
        }
    response = client.post(
        "/result",
        data={
            "selected_answer": "Test"},
        follow_redirects=True)
    assert b"Reiseziel nicht gefunden" in response.data

# Keine Details in Session (I08)


@patch("app.routes.lade_reiseziele",
       return_value=[Reiseziel("Rom", Kontinent("Europa"), Kategorie("Stadt"))])
def test_result_missing_details_in_session(mock_lade, client):
    with client.session_transaction() as sess:
        sess["quiz_config"] = {
            "richtige_antwort": "Rom"
            # "details" fehlt hier absichtlich
        }
    response = client.post(
        "/result",
        data={
            "selected_answer": "Rom"},
        follow_redirects=True)
    assert b"Fehlende Reisedetails in der Session" in response.data

# Unsichere Links, Sicherheitsprüfung schlägt fehl (I09)


@patch("app.routes.lade_reiseziele",
       return_value=[Reiseziel("Rom", Kontinent("Europa"), Kategorie("Stadt"))])
def test_result_invalid_links_replaced(mock_lade, client):
    with client.session_transaction() as sess:
        sess["quiz_config"] = {
            "richtige_antwort": "Rom",
            "details": {
                "beschreibung": "Beschreibung",
                "booking_link": "https://hacker.com/phishing",
                "wikipedia_link": "https://fakepedia.org/wiki/Test",
                "bild_url": "img.jpg"
            }
        }
    response = client.post("/result", data={"selected_answer": "Rom"})
    assert b'href="#"' in response.data
