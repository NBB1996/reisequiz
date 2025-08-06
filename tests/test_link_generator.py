import pytest
from app.services.link_generator import LinkGenerator
from app.models.reiseziel import Reiseziel, Kontinent, Kategorie


@pytest.fixture
def test_reiseziel():
    return Reiseziel("Berlin", Kontinent("Europa"), Kategorie("Stadt"))

# Booking-Link enthält korrekten Reisezielnamen (U16)


def test_booking_deeplink_basic(test_reiseziel):
    url = LinkGenerator.booking_deeplink(test_reiseziel)
    assert "booking.com/searchresults.html" in url
    assert "ss=Berlin" in url

# Booking-Link mit zusätzlichen Parametern (U17)


def test_booking_deeplink_with_extra_params(test_reiseziel):
    url = LinkGenerator.booking_deeplink(
        test_reiseziel,
        extra_params={"aid": "123456", "lang": "de"}
    )
    assert "ss=Berlin" in url
    assert "aid=123456" in url
    assert "lang=de" in url

# Booking-Link encodiert Sonderzeichen korrekt (U18)


def test_booking_deeplink_special_characters():
    ziel = Reiseziel("São Paulo", Kontinent("Südamerika"), Kategorie("Stadt"))
    url = LinkGenerator.booking_deeplink(ziel)
    assert "ss=S%C3%A3o+Paulo" in url

# Wikipedia-Link mit Standardsprache (U19)


def test_wikipedia_link_default_lang(test_reiseziel):
    url = LinkGenerator.wikipedia_link_generator(test_reiseziel)
    assert url == "https://de.wikipedia.org/wiki/Berlin"

# Wikipedia-Link mit benutzerdefinierter Sprache (U20)


def test_wikipedia_link_custom_lang(test_reiseziel):
    url = LinkGenerator.wikipedia_link_generator(test_reiseziel, lang="en")
    assert url == "https://en.wikipedia.org/wiki/Berlin"

# Wikipedia-Link mit Leerzeichen und Umlauten (U21)


def test_wikipedia_link_encoding():
    ziel = Reiseziel(
        "München Altstadt",
        Kontinent("Europa"),
        Kategorie("Stadt"))
    url = LinkGenerator.wikipedia_link_generator(ziel)
    assert "M%C3%BCnchen_Altstadt" in url
