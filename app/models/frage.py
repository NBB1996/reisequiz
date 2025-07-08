class Quizfrage:
    def __init__(self, id, hinweistext, bild_url, antwortoptionen, richtige_antwort):
        self.id = id
        self.hinweistext = hinweistext
        self.bild_url = bild_url
        self.antwortoptionen = antwortoptionen  # Liste von Reiseziel-Objekten
        self.richtige_antwort = richtige_antwort