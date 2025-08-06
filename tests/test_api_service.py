import pytest
from unittest.mock import patch, MagicMock
from app.services.api_service import APIService
from app.models.reiseziel import Reiseziel, Kontinent, Kategorie
from requests.exceptions import RequestException


# Beispiel-Reiseziel für Tests
@pytest.fixture
def example_reiseziel():
    return Reiseziel("Berlin", Kontinent("Europa"), Kategorie("Stadt"))

# Test für Hinweistext bei erfolgreicher API-Antwort (U10)


@patch("app.services.api_service.requests.get")
def test_hole_hinweistext_success(mock_get, example_reiseziel):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "extract": "<p>Berlin ist die Hauptstadt von Deutschland.</p>"
    }
    mock_get.return_value = mock_response

    result = APIService.hole_hinweistext(example_reiseziel)
    assert "Berlin ist die Hauptstadt" in result
    assert "<" not in result  # HTML sollte entfernt sein

# Test für Hinweistext bei Fehler (z. B. Timeout) (U11)


@patch("app.services.api_service.requests.get",
       side_effect=RequestException("Timeout"))
def test_hole_hinweistext_fallback_on_exception(mock_get, example_reiseziel):
    result = APIService.hole_hinweistext(example_reiseziel)
    assert result == "Hinweis nicht verfügbar."

# Test für Bild-URL bei erfolgreicher API-Antwort mit HTTPS-Link (U12)


@patch("app.services.api_service.requests.get")
def test_hole_bild_url_success(mock_get, example_reiseziel):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "thumbnail": {
            "source": "https://upload.wikimedia.org/test.jpg"
        }
    }
    mock_get.return_value = mock_response

    result = APIService.hole_bild_url(example_reiseziel)
    assert result.startswith("https://upload.wikimedia.org")

# Test für Bild-URL wenn kein gültiger Link zurückgegeben wird (U13)


@patch("app.services.api_service.requests.get")
def test_hole_bild_url_invalid_data_returns_placeholder(
        mock_get, example_reiseziel):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "thumbnail": {
            "source": "ftp://invalid-link"
        }
    }
    mock_get.return_value = mock_response

    result = APIService.hole_bild_url(example_reiseziel)
    assert result == APIService.PLACEHOLDER_IMAGE_URL

# Test für Bild-URL bei Ausnahme (z. B. Netzwerkausfall) (U14)


@patch("app.services.api_service.requests.get",
       side_effect=RequestException("Network Error"))
def test_hole_bild_url_fallback_on_exception(mock_get, example_reiseziel):
    result = APIService.hole_bild_url(example_reiseziel)
    assert result == APIService.PLACEHOLDER_IMAGE_URL

# Test für statische Platzhalterbild-URL (U15)


def test_placeholder_bild():
    assert APIService.placeholder_bild() == "/static/platzhalter.jpg"
