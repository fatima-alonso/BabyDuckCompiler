from SymbolTable import SymbolTable


class FunctionDirectory:

    def __init__(self):
        self.functions = {}
        self.global_table = SymbolTable()

    # Registrar una función
    def add_function(self, nombre, return_type, parameters):

        # Validar que no exista otra función con ese nombre
        if nombre in self.functions:
            return False

        # Validar que no exista una variable global con ese nombre
        if self.global_table.get_symbol(nombre) is not None:
            return False

        local_table = SymbolTable(parent=self.global_table)

        # Registrar parámetros en la tabla local
        for parameter in parameters:
            if not local_table.add_symbol(
                parameter["nombre"],
                parameter["tipo"]
            ):
                return False

        self.functions[nombre] = {
            "return_type": return_type,
            "parameters": parameters,
            "local_table": local_table
        }

        return True

    # Obtener información de una función
    def get_function(self, nombre):
        return self.functions.get(nombre)

    # Registrar una variable global
    def add_global_variable(self, nombre, tipo):

        # Validar que no exista una función con ese nombre
        if nombre in self.functions:
            return False

        return self.global_table.add_symbol(nombre, tipo)

    # Registrar una variable local
    def add_local_variable(self, function_name, nombre, tipo):

        function = self.get_function(function_name)

        # Validar que la función exista
        if function is None:
            return False

        local_table = function["local_table"]

        return local_table.add_symbol(nombre, tipo)