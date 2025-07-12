class Reiseziel:
    def __init__(self, name, land, kontinent, kategorie):
        self.name = name
        self.kontinent = kontinent  # Instanz von Kontinent
        self.kategorie = kategorie  # Instanz von Kategorie
        self.details = None         # wird später aus API ergänzt

class ReisezielDetails:
    def __init__(self, beschreibung, sehenswuerdigkeiten, image_url, booking_url):
        self.beschreibung = beschreibung
        self.sehenswuerdigkeiten = sehenswuerdigkeiten  # Liste von Attraktionen
        self.image_url = image_url
        self.booking_url = booking_url
