import requests
import bleach
from urllib.parse import quote, urlparse
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
        Gibt den standardmäßigen Header zurück, z.B. für andere Module wie Bildverarbeitung.
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
            response = requests.get(url, headers=APIService.HEADERS, timeout=5)
            if response.status_code == 200:
                # raw/clean als Sicherheitsmaßnahme um nur reinen Text zurück zu geben. 
                raw = response.json().get("extract", "")
                clean = bleach.clean(raw, tags=[], strip=True)
                return clean or "Hinweis nicht verfügbar."
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
            response = requests.get(url, headers=APIService.HEADERS, timeout=5)
            if response.status_code == 200:
                thumb = response.json().get("thumbnail", {})
                src = thumb.get("source", "")
                # URL validieren: nur http(s)-Schema zulassen
                parsed = urlparse(src)
                if parsed.scheme in ("http", "https"):
                    return src
        except requests.RequestException as e:
            print(f"[Fehler Bildabruf {reiseziel.name}]: {e}")
        return APIService.placeholder_bild()

    @staticmethod
    def placeholder_bild() -> str:
        """
        Gibt die URL eines Standard-Platzhalterbilds zurück.
        Returns:
            str: Platzhalterbild-URL.
        """
        return "/static/platzhalter.jpg"

