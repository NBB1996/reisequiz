class Kontinent:
    """
    Repräsentiert einen geografischen Kontinent für die Quizfilterung.
    Attribute:
        name (str): Anzeigename des Kontinents (z.B. 'Europa', 'Asien').
    """

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def get_all() -> list["Kontinent"]:
        """
        Gibt alle verfügbaren Kontinente zurück.
        Returns:
            Liste von Kontinent-Objekten.
        """
        return [
            Kontinent("Afrika"),
            Kontinent("Asien"),
            Kontinent("Australien und Ozeanien"),
            Kontinent("Europa"),
            Kontinent("Nord-/Mittelamerika"),
            Kontinent("Südamerika")
        ]

    @staticmethod
    def get_by_name(name: str) -> "Kontinent | None":
        """
        Sucht einen Kontinent anhand seines Namens.
        Args:
            name (str): Gesuchter Kontinentname.
        Returns:
            Kontinent-Objekt oder None, wenn nicht gefunden.
        """
        return next((k for k in Kontinent.get_all() if k.name == name), None)
