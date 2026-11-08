# from FunctionDirectory import FunctionDirectory

# directory = FunctionDirectory()

# # Variables globales
# print(directory.add_global_variable("x", "int"))  # True
# print(directory.add_global_variable("y", "float"))  # True

# # Función
# parameters = [
#     {"nombre": "a", "tipo": "int"},
#     {"nombre": "b", "tipo": "int"}
# ]

# print(directory.add_function("suma", "int", parameters))  # True

# # Intentar declarar una función duplicada
# print(directory.add_function("suma", "int", parameters))  # False

# # Agregar variable local
# print(directory.add_local_variable("suma", "resultado", "int"))  # True

# # Intentar duplicar una variable local
# print(directory.add_local_variable("suma", "resultado", "int"))  # False

# # Intentar declarar una función con nombre de variable global
# print(directory.add_function("x", "int", []))  # False

# # Intentar declarar variable global con nombre de función
# print(directory.add_global_variable("suma", "int"))  # False

# # Consultar variable global desde la tabla local
# suma = directory.get_function("suma")
# print(suma["local_table"].get_symbol("x"))  # {'tipo': 'int'}