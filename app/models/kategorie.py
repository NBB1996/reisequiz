class Kategorie:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all():
        return [Kategorie("Stadt"), Kategorie("Region")]

    @staticmethod
    def get_by_name(name):
        for kat in Kategorie.get_all():
            if kat.name == name:
                return kat
        return None

