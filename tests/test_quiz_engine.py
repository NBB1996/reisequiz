import pytest
from unittest.mock import patch, MagicMock


from app.quiz_engine import generiere_quizfrage
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
dummy_reiseziele = [
    {"name": "Paris", "kategorie": "Stadt", "kontinent": "Europa"},
    {"name": "Rom", "kategorie": "Stadt", "kontinent": "Europa"},
    {"name": "Madrid", "kategorie": "Stadt", "kontinent": "Europa"},
    {"name": "Berlin", "kategorie": "Stadt", "kontinent": "Europa"}
]

# Temporäres ersetzten der echten Funktionen durch Platzhalter (Mocks)
@patch("app.quiz_engine.lade_reiseziele")
@patch("app.quiz_engine.erzeuge_reiseziel_details")
@patch("app.quiz_engine.verpixle_bild")
def test_generiere_quizfrage_valid(
    mock_verpixle_bild,
    mock_erzeuge_details,
    mock_lade_reiseziele,
    dummy_kategorie,
    dummy_kontinent,
    dummy_level
):
    """
    Testet, ob generiere_quizfrage ein gültiges Quizfrage-Objekt liefert,
    mit der erwarteten Anzahl an Antwortoptionen und einer enthaltenen richtigen Antwort.
    """

    # 1. Mocking der Rückgaben vorbereiten
    mock_lade_reiseziele.return_value = [
        Reiseziel(name=z["name"], kategorie=Kategorie(z["kategorie"]), kontinent=Kontinent(z["kontinent"]))
        for z in dummy_reiseziele
    ]

    mock_erzeuge_details.return_value = MagicMock(
        beschreibung="Eine wunderschöne Stadt mit Geschichte",
        image_url="http://example.com/test.jpg",
        booking_url="http://booking.com/test",
        wikipedia_url="http://wikipedia.org/test"
    )

    mock_verpixle_bild.return_value = "data:image/jpeg;base64,DUMMY"

    # 2. Funktion aufrufen
    quizfrage, details = generiere_quizfrage(dummy_kategorie, dummy_kontinent, dummy_level)

    # 3. Prüfung des Rückgabeobjekts
    assert quizfrage is not None
    assert quizfrage.richtige_antwort is not None
    assert isinstance(quizfrage.antwortoptionen, list)
    assert len(quizfrage.antwortoptionen) == dummy_level.antwortanzahl
    assert quizfrage.richtige_antwort in quizfrage.antwortoptionen
    assert isinstance(quizfrage.hinweistext, str)
    assert "Paris" not in quizfrage.hinweistext  # Hinweistext zensiert Zielnamen
    assert quizfrage.bild_url.startswith("data:image/")  # Base64-Vorschaubild
