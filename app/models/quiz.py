from app.models.quizfrage import Quizfrage
from app.models.kategorie import Kategorie
from app.models.kontinent import Kontinent
from app.models.level import Level


class Quiz:
    """
    Repräsentiert eine konfigurierte Quizrunde mit gewählter Kategorie, Kontinent und Schwierigkeitslevel.
    Attribute:
        kategorie (Kategorie): Vom Nutzer gewählte Quiz-Kategorie.
        kontinent (Kontinent): Vom Nutzer gewählter Kontinent.
        level (Level): Vom Nutzer gewähltes Schwierigkeitslevel.
        frage (Quizfrage | None): Generierte Quizfrage (nach Initialisierung noch None).
    """

    def __init__(
            self,
            kategorie: Kategorie,
            kontinent: Kontinent,
            level: Level):
        self.kategorie = kategorie
        self.kontinent = kontinent
        self.level = level
        self.frage: Quizfrage | None = None
