from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from BabyDuckLexer import BabyDuckLexer
from BabyDuckParser import BabyDuckParser
from SemanticAnalyzer import SemanticAnalyzer


codigo = """
program prueba;

var x: int;

int suma(a: int, b: int) [
    var resultado: int;
    {
        resultado = a + b;
        return resultado;
    }
];

main {
    x = 10;
}
end
"""

# 1. Lexer: convierte el código en tokens
input_stream = InputStream(codigo)
lexer = BabyDuckLexer(input_stream)

# 2. Parser: construye el árbol sintáctico
tokens = CommonTokenStream(lexer)
parser = BabyDuckParser(tokens)
tree = parser.programa()

# 3. Semantic Analyzer: recorre el árbol
if parser.getNumberOfSyntaxErrors() == 0:

    print("Programa analizado correctamente.")

    analyzer = SemanticAnalyzer()
    walker = ParseTreeWalker()

    walker.walk(analyzer, tree)

    # Mostrar resultados
    print("\nVariables globales:")
    print(analyzer.directory.global_table.symbols)

    print("\nFunciones:")
    print(analyzer.directory.functions.keys())

    for nombre, info in analyzer.directory.functions.items():
        print(f"\nVariables locales de {nombre}:")
        print(info["local_table"].symbols)

    print("\nErrores semánticos:")
    print(analyzer.errors)

else:
    print("El programa contiene errores de sintaxis.")