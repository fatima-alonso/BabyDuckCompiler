from BabyDuckListener import BabyDuckListener
from Stack import Stack
from Queue import Queue
from Quadruple import Quadruple
from SemanticCube import SemanticCube


class QuadrupleGenerator(BabyDuckListener):

    def __init__(self, directory):
        # Pilas
        self.POper = Stack()
        self.PilaO = Stack()
        self.PTypes = Stack()
        self.Pjumps = Stack()
        self.Pcycles = Stack()



        # Cola de cuádruplos
        self.Quad = Queue()

        # Control de temporales
        self.temp_counter = 1

        # Información semántica
        self.directory = directory
        self.semantic_cube = SemanticCube()
        self.current_function = None
        self.errors = []

    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp

    def generate_quad(self, operator, left, right, result):
        quad = Quadruple(operator, left, right, result)
        self.Quad.enqueue(quad)

    # Buscar el tipo de una variable
    def get_variable(self, nombre):

        if self.current_function is not None:
            function = self.directory.get_function(
                self.current_function
            )

            if function is not None:
                return function["local_table"].get_symbol(nombre)

        return self.directory.global_table.get_symbol(nombre)

    # Obtener operandos y tipos de las pilas
    def get_operands(self, cantidad):

        operands = []
        types = []

        for _ in range(cantidad):
            operands.append(self.PilaO.pop())
            types.append(self.PTypes.pop())

        operands.reverse()
        types.reverse()

        return operands, types

    
    def process_function_call(self, ctx, use_result):

        nombre = ctx.ID().getText()

        # Obtener la información de la función
        function = self.directory.get_function(nombre)

        # Recuperar las expresiones que se pasan como argumentos
        argumentos_ctx = ctx.argumentos_opt().argumentos()

        if argumentos_ctx is not None:
            cantidad = len(argumentos_ctx.expresion())
        else:
            cantidad = 0

        # Recuperar operandos y tipos en el orden original
        operands, types = self.get_operands(cantidad)

        # Verificar que la función exista
        if function is None:
            self.errors.append(
                f"Error: la función '{nombre}' no está declarada."
            )
            return None, None

        parameters = function["parameters"]
        return_type = function["return_type"]

        # Verificar cantidad de argumentos
        if cantidad != len(parameters):
            self.errors.append(
                f"Error: la función '{nombre}' espera "
                f"{len(parameters)} argumentos, pero recibió {cantidad}."
            )
            return None, None

        # Verificar tipos de los argumentos
        for i, (argument_type, parameter) in enumerate(
            zip(types, parameters)
        ):
            parameter_type = parameter["tipo"]

            if not self.semantic_cube.can_assign(
                parameter_type,
                argument_type
            ):
                self.errors.append(
                    f"Error: el argumento {i + 1} de la función "
                    f"'{nombre}' debe ser de tipo '{parameter_type}', "
                    f"pero se recibió '{argument_type}'."
                )
                return None, None

        # Una función void no puede utilizarse como expresión
        if use_result and return_type == "void":
            self.errors.append(
                f"Error: la función '{nombre}' no retorna un valor "
                "y no puede utilizarse dentro de una expresión."
            )
            return None, None

        # Reservar el espacio para ejecutar la función
        self.generate_quad(
            "ERA",
            nombre,
            "-",
            "-"
        )

        # Pasar los argumentos a sus respectivos parámetros
        for i, operand in enumerate(operands):
            self.generate_quad(
                "PARAM",
                operand,
                "-",
                i + 1
            )

        # Preparar el temporal que recibirá el valor de retorno
        if use_result:
            result = self.new_temp()
        else:
            result = "-"

        # Ejecutar la función
        self.generate_quad(
            "GOSUB",
            nombre,
            "-",
            result
        )

        return result, return_type


    # Procesar factores
    def exitFactor(self, ctx):

        if ctx.ID() is not None:

            nombre = ctx.ID().getText()
            variable = self.get_variable(nombre)

            if variable is None:
                self.errors.append(
                    f"Error: variable '{nombre}' no declarada."
                )
                self.PilaO.push(nombre)
                self.PTypes.push(None)

            else:
                self.PilaO.push(nombre)
                self.PTypes.push(variable["tipo"])

        elif ctx.cte() is not None:

            constante = ctx.cte()

            if constante.CTE_INT() is not None:
                tipo = "int"
            else:
                tipo = "float"

            self.PilaO.push(constante.getText())
            self.PTypes.push(tipo)

        # Los paréntesis ya fueron procesados por expresion.
        # Las llamadas a funciones se procesan en exitF_call_sin_pyc.
        # Su resultado ya queda en las pilas de operandos y tipos.

    # Procesar multiplicaciones y divisiones
    def exitTermino(self, ctx):

        factores = ctx.factor()

        operands, types = self.get_operands(len(factores))

        result = operands[0]
        result_type = types[0]

        for i in range(1, len(factores)):

            operator = ctx.getChild(2 * i - 1).getText()

            right_operand = operands[i]
            right_type = types[i]

            new_type = self.semantic_cube.get_result_type(
                result_type,
                operator,
                right_type
            ) if result_type is not None and right_type is not None else None

            if new_type is None:
                self.errors.append(
                    f"Error: operación '{operator}' incompatible."
                )
                result = None
                result_type = None

            else:
                temp = self.new_temp()

                self.generate_quad(
                    operator,
                    result,
                    right_operand,
                    temp
                )

                result = temp
                result_type = new_type

        self.PilaO.push(result)
        self.PTypes.push(result_type)

    # Procesar sumas y restas
    def exitExp(self, ctx):

        terminos = ctx.termino()

        operands, types = self.get_operands(len(terminos))

        result = operands[0]
        result_type = types[0]

        for i in range(1, len(terminos)):

            operator = ctx.getChild(2 * i - 1).getText()

            right_operand = operands[i]
            right_type = types[i]

            new_type = self.semantic_cube.get_result_type(
                result_type,
                operator,
                right_type
            ) if result_type is not None and right_type is not None else None

            if new_type is None:
                self.errors.append(
                    f"Error: operación '{operator}' incompatible."
                )
                result = None
                result_type = None

            else:
                temp = self.new_temp()

                self.generate_quad(
                    operator,
                    result,
                    right_operand,
                    temp
                )

                result = temp
                result_type = new_type

        self.PilaO.push(result)
        self.PTypes.push(result_type)

    def enterFuncion(self, ctx):
        self.current_function = ctx.ID().getText()

    def exitFuncion(self, ctx):
        self.current_function = None

    def exitAssign(self, ctx):

        nombre = ctx.ID().getText()

        # Recuperar resultado y tipo de la expresión
        resultado = self.PilaO.pop()
        tipo_expresion = self.PTypes.pop()

        # Buscar variable destino
        variable = self.get_variable(nombre)

        if variable is None:
            self.errors.append(
                f"Error: variable '{nombre}' no declarada."
            )
            return

        tipo_variable = variable["tipo"]

        # Validar compatibilidad de tipos
        if not self.semantic_cube.can_assign(
            tipo_variable,
            tipo_expresion
        ):
            self.errors.append(
                f"Error: no se puede asignar "
                f"'{tipo_expresion}' a '{tipo_variable}'."
            )
            return

        # Generar cuádruplo de asignación
        self.generate_quad(
            "=",
            resultado,
            "-",
            nombre
        )
    

    def exitArg_print(self, ctx):

        # Caso 1: imprimir una cadena de texto
        if ctx.CTE_STRING() is not None:

            texto = ctx.CTE_STRING().getText()

            self.generate_quad(
                "PRINT",
                texto,
                "-",
                "-"
            )

        # Caso 2: imprimir una expresión
        elif ctx.expresion() is not None:

            resultado = self.PilaO.pop()
            tipo = self.PTypes.pop()

            if resultado is not None and tipo is not None:

                self.generate_quad(
                    "PRINT",
                    resultado,
                    "-",
                    "-"
                )
    
    def exitRead_stmt(self, ctx):

        nombre = ctx.ID().getText()

        # Verificar que la variable esté declarada
        variable = self.get_variable(nombre)

        if variable is None:
            self.errors.append(
                f"Error: variable '{nombre}' no declarada."
            )
            return

        # Generar cuádruplo de lectura
        self.generate_quad(
            "READ",
            "-",
            "-",
            nombre
        )

    
    def exitReturn_stmt(self, ctx):

        # Recuperar el resultado de la expresión
        resultado = self.PilaO.pop()
        tipo = self.PTypes.pop()

        # Verificar que exista un resultado válido
        if resultado is None or tipo is None:
            self.errors.append(
                "Error: no se pudo generar el valor de retorno."
            )
            return

        # Generar cuádruplo de retorno
        self.generate_quad(
            "RETURN",
            resultado,
            "-",
            "-"
        )

    
    # Llamada a función como una instrucción independiente
    def exitF_call(self, ctx):

        self.process_function_call(
            ctx,
            use_result=False
        )


    # Llamada a función dentro de una expresión
    def exitF_call_sin_pyc(self, ctx):

        resultado, tipo = self.process_function_call(
            ctx,
            use_result=True
        )

        if resultado is not None and tipo is not None:
            self.PilaO.push(resultado)
            self.PTypes.push(tipo)




    def exitExpresion(self, ctx):

        # Si no existe operador relacional,
        # la expresión ya fue procesada por exitExp.
        if ctx.rel_op() is None:
            return

        # Recuperar los dos operandos y sus tipos
        operands, types = self.get_operands(2)

        left_operand = operands[0]
        right_operand = operands[1]

        left_type = types[0]
        right_type = types[1]

        operator = ctx.rel_op().getText()

        # Validar la operación relacional
        result_type = self.semantic_cube.get_result_type(
            left_type,
            operator,
            right_type
        ) if left_type is not None and right_type is not None else None

        if result_type is None:
            self.errors.append(
                f"Error: comparación '{operator}' incompatible."
            )
            self.PilaO.push(None)
            self.PTypes.push(None)
            return

        # Generar temporal
        temp = self.new_temp()

        # Generar cuádruplo
        self.generate_quad(
            operator,
            left_operand,
            right_operand,
            temp
        )

        # Guardar el resultado booleano
        self.PilaO.push(temp)
        self.PTypes.push(result_type)

       # Si esta expresión pertenece a la condición de un if,
        # generar el salto falso inmediatamente.
        if ctx.parentCtx.__class__.__name__ in (
            "ConditionContext",
            "CycleContext"
        ):
            self.generate_false_jump()

    def fill_jump(self, position, destination):
        quad = self.Quad.get_all()[position]
        quad.fill_result(destination)

    def enterCondition(self, ctx):
        # La expresión se procesa después de entrar a Condition.
        # El salto se genera al terminar de evaluar la expresión.
        pass

    def exitCondition(self, ctx):

        if ctx.ELSE() is None:

            # IF sin ELSE
            if self.Pjumps.is_empty():
                return

            end = self.Pjumps.pop()

            self.fill_jump(
                end,
                self.Quad.size() + 1
            )

        else:

            # IF-ELSE
            if self.Pjumps.is_empty():
                return

            end = self.Pjumps.pop()

            self.fill_jump(
                end,
                self.Quad.size() + 1
            )
    def enterCycle(self, ctx):

        # Guardar la posición donde comienza el while
        start = self.Quad.size() + 1

        self.Pcycles.push(start)


    def exitCycle(self, ctx):

        # Recuperar la posición inicial del ciclo
        return_position = self.Pcycles.pop()

        # Generar salto incondicional al inicio del while
        self.generate_quad(
            "GOTO",
            "-",
            "-",
            return_position
        )

        # Recuperar el GotoF generado por la condición
        false_jump = self.Pjumps.pop()

        # Completar el destino para salir del ciclo
        self.fill_jump(
            false_jump,
            self.Quad.size() + 1
        )

    def generate_false_jump(self):

        result = self.PilaO.pop()
        exp_type = self.PTypes.pop()

        if exp_type != "bool":
            self.errors.append(
                "Error: la condición debe ser de tipo bool."
            )
            return

        self.generate_quad(
            "GotoF",
            result,
            "-",
            None
        )

        self.Pjumps.push(self.Quad.size() - 1)

    def exitStatement(self, ctx):

        parent = ctx.parentCtx

        # Verificar que pertenece directamente a un if-else
        if parent.__class__.__name__ != "ConditionContext":
            return

        if parent.ELSE() is None:
            return

        statements = parent.statement()

        # Nos interesa únicamente el primer statement (bloque IF)
        if ctx != statements[0]:
            return

        # Generar GOTO para saltar el bloque ELSE
        self.generate_quad(
            "GOTO",
            "-",
            "-",
            None
        )

        # Guardar la posición del GOTO
        goto_position = self.Quad.size() - 1

        # Completar el GotoF para que apunte al ELSE
        false_jump = self.Pjumps.pop()

        self.fill_jump(
            false_jump,
            self.Quad.size() + 1
        )

        # Guardar el GOTO pendiente
        self.Pjumps.push(goto_position)