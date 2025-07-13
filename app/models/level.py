class Level:
    """
    Repräsentiert ein Schwierigkeitslevel im Quiz.

    Attribute:
        name (str): Anzeigename des Levels (z.B. 'Sofasurfer').
        antwortanzahl (int): Anzahl der Antwortmöglichkeiten.
        verpixelung (int): Stärke der Bildverpixelung (0 = leicht, 2 = schwer).
        beschreibung (str): Kurzbeschreibung zur Anzeige im UI.
    """
    def __init__(self, name: str, antwortanzahl: int, verpixelung: int, beschreibung: str):
        self.name = name
        self.antwortanzahl = antwortanzahl
        self.verpixelung = verpixelung
        self.beschreibung = beschreibung

    @staticmethod
    def get_all() -> list["Level"]:
        """Liefert alle verfügbaren Schwierigkeitsstufen."""
        return [
            Level("Sofasurfer", 2, 0, "Einfach - Für Reise-Anfänger"),
            Level("Backpacker", 4, 1, "Mittel - Für Reise-Erfahrene"),
            Level("Globetrotter", 6, 2, "Schwer - Für Reise-Profis")
        ]

    @staticmethod
    def get_by_name(name: str) -> "Level | None":
        """
        Sucht ein Level anhand seines Namens.
        Args:
            name (str): Der gesuchte Anzeigename.
        Returns:
            Level-Objekt oder None, wenn nicht gefunden.
        """
        return next((level for level in Level.get_all() if level.name == name), None)


