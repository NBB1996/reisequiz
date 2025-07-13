class Kontinent:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all():
        return [Kontinent("Europa"), Kontinent("Asien"), Kontinent("Afrika"),
                Kontinent("Nord-/Mittelamerika"), Kontinent("Südamerika"), Kontinent("Australien und Ozeanien")]

    @staticmethod
    def get_by_name(name):
        for kont in Kontinent.get_all():
            if kont.name == name:
                return kont
        return None
