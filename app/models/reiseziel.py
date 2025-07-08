class Reiseziel:
    def __init__(self, id, name, kontinent, kategorie):
        self.id = id
        self.name = name
        self.kontinent = kontinent
        self.kategorie = kategorie
        self.details = None  # ReisezielDetails wird zur Laufzeit ergänzt

class ReisezielDetails:
    def __init__(self, id, beschreibung, aktivitaeten, sehenswuerdigkeiten, buchungslink):
        self.id = id
        self.beschreibung = beschreibung
        self.aktivitaeten = aktivitaeten
        self.sehenswuerdigkeiten = sehenswuerdigkeiten
        self.buchungslink = buchungslink