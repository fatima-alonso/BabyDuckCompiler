class SymbolTable:

    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def add_symbol(self, nombre, tipo):

        if nombre in self.symbols:
            return False

        self.symbols[nombre] = {
            "tipo": tipo
        }

        return True

    def get_symbol(self, nombre):

        if nombre in self.symbols:
            return self.symbols[nombre]

        if self.parent is not None:
            return self.parent.get_symbol(nombre)

        return None
