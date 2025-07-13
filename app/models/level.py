class Level:
    def __init__(self, name, antwortanzahl, verpixelung):
        self.name = name
        self.antwortanzahl = antwortanzahl
        self.verpixelung = verpixelung  # z. B. 0 (leicht) bis 3 (stark)

    @staticmethod
    def get_all():
        return [
            Level("Sofasurfer", 2, 0),
            Level("Backpacker", 4, 1),
            Level("Globetrotter", 6, 2)
        ]

    @staticmethod
    def get_by_name(name):
        for level in Level.get_all():
            if level.name == name:
                return level
        return None

