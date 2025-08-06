import requests
import bleach
from urllib.parse import quote, urlparse
from typing import Optional, Mapping
from app.models.reiseziel import Reiseziel


class APIService:
    """
    Liefert Daten über Wikipedia APIs für Quiz-Hinweise, Bilder und Links.
    """

    # Konfigurierbare Klassenattribute
    HEADERS: Mapping[str, str] = {
        "User-Agent": "ReisequizApp/1.0 (kontakt@mein-reisequiz.de)"
    }

    # Endpoint-Templates mit Platzhalter für Sprache und Titel
    SUMMARY_ENDPOINT: str = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    IMAGE_ENDPOINT: str = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    # Default-Sprachen für Text und Bild
    SUMMARY_DEFAULT_LANG: str = "de"
    IMAGE_DEFAULT_LANG: str = "en"
    # URL für das Platzhalterbild
    PLACEHOLDER_IMAGE_URL: str = "/static/platzhalter.jpg"

    @classmethod
    def get_standard_headers(cls) -> Mapping[str, str]:
        """Gibt den standardmäßigen Header zurück (kann zur Laufzeit angepasst werden)."""
        return cls.HEADERS

    @classmethod
    def hole_hinweistext(
        cls,
        reiseziel: Reiseziel,
        *,
        lang: Optional[str] = None
    ) -> str:
        """
        Holt einen Kurztext aus der Wikipedia als Beschreibung.
        Args:
            reiseziel: Zielort.
            lang: Sprachcode (z.B. 'de', 'en').
        Default:
            SUMMARY_DEFAULT_LANG.
        Returns:
            Extrakt aus der Wikipedia-Zusammenfassung oder Fallback-Text.
        """
        language = lang or cls.SUMMARY_DEFAULT_LANG
        title = quote(reiseziel.name.replace(" ", "_"))
        url = cls.SUMMARY_ENDPOINT.format(lang=language, title=title)

        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=5)
            if resp.status_code == 200:
                raw = resp.json().get("extract", "")
                clean = bleach.clean(raw, tags=[], strip=True)
                return clean or "Hinweis nicht verfügbar."
        except requests.RequestException as e:
            print(f"[Fehler beim Hinweistext für {reiseziel.name}]: {e}")
        return "Hinweis nicht verfügbar."

    @classmethod
    def hole_bild_url(
        cls,
        reiseziel: Reiseziel,
        *,
        lang: Optional[str] = None
    ) -> str:
        """
        Holt ein Vorschaubild aus der Wikipedia.
        Args:
            reiseziel: Zielort.
            lang: Sprachcode (z.B. 'de', 'en').
        Default:
            IMAGE_DEFAULT_LANG.
        Returns:
            URL eines Wikipedia-Bilds oder eines Platzhalterbilds.
        """
        language = lang or cls.IMAGE_DEFAULT_LANG
        title = quote(reiseziel.name.replace(" ", "_"))
        url = cls.IMAGE_ENDPOINT.format(lang=language, title=title)

        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=5)
            if resp.status_code == 200:
                thumb = resp.json().get("thumbnail", {})
                src = thumb.get("source", "")
                parsed = urlparse(src)
                if parsed.scheme in ("http", "https"):
                    return src
        except requests.RequestException as e:
            print(f"[Fehler Bildabruf {reiseziel.name}]: {e}")

        # Fallback auf konfiguriertes Platzhalterbild
        return cls.PLACEHOLDER_IMAGE_URL

    @classmethod
    def placeholder_bild(cls) -> str:
        """
        Gibt die URL eines Standard-Platzhalterbilds zurück.
        """
        return cls.PLACEHOLDER_IMAGE_URL
