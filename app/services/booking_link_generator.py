from urllib.parse import urlencode, quote_plus
from app.models.reiseziel import Reiseziel
class BookingDeeplinkGenerator:
    """
    Erzeugt dynamische Deeplinks zu Booking.com basierend auf einem Reiseziel.
    """
    @staticmethod
    def bereitstellung_deeplink(reiseziel: Reiseziel) -> str:
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
