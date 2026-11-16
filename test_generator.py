from QuadrupleGenerator import QuadrupleGenerator

generator = QuadrupleGenerator()

t1 = generator.new_temp()

generator.generate_quad("*", "b", "c", t1)

t2 = generator.new_temp()

generator.generate_quad("+", "a", t1, t2)

for quad in generator.Quad.get_all():
    print(quad)