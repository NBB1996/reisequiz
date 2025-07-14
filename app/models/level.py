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
        """
        Liefert alle verfügbaren Schwierigkeitsstufen. 
        2,4,6 sind die möglichen Antwortoptionen und 40,15,6 der Grad der Verpixelung.
        """
        return [
            Level("Sofasurfer", 2, 70, "Einfach - Für Reise-Anfänger"),     # kaum verpixelt
            Level("Backpacker", 4, 15, "Mittel - Für Reise-Erfahrene"),     # mittel verpixelt
            Level("Globetrotter", 6, 6, "Schwer - Für Reise-Profis")        # stark verpixelt
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


