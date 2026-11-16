from BabyDuckListener import BabyDuckListener
from FunctionDirectory import FunctionDirectory


class FunctionCollector(BabyDuckListener):

    def __init__(self):
        self.directory = FunctionDirectory()
        self.errors = []
        self.valid_function_contexts = set()
        self.global_variables = set()


    def enterPrograma(self, ctx):

        vars_ctx = ctx.vars_()

        lista_ids = vars_ctx.lista_id()
        
        for lista in lista_ids:
            for identificador in lista.ID():
                self.global_variables.add(identificador.getText())

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
        # Validar conflicto con variable global
        if nombre in self.global_variables:
            self.errors.append(
                f"Error: el nombre '{nombre}' ya está utilizado "
                "por una variable global."
            )
            return

        # 1. Validar función duplicada
        if nombre in self.directory.functions:
            self.errors.append(
                f"Error: la función '{nombre}' ya fue declarada."
            )
            return

        # 2. Validar conflicto con variable global
        if self.directory.global_table.get_symbol(nombre) is not None:
            self.errors.append(
                f"Error: el nombre '{nombre}' ya está utilizado "
                "por una variable global."
            )
            return

        # 3. Validar parámetros duplicados
        nombres_parametros = [p["nombre"] for p in parameters]

        if len(nombres_parametros) != len(set(nombres_parametros)):
            duplicados = [
                nombre_parametro
                for nombre_parametro in nombres_parametros
                if nombres_parametros.count(nombre_parametro) > 1
            ]

            duplicados = list(set(duplicados))

            self.errors.append(
                f"Error: la función '{nombre}' tiene parámetros "
                f"duplicados: {', '.join(duplicados)}."
            )
            return

        # 4. Registrar función
        if self.directory.add_function(nombre, return_type, parameters):
            self.valid_function_contexts.add(id(ctx))
