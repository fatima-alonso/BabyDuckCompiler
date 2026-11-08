from BabyDuckListener import BabyDuckListener
from FunctionDirectory import FunctionDirectory
from SemanticCube import SemanticCube


class SemanticAnalyzer(BabyDuckListener):

    def __init__(self):
        self.directory = FunctionDirectory()
        self.semantic_cube = SemanticCube()

        self.current_function = None
        self.errors = []

    # Detectar el inicio de una función
    def enterFuncion(self, ctx):

        nombre = ctx.ID().getText()
        return_type = ctx.retorno().getText()

        parameters = []

        parametros_ctx = ctx.parametros_opt().parametros()

        if parametros_ctx is not None:

            ids = parametros_ctx.ID()
            types = parametros_ctx.type_()

            for nombre_parametro, tipo_parametro in zip(ids, types):

                parameters.append({
                    "nombre": nombre_parametro.getText(),
                    "tipo": tipo_parametro.getText()
                })

        if self.directory.add_function(
            nombre,
            return_type,
            parameters
        ):
            self.current_function = nombre

        else:
            self.errors.append(
                f"Error: función '{nombre}' duplicada, "
                "con conflicto de nombre o parámetros repetidos."
            )

    # Detectar las declaraciones de variables
    def enterVars(self, ctx):

        listas_ids = ctx.lista_id()
        tipos = ctx.type_()

        for lista, tipo_ctx in zip(listas_ids, tipos):

            tipo = tipo_ctx.getText()

            for identificador in lista.ID():

                nombre = identificador.getText()

                if self.current_function is None:

                    valid = self.directory.add_global_variable(
                        nombre,
                        tipo
                    )

                else:

                    valid = self.directory.add_local_variable(
                        self.current_function,
                        nombre,
                        tipo
                    )

                if not valid:
                    self.errors.append(
                        f"Error: variable '{nombre}' duplicada "
                        "o con conflicto de nombre."
                    )

    # Detectar el final de una función
    def exitFuncion(self, ctx):
        self.current_function = None