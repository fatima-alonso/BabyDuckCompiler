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
        # Las llamadas a funciones las agregaremos después.

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
        if ctx.parentCtx.__class__.__name__ == "ConditionContext":
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

            if self.Pjumps.is_empty():
                return

            end = self.Pjumps.pop()

            self.fill_jump(
                end,
                self.Quad.size() + 1
            )

    def generate_false_jump(self):

        result = self.PilaO.pop()
        exp_type = self.PTypes.pop()

        if exp_type != "bool":
            self.errors.append(
                "Error: la condición del if debe ser de tipo bool."
            )
            return

        self.generate_quad(
            "GotoF",
            result,
            "-",
            None
        )

        self.Pjumps.push(self.Quad.size() - 1)