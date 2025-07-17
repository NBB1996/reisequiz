from urllib.parse import urlencode, quote_plus, quote
from app.models.reiseziel import Reiseziel
class LinkGenerator:
    """
    Erzeugt dynamische Deeplinks zu Booking.com basierend auf einem Reiseziel.
    """
    @staticmethod
    def booking_deeplink(reiseziel: Reiseziel) -> str:
        """
        Generiert einen Deeplink zur Booking.com-Suche für das angegebene Reiseziel.
        Args:
            reiseziel (Reiseziel): Das Reiseziel, für das ein Buchungslink erzeugt werden soll.
        Returns:
            str: Vollständige Booking.com-Such-URL.
        """
        base_url = "https://www.booking.com/searchresults.html"
        params = {"ss": reiseziel.name}
        query_string = urlencode(params, quote_via=quote_plus)
        
        return f"{base_url}?{query_string}"
    
    @staticmethod
    def wikipedia_link_generator(reiseziel: Reiseziel) -> str:
        """
        Generiert einen Link zur deutschsprachigen Wikipedia-Seite des Reiseziels.
        Args:
            reiseziel (Reiseziel): Zielort.
        Returns:
            str: URL zur Wikipedia-Seite.
        """
        name_encoded = quote(reiseziel.name)
        return f"https://de.wikipedia.org/wiki/{name_encoded}"
