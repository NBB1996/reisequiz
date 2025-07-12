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
        # Beispiel: Wikipedia-Bild (kann auch Wikivoyage sein)
        url = f"https://de.wikipedia.org/api/rest_v1/page/media/{reiseziel.name}"
        response = requests.get(url)
        if response.status_code == 200:
            pages = response.json().get("items", [])
            for item in pages:
                if item["type"] == "image":
                    return item["original"]["source"]
        return "/static/placeholder.jpg"

    @staticmethod
    def holeWikipediaLink(reiseziel):
        from urllib.parse import quote
        name_encoded = quote(reiseziel.name)
        return f"https://de.wikipedia.org/wiki/{name_encoded}"
