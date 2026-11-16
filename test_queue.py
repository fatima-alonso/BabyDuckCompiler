from Queue import Queue

cola = Queue()

cola.enqueue(("+", "a", "b", "t1"))
cola.enqueue(("*", "c", "d", "t2"))
cola.enqueue(("=", "t1", "-", "resultado"))

print("Primer elemento:", cola.peek())
print("Elemento retirado:", cola.dequeue())
print("Elementos restantes:", cola.get_all())
print("Tamaño:", cola.size())