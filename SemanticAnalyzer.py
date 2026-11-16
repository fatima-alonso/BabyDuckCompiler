from BabyDuckListener import BabyDuckListener
from FunctionDirectory import FunctionDirectory
from SemanticCube import SemanticCube


class SemanticAnalyzer(BabyDuckListener):

    def __init__(self, directory=None, valid_function_contexts=None):
        self.directory = directory if directory is not None else FunctionDirectory()
        self.semantic_cube = SemanticCube()
        self.current_function = None
        self.errors = []
        self.expression_types = {}
        self.functions_with_return = set()
        self.valid_function_contexts = valid_function_contexts or set()
        self.skip_current_function = False

    

    # Buscar una variable en las tablas de símbolos
    def get_variable(self, nombre):

        if self.current_function is not None:

            function = self.directory.get_function(
                self.current_function
            )

            if function is not None:
                return function["local_table"].get_symbol(nombre)

        return self.directory.global_table.get_symbol(nombre)

    # Detectar el inicio de una función
    def enterFuncion(self, ctx):

        nombre = ctx.ID().getText()

        if id(ctx) not in self.valid_function_contexts:
            self.current_function = None
            self.skip_current_function = True
            return

        self.current_function = nombre
        self.skip_current_function = False
        self.functions_with_return.discard(nombre)

        

    # Detectar las declaraciones de variables
    def enterVars(self, ctx):
        if self.skip_current_function:
            return

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

        if self.skip_current_function:
            self.skip_current_function = False
            self.current_function = None
            return

        nombre = ctx.ID().getText()

        if self.current_function == nombre:

            function = self.directory.get_function(nombre)

            if function is not None:

                if function["return_type"] != "void":

                    if nombre not in self.functions_with_return:
                        self.errors.append(
                            f"Error: la función '{nombre}' debe "
                            "contener una instrucción return."
                        )

            self.current_function = None

    # Identificar el tipo de cada factor
    def exitFactor(self, ctx):
        if self.skip_current_function:
            return

        if ctx.ID() is not None:

            nombre = ctx.ID().getText()
            variable = self.get_variable(nombre)

            if variable is None:
                self.errors.append(
                    f"Error: variable '{nombre}' no declarada."
                )
                self.expression_types[ctx] = None

            else:
                self.expression_types[ctx] = variable["tipo"]

        elif ctx.cte() is not None:

            constante = ctx.cte()

            if constante.CTE_INT() is not None:
                self.expression_types[ctx] = "int"

            else:
                self.expression_types[ctx] = "float"

        elif ctx.expresion() is not None:

            self.expression_types[ctx] = self.expression_types.get(
                ctx.expresion()
            )

        elif ctx.factor() is not None:

            self.expression_types[ctx] = self.expression_types.get(
                ctx.factor()
            )
        elif ctx.f_call_sin_pyc() is not None:

            self.expression_types[ctx] = self.expression_types.get(
                ctx.f_call_sin_pyc()
            )

    # Evaluar multiplicaciones y divisiones
    def exitTermino(self, ctx):
        if self.skip_current_function:
            return

        factores = ctx.factor()

        if len(factores) == 1:
            self.expression_types[ctx] = self.expression_types.get(
                factores[0]
            )
            return

        result_type = self.expression_types.get(factores[0])

        for i in range(1, len(factores)):

            operator = ctx.getChild(2 * i - 1).getText()
            right_type = self.expression_types.get(factores[i])

            if result_type is None or right_type is None:
                result_type = None
                continue

            result_type = self.semantic_cube.get_result_type(
                result_type,
                operator,
                right_type
            )

            if result_type is None:
                self.errors.append(
                    f"Error: operación '{operator}' incompatible."
                )

        self.expression_types[ctx] = result_type

    # Evaluar sumas y restas
    def exitExp(self, ctx):
        if self.skip_current_function:
            return

        terminos = ctx.termino()

        if len(terminos) == 1:
            self.expression_types[ctx] = self.expression_types.get(
                terminos[0]
            )
            return

        result_type = self.expression_types.get(terminos[0])

        for i in range(1, len(terminos)):

            operator = ctx.getChild(2 * i - 1).getText()
            right_type = self.expression_types.get(terminos[i])

            if result_type is None or right_type is None:
                result_type = None
                continue

            result_type = self.semantic_cube.get_result_type(
                result_type,
                operator,
                right_type
            )

            if result_type is None:
                self.errors.append(
                    f"Error: operación '{operator}' incompatible."
                )

        self.expression_types[ctx] = result_type

    # Evaluar expresiones relacionales
    def exitExpresion(self, ctx):
        if self.skip_current_function:
            return

        expresiones = ctx.exp()

        if len(expresiones) == 1:
            self.expression_types[ctx] = self.expression_types.get(
                expresiones[0]
            )
            return

        left_type = self.expression_types.get(expresiones[0])
        right_type = self.expression_types.get(expresiones[1])
        operator = ctx.rel_op().getText()

        if left_type is None or right_type is None:
            self.expression_types[ctx] = None
            return

        result_type = self.semantic_cube.get_result_type(
            left_type,
            operator,
            right_type
        )

        if result_type is None:
            self.errors.append(
                f"Error: operación relacional incompatible entre "
                f"'{left_type}' y '{right_type}'."
            )

        self.expression_types[ctx] = result_type

    # Validar asignaciones
    def exitAssign(self, ctx):
        if self.skip_current_function:
            return

        nombre = ctx.ID().getText()
        variable = self.get_variable(nombre)

        if variable is None:
            self.errors.append(
                f"Error: variable '{nombre}' no declarada."
            )
            return

        expression_type = self.expression_types.get(ctx.expresion())
        variable_type = variable["tipo"]

        if expression_type is None:
            return

        if not self.semantic_cube.can_assign(
            variable_type,
            expression_type
        ):
            self.errors.append(
                f"Error: no se puede asignar un valor de tipo "
                f"'{expression_type}' a la variable '{nombre}' "
                f"de tipo '{variable_type}'."
            )

    # Validar condiciones if
    def exitCondition(self, ctx):
        if self.skip_current_function:
            return

        expression_type = self.expression_types.get(
            ctx.expresion()
        )

        if expression_type is None:
            return

        if expression_type != "bool":
            self.errors.append(
                "Error: la condición del if debe ser de tipo 'bool'."
            )

    # Validar condiciones while
    def exitCycle(self, ctx):
        if self.skip_current_function:
            return

        expression_type = self.expression_types.get(
            ctx.expresion()
        )

        if expression_type is None:
            return

        if expression_type != "bool":
            self.errors.append(
                "Error: la condición del while debe ser de tipo 'bool'."
            )

    # Validar llamadas a funciones
    def validate_function_call(self, ctx, is_expression=False):

        nombre = ctx.ID().getText()

        function = self.directory.get_function(nombre)

        # Verificar que la función exista
        if function is None:
            self.errors.append(
                f"Error: función '{nombre}' no declarada."
            )

            return None

        # Obtener parámetros esperados
        expected_parameters = function["parameters"]

        # Obtener argumentos enviados
        argumentos_ctx = ctx.argumentos_opt().argumentos()

        if argumentos_ctx is not None:
            arguments = argumentos_ctx.expresion()
        else:
            arguments = []

        # Validar cantidad de argumentos
        if len(arguments) != len(expected_parameters):

            self.errors.append(
                f"Error: la función '{nombre}' esperaba "
                f"{len(expected_parameters)} argumentos, "
                f"pero recibió {len(arguments)}."
            )

            return None

        # Validar tipos de argumentos
        for argument, parameter in zip(
            arguments,
            expected_parameters
        ):

            argument_type = self.expression_types.get(argument)
            parameter_type = parameter["tipo"]

            if argument_type is None:
                continue

            if not self.semantic_cube.can_assign(
                parameter_type,
                argument_type
            ):
                self.errors.append(
                    f"Error: argumento incompatible en la función "
                    f"'{nombre}'. Se esperaba '{parameter_type}' "
                    f"pero se recibió '{argument_type}'."
                )

        # Si la llamada forma parte de una expresión
        return_type = function["return_type"]

        if is_expression and return_type == "void":

            self.errors.append(
                f"Error: la función '{nombre}' no devuelve un valor "
                "y no puede utilizarse en una expresión."
            )

            return None

        return return_type
    # Validar llamadas a funciones como instrucciones
    def exitF_call(self, ctx):
        if self.skip_current_function:
            return

        self.validate_function_call(ctx)

    # Validar llamadas a funciones dentro de expresiones
    def exitF_call_sin_pyc(self, ctx):
        if self.skip_current_function:
            return

        return_type = self.validate_function_call(
            ctx,
            is_expression=True
        )

        self.expression_types[ctx] = return_type

    # Validar instrucciones return
    def exitReturn_stmt(self, ctx):

        if self.skip_current_function:
            return

        if self.current_function is None:
            self.errors.append(
                "Error: return no puede utilizarse fuera de una función."
            )
            return

        function = self.directory.get_function(self.current_function)

        # Si la función no pudo registrarse, no continuar
        if function is None:
            return

        self.functions_with_return.add(self.current_function)

        return_type = function["return_type"]

        expression_type = self.expression_types.get(
            ctx.expresion()
        )

        if return_type == "void":
            self.errors.append(
                f"Error: la función '{self.current_function}' "
                "es void y no debe devolver un valor."
            )
            return

        if expression_type is None:
            return

        if not self.semantic_cube.can_assign(
            return_type,
            expression_type
        ):
            self.errors.append(
                f"Error: la función '{self.current_function}' "
                f"debe devolver '{return_type}', pero devuelve "
                f"'{expression_type}'."
            )

            

       

    # Validar instrucciones read
    def exitRead_stmt(self, ctx):
        if self.skip_current_function:
            return

        nombre = ctx.ID().getText()

        variable = self.get_variable(nombre)

        if variable is None:
            self.errors.append(
                f"Error: variable '{nombre}' no declarada en read."
            )