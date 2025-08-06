from app.models.kontinent import Kontinent
from app.models.kategorie import Kategorie


class Reiseziel:
    """
    Repräsentiert ein Reiseziel (z.B. Stadt oder Region) im Quiz.
    Attribute:
        name (str): Name des Reiseziels (z.B. 'Paris').
        kontinent (Kontinent): Zugehöriger Kontinent.
        kategorie (Kategorie): Zugehörige Kategorie (Stadt oder Region).
        details (ReisezielDetails | None): Detailinformationen aus externen APIs (wird dynamisch ergänzt).
    """

    def __init__(self, name: str, kontinent: Kontinent, kategorie: Kategorie):
        self.name = name
        self.kontinent = kontinent
        self.kategorie = kategorie
        self.details: ReisezielDetails | None = None


class ReisezielDetails:
    """
    Repräsentiert ergänzende Detailinformationen zu einem Reiseziel (aus APIs).
    Attribute:
        name (str): Name des Reiseziels (zur Redundanz/Referenz).
        beschreibung (str): Textuelle Beschreibung (aus Wikipedia).
        image_url (str): Bild-URL (aus API, ggf. verpixelt).
        booking_url (str): Deeplink zu einer Buchungsplattform (z.B. Booking.com).
        wikipedia_url (str): Link zum Wikipedia-Artikel über das Reiseziel.
    """

    def __init__(
        self,
        name: str,
        beschreibung: str,
        image_url: str,
        booking_url: str,
        wikipedia_url: str
    ):
        self.name = name
        self.beschreibung = beschreibung
        self.image_url = image_url
        self.booking_url = booking_url
        self.wikipedia_url = wikipedia_url
