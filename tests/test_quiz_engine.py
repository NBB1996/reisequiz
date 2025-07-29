import pytest
from unittest.mock import patch, MagicMock

# Imports aus der Anwendung
from app.quiz_engine import (
    generiere_quizfrage,
    zensiere_reiseziel_name,
    lade_reiseziele,
    verpixle_bild,
    erzeuge_reiseziel_details
)
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level
from app.models.reiseziel import Reiseziel

# Beispiel-Dummy-Level für Schwierigkeitsstufe „Mittel“
@pytest.fixture
def dummy_level():
    return Level(name="Backpacker", antwortanzahl=4, verpixelung=15, beschreibung="Mittel - Für Reise-Erfahrene")

# Kategorie & Kontinent als Enums oder Objekte
@pytest.fixture
def dummy_kategorie():
    return Kategorie("Stadt")

@pytest.fixture
def dummy_kontinent():
    return Kontinent("Europa")

# Dummy-Reiseziele simulieren JSON-Datei
@pytest.fixture
def dummy_reiseziele():
    return [
        {"name": "Paris", "kategorie": "Stadt", "kontinent": "Europa"},
        {"name": "Rom", "kategorie": "Stadt", "kontinent": "Europa"},
        {"name": "Madrid", "kategorie": "Stadt", "kontinent": "Europa"},
        {"name": "Berlin", "kategorie": "Stadt", "kontinent": "Europa"}
    ]

# Hilfsfunktion zur Erstellung von Reiseziel-Objekten
def make_reiseziel(name, kategorie="Stadt", kontinent="Europa"):
    return Reiseziel(name=name, kategorie=Kategorie(kategorie), kontinent=Kontinent(kontinent))

# Testen Reiseziel laden (U01)
@patch("builtins.open", new_callable=MagicMock)
@patch("json.load")
def test_lade_reiseziele(mock_json_load, mock_open):
    """Testet das Laden von Reisezielen aus JSON-Datei."""
    mock_json_load.return_value = [
        {"name": "Paris", "kategorie": "Stadt", "kontinent": "Europa"}
    ]
    result = lade_reiseziele()
    assert len(result) == 1
    assert result[0].name == "Paris"

# Testen Zensur Reisezielname (U02)
def test_zensiere_reiseziel_name():
    """Testet, ob ein Reisezielname korrekt durch '__' ersetzt wird."""
    text = "Paris ist eine wunderschöne Stadt. Ich liebe Paris."
    erwartet = "__ ist eine wunderschöne Stadt. Ich liebe __."
    assert zensiere_reiseziel_name(text, "Paris") == erwartet

# Testen Bild Verpixeln (U03)
@patch("app.quiz_engine.requests.get")
@patch("app.quiz_engine.Image.open")
def test_verpixle_bild_success(mock_image_open, mock_requests_get, dummy_level: Level):
    """Testet erfolgreiche Verpixelung eines Bildes und Base64-Kodierung."""
    dummy_response = MagicMock()
    dummy_response.content = b"fake-image-bytes"
    mock_requests_get.return_value = dummy_response

    dummy_img = MagicMock()
    dummy_img.size = (100, 100)
    dummy_img.resize.return_value = dummy_img
    dummy_img.convert.return_value = dummy_img
    mock_image_open.return_value = dummy_img

    result = verpixle_bild("http://example.com/test.jpg", dummy_level)
    assert result.startswith("data:image/jpeg;base64,"), "Base64-Bild nicht korrekt generiert"

# Testen Fehlerhafte Bild URL (U04)
@patch("app.quiz_engine.requests.get", side_effect=Exception("404 Not Found"))
def test_verpixle_bild_fail(mock_get):
    """Testet das Verhalten bei fehlerhafter Bild-URL (Fallback auf Original)."""
    result = verpixle_bild("http://broken-url.jpg", Level("Test", 2, 10, "Desc"))
    assert result == "http://broken-url.jpg"

# Testen Ungültiger Verpixelungswert (U05)
def test_verpixle_bild_invalid_verpixelung():
    """Testet die Behandlung eines ungültigen Verpixelungswertes (z. B. 0 oder negativ)."""
    level = Level(name="Fehlerhaft", antwortanzahl=2, verpixelung=0, beschreibung="Ungültig")
    result = verpixle_bild("http://invalid-url.jpg", level)
    assert result == "http://invalid-url.jpg"

# Testen API Reiseziel Details erzeugen (U06)
@patch("app.quiz_engine.APIService.hole_hinweistext", return_value="Hinweistext")
@patch("app.quiz_engine.APIService.hole_bild_url", return_value="http://image.jpg")
@patch("app.quiz_engine.LinkGenerator.booking_deeplink", return_value="http://booking")
@patch("app.quiz_engine.LinkGenerator.wikipedia_link_generator", return_value="http://wiki")
def test_erzeuge_reiseziel_details(mock_wiki, mock_booking, mock_bild, mock_text):
    """Testet, ob korrekte ReisezielDetails aus API-Service erzeugt werden."""
    reiseziel = make_reiseziel("Rom")
    details = erzeuge_reiseziel_details(reiseziel)
    assert details.name == "Rom"
    assert details.beschreibung == "Hinweistext"
    assert details.image_url == "http://image.jpg"
    assert details.booking_url == "http://booking"
    assert details.wikipedia_url == "http://wiki"

# Testen Generieren einer Quizfrage (U07)
@patch("app.quiz_engine.lade_reiseziele")
@patch("app.quiz_engine.erzeuge_reiseziel_details")
@patch("app.quiz_engine.verpixle_bild")
def test_generiere_quizfrage_valid(
    mock_verpixle_bild,
    mock_erzeuge_details,
    mock_lade_reiseziele,
    dummy_kategorie,
    dummy_kontinent,
    dummy_level,
    dummy_reiseziele
):
    """Testet die korrekte Erstellung einer Quizfrage inkl. Antwortoptionen."""
    mock_lade_reiseziele.return_value = [
        make_reiseziel(z["name"], z["kategorie"], z["kontinent"]) for z in dummy_reiseziele
    ]
    mock_erzeuge_details.return_value = MagicMock(
        beschreibung="Eine wunderschöne Stadt mit Geschichte",
        image_url="http://example.com/test.jpg",
        booking_url="http://booking.com/test",
        wikipedia_url="http://wikipedia.org/test"
    )

    quizfrage, details = generiere_quizfrage(dummy_kategorie, dummy_kontinent, dummy_level)
    assert quizfrage is not None
    assert quizfrage.richtige_antwort is not None
    assert isinstance(quizfrage.antwortoptionen, list)
    assert len(quizfrage.antwortoptionen) == dummy_level.antwortanzahl
    assert quizfrage.richtige_antwort in quizfrage.antwortoptionen
    assert isinstance(quizfrage.hinweistext, str)
    assert quizfrage.bild_url.startswith("data:image/")

# Testen von Quizfragen mit zu wenigen Antwortoptionen (U08)
@patch("app.quiz_engine.lade_reiseziele")
def test_generiere_quizfrage_too_few_options(mock_lade_reiseziele, dummy_kategorie, dummy_kontinent):
    """Testet Fehlerfall: zu wenige Reiseziele vorhanden für gewünschte Antwortanzahl."""
    mock_lade_reiseziele.return_value = [make_reiseziel("Paris")]
    with pytest.raises(ValueError, match="Nicht genug Reisezieloptionen"):
        generiere_quizfrage(dummy_kategorie, dummy_kontinent, Level("Globetrotter", 6, 70, "Schwer"))

