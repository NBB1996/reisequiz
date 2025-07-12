from app.models.quizfrage import Quizfrage

class Quiz:
    def __init__(self, kategorie, kontinent, level):
        self.kategorie = kategorie
        self.kontinent = kontinent
        self.level = level
        self.frage: Quizfrage | None = None