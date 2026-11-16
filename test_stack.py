from Stack import Stack

pila = Stack()

pila.push("a")
pila.push("+")
pila.push("b")

print("Elemento superior:", pila.peek())
print("Elemento retirado:", pila.pop())
print("Nuevo elemento superior:", pila.peek())
print("Tamaño:", pila.size())