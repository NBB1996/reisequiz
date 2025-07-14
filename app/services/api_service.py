import requests
from urllib.parse import quote
from app.models.reiseziel import Reiseziel

class APIService:
    """
    Liefert Daten über Wikipedia APIs für Quiz-Hinweise, Bilder und Links.
    """

    # Zentral definierter User-Agent für alle Wikimedia-Anfragen
    HEADERS = {
        "User-Agent": "ReisequizApp/1.0 (kontakt@mein-reisequiz.de)"
    }

    @staticmethod
    def get_standard_headers():
        """
        Gibt den standardmäßigen Header zurück, z. B. für andere Module wie Bildverarbeitung.
        """
        return APIService.HEADERS

    @staticmethod
    def hole_hinweistext(reiseziel: Reiseziel) -> str:
        """
        Holt einen Kurztext aus der deutschen Wikipedia als Beschreibung.
        Args:
            reiseziel (Reiseziel): Das Ziel, zu dem der Hinweistext geladen werden soll.
        Returns:
            str: Extrakt aus der Wikipedia-Zusammenfassung oder ein Fallback-Text.
        """
        url = f"https://de.wikipedia.org/api/rest_v1/page/summary/{quote(reiseziel.name)}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json().get("extract", "Hinweis nicht verfügbar.")
        except requests.RequestException as e:
            print(f"[Fehler beim Hinweistext für {reiseziel.name}]: {e}")
        return "Hinweis nicht verfügbar."

    @staticmethod
    def hole_bild_url(reiseziel: Reiseziel) -> str:
        """
        Holt ein Vorschaubild aus der englischen Wikipedia (bessere Bildverfügbarkeit).
        Args:
            reiseziel (Reiseziel): Das Ziel, zu dem ein Bild geladen werden soll.
        Returns:
            str: URL eines Wikipedia-Bilds oder eines Platzhalterbilds.
        """
        titel = reiseziel.name.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(titel)}"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                thumbnail = data.get("thumbnail", {})
                return thumbnail.get("source", APIService._placeholder_bild())
        except requests.RequestException as e:
            print(f"[Fehler beim Bildabruf für {reiseziel.name}]: {e}")
        return APIService._placeholder_bild()

    @staticmethod
    def hole_wikipedia_link(reiseziel: Reiseziel) -> str:
        """
        Generiert einen Link zur deutschsprachigen Wikipedia-Seite des Reiseziels.
        Args:
            reiseziel (Reiseziel): Zielort.
        Returns:
            str: URL zur Wikipedia-Seite.
        """
        name_encoded = quote(reiseziel.name)
        return f"https://de.wikipedia.org/wiki/{name_encoded}"

    @staticmethod
    def _placeholder_bild() -> str:
        """
        Gibt die URL eines Standard-Platzhalterbilds zurück.
        Returns:
            str: Platzhalterbild-URL.
        """
        return "https://via.placeholder.com/400x250?text=Kein+Bild"

