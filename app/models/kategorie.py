class Kategorie:
    """
    Repräsentiert eine auswählbare Quiz-Kategorie, z.B. 'Stadt' oder 'Region'.
    Attribute:
        name (str): Anzeigename der Kategorie.
    """

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def get_all() -> list["Kategorie"]:
        """
        Gibt alle verfügbaren Kategorien zurück.
        Returns:
            Liste von Kategorie-Objekten.
        """
        return [
            Kategorie("Stadt"),
            Kategorie("Region")
        ]

    @staticmethod
    def get_by_name(name: str) -> "Kategorie | None":
        """
        Sucht eine Kategorie anhand ihres Namens.
        Args:
            name (str): Gesuchter Kategoriename.
        Returns:
            Kategorie-Objekt oder None, wenn nicht gefunden.
        """
        return next((kat for kat in Kategorie.get_all() if kat.name == name), None)


