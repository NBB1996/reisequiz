from app.models.reiseziel import Reiseziel

class Quizfrage:
    """
    Repräsentiert eine einzelne Quizfrage bestehend aus Hinweistext, Bild, Antwortoptionen und Lösung.
    Attribute:
        hinweistext (str): Textlicher Hinweis auf das Reiseziel (aus API, ohne direkten Ortsnamen).
        bild_url (str): URL zum Hinweisbild (ggf. verpixelt je nach Schwierigkeitsstufe).
        antwortoptionen (list[Reiseziel]): Liste möglicher Antwort-Reiseziele.
        richtige_antwort (Reiseziel): Das Reiseziel, das korrekt ist.
        benutzerantwort (Reiseziel | None): Die Antwort, die der Nutzer ausgewählt hat.
    """

    def __init__(
        self,
        hinweistext: str,
        bild_url: str,
        antwortoptionen: list[Reiseziel],
        richtige_antwort: Reiseziel
    ):
        self.hinweistext = hinweistext
        self.bild_url = bild_url
        self.antwortoptionen = antwortoptionen
        self.richtige_antwort = richtige_antwort
        self.benutzerantwort: Reiseziel | None = None

    def ist_richtig(self) -> bool:
        """
        Prüft, ob die vom Nutzer gegebene Antwort korrekt ist.
        Returns:
            True, wenn die Benutzerantwort mit der richtigen Antwort übereinstimmt.
        """
        return self.benutzerantwort == self.richtige_antwort
