class Level:
    def __init__(self, id, name, schwierigkeit, anzahl_antwortoptionen):
        self.id = id         # "leicht", "mittel", "schwer"
        self.name = name     # "Sofasurfer", ...
        self.schwierigkeit = schwierigkeit
        self.anzahl_antwortoptionen = anzahl_antwortoptionen
