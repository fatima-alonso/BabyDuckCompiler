class Stack:

    def __init__(self):
        self.items = []

    # Insertar un elemento en la pila
    def push(self, item):
        self.items.append(item)

    # Retirar y devolver el elemento superior
    def pop(self):
        if self.is_empty():
            return None

        return self.items.pop()

    # Consultar el elemento superior
    def peek(self):
        if self.is_empty():
            return None

        return self.items[-1]

    # Verificar si la pila está vacía
    def is_empty(self):
        return len(self.items) == 0

    # Obtener el tamaño de la pila
    def size(self):
        return len(self.items)