class Quizfrage:
    def __init__(self, hinweistext, bild_url, antwortoptionen, richtige_antwort):
        self.hinweistext = hinweistext  # Beschreibungstext (aus API)
        self.bild_url = bild_url        # Bild (ggf. verpixelt)
        self.antwortoptionen = antwortoptionen  # Liste von Reiseziel-Objekten
        self.richtige_antwort = richtige_antwort  # Das Reiseziel-Objekt, das korrekt ist
        self.benutzerantwort = None  # Das vom Nutzer ausgewählte Reiseziel

    def ist_richtig(self):
        return self.benutzerantwort == self.richtige_antwort
