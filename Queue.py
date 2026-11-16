class Queue:

    def __init__(self):
        self.items = []

    # Insertar un elemento al final de la cola
    def enqueue(self, item):
        self.items.append(item)

    # Retirar y devolver el primer elemento
    def dequeue(self):
        if self.is_empty():
            return None

        return self.items.pop(0)

    # Consultar el primer elemento
    def peek(self):
        if self.is_empty():
            return None

        return self.items[0]

    # Verificar si está vacía
    def is_empty(self):
        return len(self.items) == 0

    # Obtener el tamaño
    def size(self):
        return len(self.items)

    # Obtener todos los elementos
    def get_all(self):
        return self.items