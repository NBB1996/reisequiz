import requests

class APIService:
    @staticmethod
    def holeHinweistext(reiseziel):
        # Beispiel: Wikipedia-API für Beschreibung
        url = f"https://de.wikipedia.org/api/rest_v1/page/summary/{reiseziel.name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("extract")
        return "Hinweis nicht verfügbar."

    @staticmethod
    def holeBildURL(reiseziel):
        """
        Holt ein Vorschaubild aus Wikipedia (englische Version) über den summary-Endpoint.
        """
        titel = reiseziel.name.replace(" ", "_")
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{titel}"

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                thumbnail = data.get("thumbnail", {})
                if "source" in thumbnail:
                    return thumbnail["source"]
        except Exception as e:
            print(f"[Bildabruf-Fehler für {reiseziel.name}]:", e)

        return "https://via.placeholder.com/400x250?text=Kein+Bild"

    @staticmethod
    def holeWikipediaLink(reiseziel):
        from urllib.parse import quote
        name_encoded = quote(reiseziel.name)
        return f"https://de.wikipedia.org/wiki/{name_encoded}"
