from urllib.parse import urlencode, quote_plus, quote
from typing import Optional, Mapping
from app.models.reiseziel import Reiseziel

class LinkGenerator:
    """
    Erzeugt dynamische Deeplinks zu Booking.com basierend auf einem Reiseziel.
    Basis-URL und Default-Parameter sind als Klassenattribute definiert
    und können zur Laufzeit oder in Subklassen überschrieben werden,
    ohne den Methodenkörper anzupassen (OCP-konform).
    """
    # Kann per ENV, Config oder in einer Subklasse angepasst werden
    BOOKING_BASE_URL: str = "https://www.booking.com/searchresults.html"
    # Hier lassen sich sinnvolle Default-Parameter (z.B. Sprache, Währung, Affiliate ID) vorgeben
    BOOKING_DEFAULT_PARAMS: Mapping[str, str] = {}

    @classmethod
    def booking_deeplink(
        cls,
        reiseziel: Reiseziel,
        *,
        extra_params: Optional[Mapping[str, str]] = None
    ) -> str:
        """
        Generiert einen Deeplink zur Booking.com-Suche für das angegebene Reiseziel.
        Args:
            reiseziel (Reiseziel): Das Reiseziel, für das ein Buchungslink erzeugt werden soll.
            extra_params (optional): Beliebige zusätzliche Query-Parameter (z.B. {'aid': '123456'} für Affiliate-Links).
        Returns:
            str: Vollständige Booking.com-Such-URL.
        """
        # 1) Starte mit den Default-Parametern (kann leer sein)
        params = dict(cls.BOOKING_DEFAULT_PARAMS)
        # 2) Füge das Reiseziel hinzu
        params["ss"] = reiseziel.name
        # 3) Mische alle zusätzlichen Parameter ein
        if extra_params:
            params.update(extra_params)

        # Baue die Query-String und die komplette URL
        query_string = urlencode(params, quote_via=quote_plus)
        return f"{cls.BOOKING_BASE_URL}?{query_string}"
    
    # Basis-URL mit Platzhalter für die Sprache
    WIKI_BASE_URL: str = "https://{lang}.wikipedia.org/wiki"
    # Standard-Sprache, kann in Subklasse oder zur Laufzeit überschrieben werden
    WIKI_DEFAULT_LANG: str = "de"
    
    @classmethod
    def wikipedia_link_generator(
        cls,
        reiseziel: Reiseziel,
        *,
        lang: Optional[str] = None
    ) -> str:
        """
        Generiert einen Link zur Wikipedia-Seite des Reiseziels. 
        Args:
            reiseziel (Reiseziel): Zielort.
            lang (optional): Sprachcode (z.B. 'de', 'en'). 
        Default: 
            cls.WIKI_DEFAULT_LANG.
        Returns:
            str: URL zur Wikipedia-Seite.
        """
        # Wähle die Sprache: Parameter oder Klassen-Default
        language = lang or cls.WIKI_DEFAULT_LANG
        # Kodierung des Seitentitels
        name_encoded = quote(reiseziel.name.replace(" ", "_"))
        # Ersetze den Platzhalter in der Basis-URL
        base = cls.WIKI_BASE_URL.format(lang=language)
        return f"{base}/{name_encoded}"
