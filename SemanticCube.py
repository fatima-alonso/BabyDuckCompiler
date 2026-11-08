class SemanticCube:

    def __init__(self):

        self.cube = {}

        # Operaciones aritméticas
        arithmetic_operators = ["+", "-", "*", "/"]
        numeric_types = ["int", "float"]

        for operator in arithmetic_operators:
            for left_type in numeric_types:
                for right_type in numeric_types:

                    if operator == "/" or "float" in (left_type, right_type):
                        result_type = "float"
                    else:
                        result_type = "int"

                    self.cube[(left_type, operator, right_type)] = result_type

        # Operaciones relacionales
        relational_operators = [">", "<", "!="]

        for operator in relational_operators:
            for left_type in numeric_types:
                for right_type in numeric_types:
                    self.cube[(left_type, operator, right_type)] = "bool"

    def get_result_type(self, left_type, operator, right_type):
        return self.cube.get((left_type, operator, right_type))

    def can_assign(self, target_type, expression_type):

        if target_type == expression_type:
            return True

        if target_type == "float" and expression_type == "int":
            return True

        return False

