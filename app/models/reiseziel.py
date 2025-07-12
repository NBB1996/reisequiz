class Reiseziel:
    def __init__(self, name, kontinent, kategorie):
        self.name = name
        self.kontinent = kontinent  # Instanz von Kontinent
        self.kategorie = kategorie  # Instanz von Kategorie
        self.details = None         # wird später aus API ergänzt

class ReisezielDetails:
    def __init__(self, name, beschreibung, image_url, booking_url, wikipedia_url):
        self.name=name
        self.beschreibung = beschreibung
        self.image_url = image_url
        self.booking_url = booking_url
        self.wikipedia_url = wikipedia_url