class Quadruple:

    def __init__(self, operator, left_operand, right_operand, result):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result

    def __str__(self):
        return (
            f"({self.operator}, "
            f"{self.left_operand}, "
            f"{self.right_operand}, "
            f"{self.result})"
        )

    def fill_result(self, result):
        self.result = result