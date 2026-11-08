from antlr4 import InputStream, CommonTokenStream
from BabyDuckLexer import BabyDuckLexer
from BabyDuckParser import BabyDuckParser

# Programa de prueba
codigo = """
program prueba;

var x: int;

main {
    x = (10 + 5;
}


"""

# Crear el flujo de entrada
input_stream = InputStream(codigo)

# Crear el Scanner (Lexer)
lexer = BabyDuckLexer(input_stream)

# Convertir los tokens en un flujo
tokens = CommonTokenStream(lexer)

# Crear el Parser
parser = BabyDuckParser(tokens)

# Analizar el programa usando la regla principal
tree = parser.programa()

if parser.getNumberOfSyntaxErrors() == 0:
    print("Programa analizado correctamente.")
else:
    print("El programa contiene errores de sintaxis.")
print(tree.toStringTree(recog=parser))